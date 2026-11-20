"""
AI Disclosure
1. Samantha asked Claude if the setup for the code skeleton smelled right.
"""
import math
import random

class Cache:
    def __init__(
        self,
        total_blocks: int,
        rows: int,
        associativity: int,
        index_bits: int,
        tag_bits: int,
        block_size: int,
        overhead_size: int,
        eviction_policy: str, #either rr or r
    ):
        self.total_blocks = total_blocks
        self.rows = rows
        self.associativity = associativity
        self.index_bits = index_bits
        self.tag_bits = tag_bits
        self.block_size = block_size
        self.offset_bits = int(math.log2(block_size))
        self.overhead_per_block = overhead_size / total_blocks
        
        # Since we don't actually care about the data in the cache, we will just store the tag in it
        self.cache = [[None] * self.associativity for _ in range(self.rows)]
        
        # If we do round robin, we need a pointer to which column is the next in line
        # for eviction
        self.round_robin = [0] * self.rows
        
        # we can consider adding random later dw aboout it rn
        
        self.clock_cycles = 0
        self.hits = 0
        self.compulsory_misses = 0
        self.conflict_misses = 0
        
        # need this for the averages later.
        self.num_row_accesses = 0
        self.src_bytes_read = 0
        self.dst_bytes_read = 0
        self.inst_bytes_read = 0
        self.total_addresses = 0
    
    def process_addr(self, physical_addr: int, inst_type: str, bytes: int = 4):
        """I set the bytes=4 because all data access are four bytes so we will use it as a default"""
        # TODO: call split address to split the physical address into tag, index, and offset
        # aka: tag, index, offset = split_address(physical_addr)
        # define processing_penalty as 2 if inst_type "inst" else 1
        # clock_cycles += processing_penalty
        # if inst_type == src: src_bytes_read += bytes
        # if inst_type == "dst": dst_bytes_read += bytes
        # if inst_type == 'inst': inst_bytes_read += bytes
        # self.total_addresses += 1
        
        # define success as False so we know if we mapped or not at loop conclusion
        
        # calculate how many rows are are touching by taking the block offset + the bytes read
        # and put them in a rows array
        
        #self.num_row_accesses += len(rows array)
        
        # for loop for row in rows
            # For loop for col in range(associativity)
                # look for cache_val = self.cache[index][col]
                # if cache_val aka the tag == tag:
                    # hit +=1
                    # clock cycles +=  1
                    # success = true
                    #  break (becaues we hit so we don't need to keep checking)
                
                # if not success: (this means we had a miss rip)
                    # look for a column that has a None value, if this exists
                        # Map the tag to this spot and count it as compulsory miss so:
                        # compulsory_miss += 1
                        # clock_cycles += (4 * ciel( blocksize/4) )
                    # otherwise conflict miss
                        # replace the tag at self.cache[index][self.round_robin[index]] with current tag
                        # increment self.round_robin[index] (but keep it in range 0-associativity-1 (hint use a %))
                        # clock cycles += (4*ciel(blocksize/4))
                        # increment self.conflict_misses
        
        pass
    
    def split_address(self, physical_addr: int):
        #TODO: I suggest looking up how to use bit masking and shifting to split the address
        # Add this to the AI disclosure
        
        # return tag, index, offset
        pass
    
    def retrieve_rows_touched(self, physical_addr: int, bytes: int):
        """Idk how to explain this one but basically you figure out what the first block 
        is by getting rid of offset bits, then figure out the last address by adding it to bytes-1
        and removing offset bits. Then rows = last-first+1
        create a list and iterate from first block to last block+ 1 to find the address
        I suggest looking this one up to make sure im right just put in AI disclosure"""
        pass
        
    def calc_CPI(self, num_instructions: int):
        """this should literally just be self.clock_cycles/num_instructions"""
        pass
        
    def invalidate_blocks(self, physical_page: int, page_size: int):
        #TODO: caluclate where the page starts by doing phys_page * page_size
        #TODO find the number of blocks that the page covers by doign the page size / block size
        
        #TODO: loop over the range(number of blocks page covers)
        # TODO: calculate the block, index, and tag
        # TODO: look over the cache columns to set row[index][col] to None if the tag matches
        pass
    
    def get_hit_rate(self):
        # TODO return self.hits * 100 / self.num_row_accesses
        pass
    
    def get_miss_rate(self):
        # TODO return 100- get_hit_rate
        pass
    
    def count_unused_blocks(self):
        return sum(1 for row in self.cache for tag in row if tag is None)
    
    def get_unused_kb(self):
        # TODO: return self.count_unused_blocks() * (self.block_size + self.overhead_per_block) / 1024
        pass
    
    def get_unused_blocks(self):
        # todo return self.count_unused_blocks() / self.total_blocks
        pass