from typing import NamedTuple, Optional
from pathlib import Path
from collections import deque

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
    
    def __init__(self, trace_file: Path):
        self.name = Path(trace_file).name
        self.instructions = parse_trace_file(trace_file)
        self.instruction_position = 0 # Index of the instruction to run, we start at zero ofc
        self.page_table = [None for i in range(page_table_entries)]
        self.used_entries = 0 # number of page table entries that aren't none? 
        
    def is_finished(self) -> bool:
        # We finished this process when the number of isntructiosn we completed for it 
        # is greater or equal to the length (total) instructions
        return self.instruction_position >= len(self.instructions)
    
    def next_instructions(self, n:int) -> list:
        """we will execute n instructions at a time, so we should probably ahve a way to get just those"""
        # TODO: return n instructions with offset self.instruction_position.
        # ex. self.instruction_position=4 we want 2 instructions, return self.instructions[4:6] which returns 4,5
        # TODO: then increment the position to instruction_position + n
        
class VMSim:
    def __init__(
        self, trace_files: list, num_physical_pages: int, 
        num_system_pages: int, instructions: int, entry_size: int
    ):
        self.user_pages = num_physical_pages - num_system_pages
        self.num_system_pages = num_system_pages
        self.instructions = instructions #NOTE: If this is -1 then we do all instructions
        self.free_pool = [i for i in range(self.user_pages)] #We need user pages number of entries
        self.entry_bits = entry_size
        """
        This may need to be changed but idea is to have {process: [(free_pool index, vpn)]}
        where process is the process.name, free_pool index is the value that you get when you pop(0) from free pool
        and vpn is the page number that is using it
        """
        self.used_pages = {}
        """This way when we release a page we can just take this value and extend the free pool (.extend())"""
        self.processes = []
        for process in trace_files:
            new_process = Process(process)
            new_process_name = new_process.name
            self.processes.append(new_process)
            self.used_pages[new_process_name] = deque() #allows us to round robin FIFO when we need to replace
        
        self.total_translations = 0
        self.page_table_hits = 0
        self.pages_from_free = 0
        self.page_faults = 0
        self.trace_results = []
    
    def run(self) -> dict: # in theory return a dictionary of results
        pass
        """
        while at least one process is not finished
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
            "free": free,
            "trace_results":self.trace_results #List of dictionaires
        }
        
        """
    
    def run_single_process(self, process:Process):
        """Runs a single process by perfomring trnanslations for n instructions"""
        pass
        """
        for instruction in next instructions (from process class)
        # Note that if self.instructions = -1 then we call process.next_instructions(len(process.instructions))
            for each address in that instruction NOTE: This is the eip_addr, src, and dst
                convert the address from a string to an int using python int(str,16)
                virtual_page_num = address shifted to the right 12 (to get rid of the 12 offset bits)
                self.total-translations +=1
                check if process.page_table is none at virtual_page_num index
                if not None: hit (increment hits as necessary)
                if None and the free pool length is not zero: miss (free) (increment), pop free pool at zero,
                    append (free pool at zero, vpn) to self.used_pages[process.name]
                if none but the free pool length is zero: page fault (increment), pop from self.used_pages[process.name] (fifo)
                    append (index, new_vpn) to self.used_pages

        """
    def cleanup(self, process:Process):
        """Used when a process is completed"""
        pass
        """for used_page, vpn in self.used_pages[process.name]:
            self.freepool.append(used_page)
            self.trace_results.append(
                {
                "name": name,
                "used_page_table_entries": value
                "percent_used": value,
                "wasted": (PAGE_TABLE_ENTRIES - used_entries) * entry_size_bits / 8, rounded down
            }
                }
            )
            process.pagetable = [None for i in range(page_table_entries)]
        """
