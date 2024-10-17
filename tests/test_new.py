from pprint import pprint
import unittest

from hoi4.plain import strip_down, strip_down_v2, tokenize


class TestStrip(unittest.TestCase):
    def setUp(self):
        with open (r'demo_78.hoi4','r', encoding='utf-8') as f:
            self.filestring = f.read()
            
    def test_strip_down(self):
        f_strip = strip_down(self.filestring)
        f_strip_v2 = strip_down_v2(self.filestring)
        f_token = tokenize(f_strip)
        print(f_token[:10])
        fv2_token = tokenize(f_strip_v2)
        print(fv2_token[:10])

        self.assertEqual(fv2_token ,f_token)
        

if __name__ == '__main__':
    unittest.main()