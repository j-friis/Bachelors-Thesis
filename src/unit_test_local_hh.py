import unittest

from psql_functions import execQuery
from miss_data import add_missing_dates, add_missing_counts

param_dic = {
    "host"      : "localhost",
    "database"  : "bachelorBesoeg2014",
    "user"      : "postgres",
    "password"  : "password",
    "port"      : "5432"
}

query = """select time_ from _775147;"""
result = execQuery(param_dic, query)
dates = [(date[0]) for date in result]

query = """select count_ from _775147;"""
result = execQuery(param_dic, query)

counts = [(count[0]) for count in result]

data_dates = add_missing_dates(dates)
data_counts =  add_missing_counts(counts, dates, data_dates)

from local_hh import HH_OLH

class test_con_obs(unittest.TestCase):

    def test_height(self):
        model = HH_OLH(1.0, 2, data_dates[:32], data_counts[:32])
        self.assertEqual(model.h, 5)

        model = HH_OLH(1.0, 3, data_dates[:27], data_counts[:27])
        self.assertEqual(model.h, 3)

        model = HH_OLH(1.0, 4, data_dates[:64], data_counts[:64])
        self.assertEqual(model.h, 3)
    
    def test_tree_lengths(self):
            model = HH_OLH(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(len(model.tree_levels[0]), 1)
            self.assertEqual(len(model.tree_levels[1]), 2)
            self.assertEqual(len(model.tree_levels[2]), 4)
            self.assertEqual(len(model.tree_levels[3]), 8)
            self.assertEqual(len(model.tree_levels[4]), 16)
            self.assertEqual(len(model.tree_levels[5]), 32)

            model = HH_OLH(1.0, 3, data_dates[:28], data_counts[:28])
            self.assertEqual(len(model.tree_levels[0]), 1)
            self.assertEqual(len(model.tree_levels[1]), 3)
            self.assertEqual(len(model.tree_levels[2]), 9)
            self.assertEqual(len(model.tree_levels[3]), 27)

            model = HH_OLH(1.0, 4, data_dates[:64], data_counts[:64])
            self.assertEqual(len(model.tree_levels[0]), 1)
            self.assertEqual(len(model.tree_levels[1]), 4)
            self.assertEqual(len(model.tree_levels[2]), 16)
            self.assertEqual(len(model.tree_levels[3]), 64)

    def test_get_index(self):
            model = HH_OLH(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(model.get_index(0,4), [0,0,0,0,0,0])
            self.assertEqual(model.get_index(31,4), [31,15,7,3,1,0])

            #with self.assertRaises(IndexError): model.get_index(44,4)

            model = HH_OLH(1.0, 3, data_dates[:20], data_counts[:20])
            self.assertEqual(model.get_index(0,4), [0,0,0,0])
            self.assertEqual(model.get_index(20,4), [20,6,2,0])

            model = HH_OLH(1.0, 4, data_dates[:64], data_counts[:64])
            self.assertEqual(model.get_index(0,3), [0,0,0,0])
            self.assertEqual(model.get_index(63,4), [63,15,3,0])

    def test_turns_left(self):
            model = HH_OLH(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(model.turns_left([0,0,0,0,0,0]), [1,1,1,1,1])
            self.assertEqual(model.turns_left([31,15,7,3,1,0]), [0,0,0,0,1])
    
    def test_turns_right(self):
            model = HH_OLH(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(model.turns_right([0,0,0,0,0,0]), [0,0,0,0,0])
            self.assertEqual(model.turns_right([31,15,7,3,1,0]), [0,0,0,0,0])

    def test_get_group(self):
            model = HH_OLH(1.0, 4, data_dates[:28], data_counts[:28])
            self.assertEqual(model.get_group(0,0), 0)
            self.assertEqual(model.get_group(1,0), 1)
            self.assertTrue((model.get_group(1,1) == [0,1,2,3]).all())

    def test_real_answer(self):
            model = HH_OLH(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertAlmostEqual(model.real_answer(('2014-01-2','2014-1-2')), 239.0)



if __name__ == '__main__':
    unittest.main()
