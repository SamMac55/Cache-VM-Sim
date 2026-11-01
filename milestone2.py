from typing import NamedTuple, Optional
from pathlib import Path

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