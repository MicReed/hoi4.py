import os
import unittest
import pandas as pd
import datetime
from extract_hoi4.cal_prod import cal_line_output


class TestCalProd(unittest.TestCase):
    # def test_cal_line_output(self):
    #     true_date = '1936_02_01'
    #     test_date = cal_line_output(0.2, 0.1113699, days = 60)
    #     print(test_date)
    #     f_true_date = datetime.datetime.strptime(true_date, '%Y_%m_%d')
    #     self.assertEqual(f_true_date, test_date)

    pass


if __name__ == '__main__':
    # Print the current working directory
    cur_dir = os.getcwd()
    print("Current working directory:", cur_dir)
    unittest.main()
