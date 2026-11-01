from typing import NamedTuple, Optional
from pathlib import Path

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
    
def parse_trace_file(trace_file: Path) -> list:
    """
    To make our lives easier, we should parse the entire trace file first
    and then return a list of instructions for this trace file. This is becaues
    we will run -n number of instructions per trace at a time, and keeping track
    of file offsets and reading from the file multiple times will be difficult
    """
    
    # TODO: Open the file using with open(trace_file, "r") as f:
    
        # TODO: Read all of the lines into a list using f.read().splitlines()
    """ NOTE: lines 0,1 are an instruction, line 2 is blank bc of how the trace files are
    you may want to do something to remove those blank lines...    
    """
        # TODO: Once those blank lines are cleaned, iterate through the lines (two lines at a time), and create the 
        #   instruction
        
    """NOTE: the first line, eip_length = line[5:7] (convert to an int) and eip_addr is line[10:18]
    the second line will look something like this: dstM: 00000000 --------    srcM: 0012cdb8 40ce1200
    the first thing after each colon is the address then the second is the data. We ignore if the data is -------
    I think that all zero addresses are also considered invalid?"""
        # TODO: append instruction to a list of instructions
    
    # TODO: When done, return the list of instructions
    pass

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
    def __init__():
        pass