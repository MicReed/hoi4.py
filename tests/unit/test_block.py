import unittest
import re
import json

from hoi4.plain import strip_down, tokenize
from hoi4.block import Blocks

class TestBlocksDemo78(unittest.TestCase):
    def setUp(self):
        with open (r'demo_78.hoi4','r', encoding='utf-8') as f:
            filestring = f.read()
        # parse_tokens_subclass(filestring)
        f_strip = strip_down(filestring)
        self.f_token = tokenize(f_strip)
        Blocks.set_tokens(self.f_token)
        self.main_block = Blocks('main',0, None)
        self.main_block.parse_tokens()
    
    def test_get_subdict_keys(self):
        correct_keys = ['player_countries', 'mods', 'railway_gun_index', 'industry_organisation_index', 'id_counter_store', 'saved_event_target', 'flags']
        self.assertEqual(list(self.main_block.sub_blocks.keys()), correct_keys)
    
    
class TestBlocksAll(unittest.TestCase):
    def setUp(self):
        save_address = r'demo_my_save_file.hoi4'
        # save_address = r'demo_78.hoi4'
        # save_address = r'demo_60000.hoi4'
        self.output_address = save_address.replace('.hoi4', '_blocks.json')
        
        with open (save_address, 'r', encoding='utf-8') as f:
            filestring = f.read()
        f_strip = strip_down(filestring)
        self.f_token = tokenize(f_strip)
        Blocks.set_tokens(self.f_token)
        self.main_block = Blocks('main',0, None)
        self.main_block.parse_tokens()
    
    def test_all(self):
        with open(self.output_address, 'w') as f:
            json.dump(self.main_block.contents, f, indent=4)
    

if __name__ == '__main__':
    unittest.main()