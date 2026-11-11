import math
from tracemalloc import start
from typing import NamedTuple, Optional
from pathlib import Path
from collections import deque

"""
Summary of AI usage (add any AI usage here)
1. Gemini reminded me (Samantha) how to make a namedtuple with optional values
2. Claude helped with the planning of the VMSim Class, specifically
    how to seperate the function responsibilities
3. Claude verified that the function plans (and how they would work) smelled right
4. Claude suggested the next_instructions function in the Process class
5. AI assisted Sofia in commenting the parse_trace_file function
6. Claude helped reminded Sam how to sort a list of dicts by a specific key (lambda function)
7. AI helped Gerald with testing scripts. It provided the script after Gerald made the code and explained what he needed to 
    accomplish in his classes. 
"""

# constants
page_table_entries = 512 * 1024
page_offset = 12 #12 bits for 4k page size

class Instruction(NamedTuple):
    """
    This class basically creates an instruction object with a named tuple
    This way, we can store all of the information of the instructions like:
    Instruction(eip_len=#, eip_addr="this", src="this or None", dst="this or None")  
    Note that if we don't have a source or desination, we ignore this instruction!  
    """
    eip_len: int
    eip_addr: str
    src: Optional[str] = None
    dst: Optional[str] = None
 
    
def parse_trace_file(trace_file: Path) -> list[Instruction]:
    instructions = []

    with open(trace_file, "r") as f:
        lines = f.read().splitlines()

        # removes blanks
        lines = [line.strip() for line in lines if line.strip()]

        # reading
        for i in range(0, len(lines), 2):
            instruction_line = lines[i]
            memory_line = lines[i + 1]

            # Get instruction
            eip_len = int(instruction_line[5:7])
            eip_addr = instruction_line[10:18]

            # Get source/destination
            parts = memory_line.split()

            dst_addr = parts[1]
            dst_data = parts[2]
            src_addr = parts[4]
            src_data = parts[5]

            # Ignore invalid
            if dst_addr == "00000000" or dst_data == "--------":
                dst_addr = None

            if src_addr == "00000000" or src_data == "--------":
                src_addr = None

            # Create instruction
            instruction = Instruction(eip_len, eip_addr, src_addr, dst_addr)
            instructions.append(instruction)

    return instructions

class Process:
    """Each trace file = a process, processes need to store some data, so its best to just make a class out of it nno?"""
    
    def __init__(self, trace_file: Path, pid: int):
        self.pid = pid
        self.name = Path(trace_file).name
        self.instructions = parse_trace_file(trace_file)
        self.instruction_position = 0 # Index of the instruction to run, we start at zero ofc
        self.page_table = [None for i in range(page_table_entries)]
        # self.used_entries = 0 # number of page table entries that aren't none? 
        
    def is_finished(self) -> bool:
        # We finished this process when the number of isntructiosn we completed for it 
        # is greater or equal to the length (total) instructions
        return self.instruction_position >= len(self.instructions)
    
    def next_instructions(self, n:int) -> list[Instruction]:
        """we will execute n instructions at a time, so we should probably have a way to get just those"""
        # TODO: return n instructions with offset self.instruction_position.
        # ex. self.instruction_position=4 we want 2 instructions, return self.instructions[4:6] which returns 4,5
        # TODO: then increment the position to instruction_position + n

        #Grab the first instruction, Count all inst to see where to end, get all inst between start and end, update posisiton to be the
        # latest, send selected instr up.  

        start = self.instruction_position
        end = min(start + n, len(self.instructions))

        batch = self.instructions[start:end]
        self.instruction_position = end

        return batch
        
        
class VMSim:
    def __init__(
        self, trace_files: list, num_physical_pages: int, 
        num_system_pages: int, instructions: int, entry_size: int
    ):
        self.user_pages = num_physical_pages - num_system_pages
        self.num_system_pages = num_system_pages
        self.time_slice = instructions #NOTE: If this is -1 then we do all instructions
        self.free_pool = [i for i in range(self.user_pages)] #We need user pages number of entries
        self.entry_bits = entry_size
        """
        This may need to be changed but idea is to have {process: [(free_pool index, vpn)]}
        where process is the process.pid, free_pool index is the value that you get when you pop(0) from free pool
        and vpn is the page number that is using it
        """
        self.used_pages: dict[deque] = {} # I added typehinting to this so vscode would resolve the functions
        """This way when we release a page we can just take this value and extend the free pool (.extend())"""
        self.processes: list[Process] = [] #same thing here (sam's personal preference )
        count = 0
        for process in trace_files:
            new_process = Process(process, count)
            count+=1
            self.processes.append(new_process)
            self.used_pages[new_process.pid] = deque() #allows us to round robin FIFO when we need to replace
        
        self.total_translations = 0
        self.page_table_hits = 0
        self.pages_from_free = 0
        self.page_faults = 0
        self.trace_results = []
    
    def run(self) -> dict: # in theory return a dictionary of results
        """
        while at least one process is not finished (you may want to use the any() function)
            for each unfinished process (may need to create a list of these processes to keep track)
                run_single_process(process)
                check if process is finished
                    if it is finished cleanup()
                    remove process from list of unfinished processes
        
        return {
            "system_pages": value,
            "user_pages": value,
            "virtual_pages_mapped": hits + misses (aka free) + faults,
            "hits": hits,
            "faults": faults,
            "free": free (pages from free),
            "trace_results":self.trace_results #List of dictionaires
        }
        
        """
        while any(not p.is_finished() for p in self.processes):
            for process in self.processes:
                if process.is_finished(): continue
                self.run_single_process(process)
                if process.is_finished():
                    self.cleanup(process)
        
        return{
            'system_pages': self.num_system_pages,
            'user_pages': self.user_pages,
            'virtual_pages_mapped': self.page_table_hits + self.pages_from_free + self.page_faults,
            'hits': self.page_table_hits,
            'faults': self.page_faults,
            'free': self.pages_from_free,
            'trace_results': sorted(self.trace_results, key=lambda r: r['pid']),
        }
    
    def run_single_process(self, process:Process):
        """Runs a single process by perfomring trnanslations for n instructions"""
        """
        for instruction in next instructions (from process class)
        # Note that if self.time_slice = -1 then we call process.next_instructions(len(process.instructions))
            for each address in that instruction 
                NOTE: This is the eip_addr, src, and dst (check if any of them is None)
                NOTE: you can probably do something like for instruction in [instruction.eip_addr, instruction.src, instruction.dst]:
                    and then if instruction: (execute everything else) this prevents doing something on None
                convert the address from a string to an int using python int(str,16)
                virtual_page_num = address shifted to the right 12 (to get rid of the 12 offset bits)
                self.total-translations +=1
                check if process.page_table is none at virtual_page_num index
                if not None: hit (increment hits as necessary)
                if None and the free pool length is not zero: miss (free) (increment), pop free pool at zero,
                    append (free pool at zero, vpn) to self.used_pages[process.pid], and add that instruction to the process' page table[virtual_page_num]
                if none but the free pool length is zero: page fault (increment), popleft from self.used_pages[process.name] (fifo)
                    append (index, new_vpn) to self.used_pages, if self.used_pages has nothing, evict from another process's used pages

        """
        # The number of instructions to do per time slice
        num_instructions = len(process.instructions) if self.time_slice == -1 else self.time_slice
        
        for instruction in process.next_instructions(num_instructions):
            for addr in (instruction.eip_addr, instruction.src, instruction.dst): 
                if addr is None: continue # We don't want to run into None errors so continue if address is None
                addr_as_int = int(addr, 16) # I didn't know this was a thing, but very convenient!
                vpn = addr_as_int >> page_offset
                self.total_translations += 1
                
                if process.page_table[vpn] is not None:
                    self.page_table_hits += 1
                
                elif process.page_table[vpn] is None and len(self.free_pool) > 0:
                    self.pages_from_free += 1
                    resource = self.free_pool.pop(0)
                    self.used_pages[process.pid].append((resource, vpn))
                    process.page_table[vpn] = resource
                
                else:
                    self.page_faults += 1
                    if len(self.used_pages[process.pid]) > 0:
                        # If we can take from ourselves lets do that
                        resource, old_vpn = self.used_pages[process.pid].popleft()
                        self.used_pages[process.pid].append((resource, vpn))
                        process.page_table[old_vpn] = None # clear old spot
                        process.page_table[vpn] = resource
                    else:
                        # Otherwise steal from someone else!
                        victim_processes = [victims for victims in self.processes if victims.pid != process.pid]
                        for victim in victim_processes:
                            if len(self.used_pages[victim.pid]) > 0:
                                resource, old_vpn = self.used_pages[victim.pid].popleft()
                                self.used_pages[process.pid].append((resource, vpn))
                                victim.page_table[old_vpn] = None
                                process.page_table[vpn] = resource
                                break
                        # I am going to assume that there will never be a case where all of the processes have 0 used pages
                
    def cleanup(self, process:Process):
        """Used when a process is completed"""
        pass
        """
        something like: 
        for used_page, vpn in self.used_pages[process.pid]:
            self.freepool.append(used_page)
            self.trace_results.append(
                {
                'pid': process.pid
                "name": name,
                "used_page_table_entries": value
                "percent_used": used / page_table_entries * 100,
                "wasted": (PAGE_TABLE_ENTRIES - used_entries) * entry_size_bits / 8, rounded down
            }
                }
            )
            # Clear things up
            process.pagetable = [None for i in range(page_table_entries)]
        """

        # Count the pages used by the process, calculate page table usage and wasted memory,
        # save the stats, return physical pages to the free pool, remove page mappings,
        # and clear the process's used pages.

        used_entries = len(self.used_pages[process.pid])

        percent_used = (used_entries / page_table_entries) * 100

        wasted = ((page_table_entries - used_entries)
                * self.entry_bits) // 8

        self.trace_results.append({
            "pid": process.pid,
            "name": process.name,
            "used_page_table_entries": used_entries,
            "percent_used": percent_used,
            "wasted": wasted
        })

        for physical_page, vpn in self.used_pages[process.pid]:
            self.free_pool.append(physical_page)
            process.page_table[vpn] = None

        self.used_pages[process.pid].clear()

