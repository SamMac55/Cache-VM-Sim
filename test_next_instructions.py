
from milestone2 import Process, Instruction

# Create a process without needing a trace file
process = Process.__new__(Process)

# Create 7 fake instructions
process.instructions = [
    Instruction(1, f"{i:08x}") for i in range(7)
]
process.instruction_position = 0

# Test batches of 3
assert len(process.next_instructions(3)) == 3
print("Test 1 PASSED")

assert len(process.next_instructions(3)) == 3
print("Test 2 PASSED")

assert len(process.next_instructions(3)) == 1
print("Test 3 PASSED")

assert process.next_instructions(3) == []
assert process.is_finished()
print("Test 4 PASSED")

print("ALL TESTS PASSED!")
