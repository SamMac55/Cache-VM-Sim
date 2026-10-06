"""
This file will include functions that print out the results according to
assignment specifications. 
"""

# Milestone 1
def print_header( trace_files: list ):
    """
    Prints the header + trace files
    
    Input: List of trace files names
    """
    
    """
    Example (view specs for exact view): 
    Cache Simulator - CS 3853 – Team #XX
        Trace File(s):
        Trace1.trc
        Trace2_4Evaluation.trc
        Corruption1.trc
    """
    # TODO: implement function
    pass

def print_cache_input_params(
    cache_size: int,
    block_size: int,
    associativity: int,
    replacement_policy: str,
    physical_memory: int,
    percent_memory_used: int,
    instructions_time_slice: int,
):
    """
    Prints cache simulator input parameters
    
    Inputs: all of the cache inputs we recieve from cli :)
    """
    
    """Example: (view project specs for exact things)
    
    ***** Cache Input Parameters *****
        Cache Size: 512 KB
        Block Size: 16 bytes
        Associativity: 4
        Replacement Policy: Round Robin
        Physical Memory: 1024 MB
        Percent Memory Used by System: 75.0%
        Instructions / Time Slice: 100
    """
    # TODO: implement function
    pass

def print_cache_calculated_values(
    total_blocks: int,
    tag_size: int,
    index_size: int,
    total_rows: int,
    overhead_size: int,
    implementation_mem_size: int,
    cost_total: float,
    cost_per_KB: float
):
    """
    Prints the cache simulator calculated vals
    
    Inputs: The results of the calculations + the cost per KB
    """
    
    """
    Example: (view project specs for details)
    
    ***** Cache Calculated Values *****
        Total # Blocks: 32768
        Tag Size: 13 bits  Note: (based on actual physical memory)
        Index Size: 13 bits
        Total # Rows: 8192
        Overhead Size: 57344 bytes
        Implementation Memory Size: 568.00 KB (581632 bytes)
        Cost: $39.76 @ $0.07 per KB
    
    """
    # TODO: implement function   
    pass

def print_physical_mem_calculated_vals(
    num_physical_pages: int,
    num_system_pages: int,
    size_of_page_table_entry: int,
    total_ram: int
):
    """
    Prints the physical memory calculations
    
    Inputs: calculated values from physical memory calculations
    """
    # TODO: implement function
    pass

# Milestone 2
def print_vm_sim_results(
    physical_pages_by_sys: int,
    pages_for_user: int,
    virtual_pages_mapped: int,
    page_table_hits: int,
    pages_from_free: int,
    total_page_faults: int,
    traces_results: dict
):
    """
    Prints virtual simulation results
    
    Inputs: simulation results
    NOTE: traces results is a dict in format:
    { trace_file_name: {used_entries: int, table_wasted: int}}
    """
    """Example (view docs for info)
    
    ***** VIRTUAL MEMORY SIMULATION RESULTS *****
        Physical Pages Used By SYSTEM: 196608  NOTE: -u % * total physical pages
        Pages Available to User: 65536
        Virtual Pages Mapped: 310224
        ------------------------------
        Page Table Hits: 309585 - the virtual page is already mapped in
        the page table – a hit!
        Pages from Free: 639 - # times a virtual page is mapped to a
        physical page not currently in use
        Total Page Faults: 0 - # times when no physical page is available
        and must be swapped with one in use
        Page Table Usage Per Process:
        ------------------------------
        [0] Trace1.trc:
        Used Page Table Entries: 132 ( 0.03%)
        Page Table Wasted: 1244870 bytes
        [1] Trace2_4Evaluation.trc:
        Used Page Table Entries: 303 ( 0.06%)
        Page Table Wasted: 1244464 bytes
        [2] Corruption_1.trc:
        Used Page Table Entries: 204 ( 0.04%)
        Page Table Wasted: 1244699 bytes
        """
    # TODO: implement function for milestone 2
    pass

# Milestone 3
def print_cache_sim_results(
    total_accesses: int,
    instruction_bytes: int,
    src_dst_bytes: int,
    cache_hits: int,
    cache_misses: int,
    compulsory_missses: int,
    conflict_misses: int,
    hit_rate: float,
    miss_rate: float,
    cpi: float,
    unused_cache_space: str, # In format: 428.87 KB / 568.00 KB = 75.68% Waste: $30.09/chip
    unused_cahce_blocks: str, # In format: 24799 / 32768
):
    """
    Example (view docs)
    ***** CACHE SIMULATION RESULTS *****
    Total Cache Accesses: 341318 (310224 addresses) # times cache row hit
    --- Instruction Bytes: 725273
    --- SrcDst Bytes: 287120
    Cache Hits: 331769 it was valid and tag matched
    Cache Misses: 9549 it was either not valid or tag didn’t match
    --- Compulsory Misses: 9546 it was not valid
    --- Conflict Misses: 3 it was valid, tag did not match
    ***** ***** CACHE HIT & MISS RATE: ***** *****
    Hit Rate: 97.2023% (Hits * 100) / Total Accesses
    Miss Rate: 2.7977% 1 – Hit Rate
    CPI: 4.33 Cycles/Instruction (238444) # Cycles/# Instr
    Unused Cache Space: 428.87 KB / 568.00 KB = 75.68% Waste: $30.09/chip
    Unused Cache Blocks: 24799 / 32768
    // NOTE: A cache access is any time an address maps to a row.
    // reading 7 bytes and hitting two rows is counted as two accesses, not 7.
    // Unused KB = ( (TotalBlocks-Compulsory Misses) * (BlockSize+OverheadSize) ) / 1024
    // The 1024 KB below is the total cache size for this example
    // Waste = COST/KB * Unused KB
    """
    
    #TODO implement func @ milestone 3
    pass