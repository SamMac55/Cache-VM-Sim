"""
Hosts all calculations
"""

# Cache calculations
def calc_total_blocks(cache_size: int, block_size: int) -> int:
    """
    Calculates total number of blocks using cache_size/block_size
    
    Returns total number of blocks
    """
    # TODO: implement func
    pass
    
def calc_index(cache_size: int, block_size: int, associativity: int) -> int:
    """
    Calculates index bits using cachesize/(block_size*associativity)
    
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
    Using log2(physical_mem_size) - index_bits - log2(block_size) (I think ?)
    """
    #TODO: implement
    pass

def calc_overhead(num_rows: int, tag_bits: int) -> int:
    """
    Calculates overhead bytes
    NOTE: Calculation formula coming soon
    """
    # TODO: implement
    pass

def calc_implementation_memory_size(cache_size: int, overhead:int) -> int:
    """
    Calculates the implementation size
    NOTE: I am pretty sure off the top of my head this is just cache_size(given) + overhead,
    but I need to check this, params may chagne
    """
    # TODO: implement
    pass

def calc_cost(implementation_size: int, cost_per_KB: int) -> int:
    """
    Calculates total cost by implement_size * cost per KB
    
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

def calc_num_physical_pages() -> int:
    """Calculates the number of physical pages
    NOTE: Calculation/params coming soon"""
    # TODO: implement
    pass

def calc_num_pages_system(percent_used_by_sys: float, num_phys_pages: int) -> int:
    """Calculates number of system pages using percent*num_pages"""
    # TODO: implement
    pass

def calc_size_of_entry(num_pages: int) -> int:
    """"Calculates size of page table entry 1(validbit)+log2(num_pages)"""
    # TODO: implement
    pass

def calc_total_ram():
    """Calculates total ram, params and calc coming soon"""
    #TODO: implement
    pass

    
