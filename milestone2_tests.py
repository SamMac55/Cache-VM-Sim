import unittest
import tempfile, os
from milestone2 import VMSim, Process, Instruction, page_table_entries
from collections import deque

from milestone2 import parse_trace_file
class TestParseTraceFile(unittest.TestCase):
    """These are test cases on the parse_trace_file function"""
    def test_parse_creates_valid_instruction(self):
        # NOTE: Used Gemini to remind me how to do the temporary files in unittests
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("EIP (01): 7c81eb33 5e  pop esi\n")
            tmp.write("dstM: 00000000 --------    srcM: 00000000 --------  ")
            temp_file_path = tmp.name

        try:
            self.assertTrue(os.path.exists(temp_file_path))
            
            instructions = parse_trace_file(temp_file_path)
            self.assertEqual(len(instructions), 1)
            
            instruction = instructions[0]
            
            self.assertEqual(instruction.eip_len, 1)
            self.assertEqual(instruction.eip_addr, "7c81eb33")
            self.assertIsNone(instruction.src)
            self.assertIsNone(instruction.dst)
                
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def test_parse_trace_file_with_mult_instructions(self):
        # I know this looks ugly but if i add tabs itll not work right
        fake_file_text = """EIP (07): 7c80976b 8b 84 88 10 0e 00 00  mov eax,[eax+ecx*4+0xe10]
dstM: 7ffdf034 00000000    srcM: 7ffdfe28 5097807c   

EIP (01): 7c809752 55  push ebp
dstM: 00000000 --------    srcM: 00000000 --------  

EIP (03): 7c80975b 8b 4d 08  mov ecx,[ebp+0x8]
dstM: 00000000 --------    srcM: 0012e110 06000000  

"""
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write(fake_file_text)
            
            temp_file_path = tmp.name

        try:
            self.assertTrue(os.path.exists(temp_file_path))
            
            instructions = parse_trace_file(temp_file_path)
            self.assertEqual(len(instructions), 3)
            
            instruction1 = instructions[0]
            self.assertEqual(instruction1.eip_len, 7)
            self.assertEqual(instruction1.eip_addr, "7c80976b")
            self.assertIsNotNone(instruction1.src)
            self.assertEqual(instruction1.src, "7ffdfe28")
            self.assertIsNotNone(instruction1.dst)
            self.assertEqual(instruction1.dst, "7ffdf034")
            
            instruction1 = instructions[1]
            self.assertEqual(instruction1.eip_len, 1)
            self.assertEqual(instruction1.eip_addr, "7c809752")
            self.assertIsNone(instruction1.src)
            self.assertIsNone(instruction1.dst)

            instruction1 = instructions[2]
            self.assertEqual(instruction1.eip_len, 3)
            self.assertEqual(instruction1.eip_addr, "7c80975b")
            self.assertIsNotNone(instruction1.src)
            self.assertEqual(instruction1.src, "0012e110")
            self.assertIsNone(instruction1.dst)
                
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
  
## Gerald made these tests      
class TestCleanup(unittest.TestCase):
    def test_cleanup(self):
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

class TestNextInstructions(unittest.TestCase):
    def test_next_instructions(self):
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
if __name__ == '__main__':
    unittest.main()