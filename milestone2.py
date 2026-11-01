from typing import NamedTuple, Optional

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