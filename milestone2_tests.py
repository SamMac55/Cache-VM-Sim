import unittest
import tempfile, os
from pathlib import Path

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
        

if __name__ == '__main__':
    unittest.main()