
from milestone2 import VMSim, Process, page_table_entries
from collections import deque

# Create a process without needing a trace file
process = Process.__new__(Process)
process.pid = 0
process.name = "test.trc"
process.page_table = [None] * page_table_entries

# Simulate 3 allocated physical pages
process.page_table[10] = 5
process.page_table[20] = 6
process.page_table[30] = 7

# Create a simulator without loading trace files
sim = VMSim.__new__(VMSim)
sim.entry_bits = 19
sim.free_pool = [0, 1, 2]
sim.used_pages = {
    0: deque([(5, 10), (6, 20), (7, 30)])
}
sim.trace_results = []

# Run cleanup
sim.cleanup(process)

# Test 1: Physical pages returned
assert len(sim.free_pool) == 6
assert all(page in sim.free_pool for page in [5, 6, 7])
print("Test 1 PASSED - Physical pages freed")

# Test 2: Page mappings removed
assert all(process.page_table[vpn] is None for vpn in [10, 20, 30])
print("Test 2 PASSED - Page mappings cleared")

# Test 3: Used pages cleared
assert len(sim.used_pages[0]) == 0
print("Test 3 PASSED - Used pages cleared")

# Test 4: Statistics recorded
assert len(sim.trace_results) == 1
assert sim.trace_results[0]["used_page_table_entries"] == 3
assert sim.trace_results[0]["pid"] == 0
print("Test 4 PASSED - Statistics saved")

# Test 5: Calculations correct
expected_percent = (3 / page_table_entries) * 100
expected_wasted = ((page_table_entries - 3) * 19) // 8

assert sim.trace_results[0]["percent_used"] == expected_percent
assert sim.trace_results[0]["wasted"] == expected_wasted
print("Test 5 PASSED - Calculations correct")

print("\nALL CLEANUP TESTS PASSED!")
