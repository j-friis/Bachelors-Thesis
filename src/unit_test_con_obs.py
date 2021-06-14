import unittest

import numpy as np
import pandas as pd

from datetime import date
from datetime import timedelta  

today = date.today()

start_date = today
all_dates = pd.date_range(start = start_date, periods = 512).to_pydatetime().tolist()
data_dates =  [(date.date()) for date in all_dates]
data_counts = np.ones(512)

from con_obs import con_obs

class test_con_obs(unittest.TestCase):

    def test_height(self):
        model = con_obs(1.0, 2, data_dates[:32], data_counts[:32])
        self.assertEqual(model.h, 5)

        model = con_obs(1.0, 3, data_dates[:27], data_counts[:27])
        self.assertEqual(model.h, 3)

        model = con_obs(1.0, 4, data_dates[:64], data_counts[:64])
        self.assertEqual(model.h, 3)
    
    def test_padding(self):
            model = con_obs(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(len(model.all_counts), 32)

            model = con_obs(1.0, 3, data_dates[:20], data_counts[:20])
            self.assertEqual(len(model.all_counts), 27)

            model = con_obs(1.0, 4, data_dates[:64], data_counts[:64])
            self.assertEqual(model.h, 3)
    
    def test_tree_lengths(self):
            model = con_obs(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(len(model.tree_levels[0]), 1)
            self.assertEqual(len(model.tree_levels[1]), 2)
            self.assertEqual(len(model.tree_levels[2]), 4)
            self.assertEqual(len(model.tree_levels[3]), 8)
            self.assertEqual(len(model.tree_levels[4]), 16)
            self.assertEqual(len(model.tree_levels[5]), 32)

            model = con_obs(1.0, 3, data_dates[:28], data_counts[:28])
            self.assertEqual(len(model.tree_levels[0]), 1)
            self.assertEqual(len(model.tree_levels[1]), 3)
            self.assertEqual(len(model.tree_levels[2]), 9)
            self.assertEqual(len(model.tree_levels[3]), 27)

            model = con_obs(1.0, 4, data_dates[:60], data_counts[:60])
            self.assertEqual(len(model.tree_levels[0]), 1)
            self.assertEqual(len(model.tree_levels[1]), 4)
            self.assertEqual(len(model.tree_levels[2]), 16)
            self.assertEqual(len(model.tree_levels[3]), 64)

    def test_histogram(self):
            model = con_obs(1.0, 2, data_dates[:32], data_counts[:32] )
            self.assertEqual(sum(model.histogram[0]), 32)
            self.assertEqual(sum(model.histogram[1]), 32)
            self.assertEqual(sum(model.histogram[2]), 32)
            self.assertEqual(sum(model.histogram[3]), 32)
            self.assertEqual(sum(model.histogram[4]), 32)
            self.assertEqual(sum(model.histogram[5]), 32)
            
            self.assertTrue((model.histogram[0] == [32]))
            self.assertTrue((model.histogram[1] == [16,16]))
            self.assertTrue((model.histogram[2] == [8,8,8,8]))
            self.assertTrue((model.histogram[3] == [4,4,4,4,4,4,4,4]))
            self.assertTrue((model.histogram[4] == [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]))
            self.assertTrue((model.histogram[5] == [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]))


            model = con_obs(1.0, 3, data_dates[:28], data_counts[:28])
            self.assertEqual(len(model.tree_levels[0]), 1)
            self.assertEqual(len(model.tree_levels[1]), 3)
            self.assertEqual(len(model.tree_levels[2]), 9)
            self.assertEqual(len(model.tree_levels[3]), 27)

            model = con_obs(1.0, 4, data_dates[:60], data_counts[:60])
            self.assertEqual(len(model.tree_levels[0]), 1)
            self.assertEqual(len(model.tree_levels[1]), 4)
            self.assertEqual(len(model.tree_levels[2]), 16)
            self.assertEqual(len(model.tree_levels[3]), 64)


    def test_get_index(self):
            model = con_obs(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(model.get_index(0,4), [0,0,0,0,0,0])
            self.assertEqual(model.get_index(31,4), [31,15,7,3,1,0])

            #with self.assertRaises(IndexError): model.get_index(44,4)

            model = con_obs(1.0, 3, data_dates[:20], data_counts[:20])
            self.assertEqual(model.get_index(0,4), [0,0,0,0])
            self.assertEqual(model.get_index(20,4), [20,6,2,0])

            model = con_obs(1.0, 4, data_dates[:64], data_counts[:64])
            self.assertEqual(model.get_index(0,3), [0,0,0,0])
            self.assertEqual(model.get_index(63,4), [63,15,3,0])

    def test_turns_left(self):
            model = con_obs(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(model.turns_left([0,0,0,0,0,0]), [1,1,1,1,1])
            self.assertEqual(model.turns_left([31,15,7,3,1,0]), [0,0,0,0,1])
    
    def test_turns_right(self):
            model = con_obs(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(model.turns_right([0,0,0,0,0,0]), [0,0,0,0,0])
            self.assertEqual(model.turns_right([31,15,7,3,1,0]), [0,0,0,0,0])

    def test_get_group(self):
            model = con_obs(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(model.get_group(0,0), 0)
            self.assertEqual(model.get_group(1,0), 1)

            self.assertTrue((model.get_group(0,5) == [0,1]).all())

            model = con_obs(1.0, 4, data_dates[:64], data_counts[:64])
            self.assertEqual(model.get_group(0,0), 0)
            self.assertEqual(model.get_group(1,0), 1)

            self.assertTrue((model.get_group(1,1) == [0,1,2,3]).all())

    def test_real_answer(self):
            model = con_obs(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertAlmostEqual(model.real_answer((str(today),str(today+ timedelta(days=1) ))), 2)
            

if __name__ == '__main__':
    unittest.main()
