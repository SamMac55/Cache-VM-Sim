"""
Hosts all calculations
"""

import math # Need this for log and exponent related things

# Cache calculations
def calc_total_blocks(cache_size: int, block_size: int) -> int:
    """
    Calculates total number of blocks using cache_size* 2^10/block_size
    
    Returns total number of blocks
    """
    # TODO: implement func
    pass
    
def calc_index(cache_size: int, block_size: int, associativity: int) -> int:
    """
    Calculates index bits using log2(cachesize*1024/(block_size*associativity))
    
    returns index bits
    """
    # TODO : implement
    pass

def calc_num_rows(index_bits:int) -> int:
    """
    Calculates number of rows using 2^ index_bits
    
    returns #rows
    """
    # TODO: impelemt
    pass

def calc_tag_size(physical_mem_size: int, index_bits:int, block_size:int) -> int:
    """
    Calculates tag size
    Using log2(physical_mem_size * 2^20) - index_bits - log2(block_size) (I think ?)
    """
    #TODO: implement
    pass

def calc_overhead(total_blocks: int, tag_bits: int) -> int:
    """
    Calculates overhead bytes
    ( tag_bits + 1 (aka valid bit) ) * total blocks / 8 (for bytes, round up)
    """
    # TODO: implement
    pass

def calc_implementation_memory_size(cache_size: int, overhead:int) -> int:
    """
    Calculates the implementation size
    NOTE: I am pretty sure off the top of my head this is just cache_size(given)* 1024 + overhead
    """
    # TODO: implement
    pass

def calc_cost(implementation_size: int, cost_per_KB: int) -> float:
    """
    Calculates total cost by implement_size/1024 * cost per KB
    
    NOTE: I Think cost will be a given/constant, in this case we don't need param
    """
    # TODO: implement
    pass
    
# Physical calcs
"""
Example:
Number of Physical Pages: 262144
Number of Pages for System: 196608 ( 0.75 * 262144 = 196608 )
Size of Page Table Entry: 19 bits (1 valid bit, 18 for PhysPage)
Total RAM for Page Table(s): 3735552 bytes (512K entries * 3 .trc files * 19 / 8)"""

def calc_num_physical_pages(physical_mem_size: int) -> int:
    """
    Calculates the number of physical pages with 4K page size assumption
    bits = log2(physical_mem_size)+20-12
    return 2^bits
    """
    # TODO: implement
    pass

def calc_num_pages_system(percent_used_by_sys: float, num_phys_pages: int) -> int:
    """Calculates number of system pages using int( percent/100*num_pages )"""
    # TODO: implement
    pass

def calc_size_of_entry(num_pages: int) -> int:
    """"Calculates size of page table entry 1(validbit)+log2(num_pages)"""
    # TODO: implement
    pass

def calc_total_ram(entry_size_bits: int, num_traces: int, page_table_entries: int) -> int:
    """Calculates total ram in bytes: page_table_entries * traces * entry_size_bits // 8"""
    #TODO: implement
    pass

    
