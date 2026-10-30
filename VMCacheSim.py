from argparse import ArgumentParser
from pathlib import Path

import src.calculate as calculate
import src.print_milestones as print_milestones

def main(
    cache_size: int,
    block_size: int,
    associativity: int,
    replacement_policy: str,
    physical_mem_size: int,
    phys_mem_used_percent: float,
    time_slice: int,
    trace_files: list,
):
    """
    Orchestration function for the program.
    """
    # Constants
    cost_per_kb = 0.07
    page_table_entries = 512 * 1024
    # Cache calculations
    total_blocks = calculate.calc_total_blocks(cache_size, block_size)
    index_bits = calculate.calc_index(cache_size, block_size, associativity)
    rows = calculate.calc_num_rows(index_bits)
    tag_bits = calculate.calc_tag_size(physical_mem_size, index_bits, block_size)
    overhead = calculate.calc_overhead(total_blocks, tag_bits)
    cache_implementation_size = calculate.calc_implementation_memory_size(cache_size, overhead)
    cost = calculate.calc_cost(cache_implementation_size, cost_per_kb)
    
    # Physical Memory calculations
    num_physical_pages = calculate.calc_num_physical_pages(physical_mem_size)
    system_pages = calculate.calc_num_pages_system(phys_mem_used_percent, num_physical_pages)
    entry_size = calculate.calc_size_of_entry(num_physical_pages)
    total_ram = calculate.calc_total_ram(entry_size, len(trace_files), page_table_entries)
    
    # Print everything out
    print_milestones.print_header(trace_files)
    print_milestones.print_cache_input_params(
        cache_size = cache_size,
        block_size = block_size,
        associativity = associativity,
        replacement_policy = replacement_policy,
        physical_memory = physical_mem_size,
        percent_memory_used = phys_mem_used_percent,
        instructions_time_slice = time_slice
    )
    print_milestones.print_cache_calculated_values(
        total_blocks = total_blocks,
        tag_size = tag_bits,
        index_size = index_bits,
        total_rows = rows,
        overhead_size = overhead,
        implementation_mem_size = cache_implementation_size,
        cost_total = cost,
        cost_per_KB = cost_per_kb,
    )
    print_milestones.print_physical_mem_calculated_vals(
        num_physical_pages = num_physical_pages,
        num_system_pages = system_pages,
        size_of_page_table_entry = entry_size,
        total_ram = total_ram,
    )
    
    
def cli():
    """
    Command Line entry-point for the simulator.
    """
    parser = ArgumentParser(description="Cache/VM Simulator")
    parser.add_argument(
        "-s",
        help = "Cache size in KB",
        type = int,
        choices = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192],
        required = True,
    )
    parser.add_argument(
        "-b",
        help = "Block size in bytes",
        type = int,
        choices = [8, 16, 32, 64],
        required = True,
    )
    parser.add_argument(
        "-a",
        help = "Associativity of the cache",
        type = int,
        choices = [1, 2, 4, 8, 16],
        required = True,
    )
    parser.add_argument(
        "-r",
        help = "Replacement policy - Round Robin or Random",
        type = str.lower,
        choices = ["rr", "rnd"],
        required = True,
    )
    parser.add_argument(
        "-p",
        help = "Physical memory size in MB",
        type = int,
        choices = [128, 256, 512, 1024, 2048, 4096], # 128 MB to 4 GB
        required = True,
    )
    # This argument will have to be checked manually...
    parser.add_argument(
        "-u",
        help = "Percentage of phyiscal memory used by the OS",
        type = float,
        required = True
    )
    parser.add_argument(
        "-n",
        help = "Instructions/Time Slice",
        required = True,
        type = int,
    )
    parser.add_argument(
        "-f",
        help = "Trace file name",
        required = True,
        type = Path,
        action = "append",
    )

    args = parser.parse_args()
    
    # Some manual validation checks before we hit main
    
    # Need 1-3 trace files
    if len(args.f) > 3 or len(args.f) < 1:
        parser.error(f"Expected 1-3 trace files, recieved: {len(args.f)}.")
    
    # System percentage needs to be 0-100
    sys_percent = args.u
    if sys_percent < 0 or sys_percent > 100:
        parser.error("Percentage of physical memory used by the OS must be 0-100")
    
    for file in args.f:
        if not Path(file).is_file():
            parser.error(f"{file} doesn't exist.")
    
    # Cache size must be less than physical memory size
    if args.s*1024 >= args.p*2**20:
        parser.error("Cache size must be less than physical memory size")
    main(
        cache_size = args.s,
        block_size = args.b,
        associativity = args.a,
        replacement_policy = args.r,
        physical_mem_size = args.p,
        phys_mem_used_percent = sys_percent,
        time_slice = args.n,
        trace_files = args.f
    )
    
if __name__ == "__main__":
    cli()