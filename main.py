from argparse import ArgumentParser
from pathlib import Path

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
        type = str,
        choices = ["rr", "rnd"],
        required = True,
    )
    parser.add_argument(
        "-p",
        help = "Physical memory size in MB",
        type = int,
        choices = [128, 256, 512, 1024, 2048, 4096],
        required = True,
    )
    # This argument will have to be checked manually...
    parser.add_argument(
        "-u",
        help = "Percentage of phyiscal memory used by the OS",
        type = int,
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
        nargs = "+", # so the plus sign means 1 or more, we need to manually check up to three
        required = True,
        type = Path | str
    )

    args = parser.parse_args()
    
if __name__ == "__main__":
    cli()