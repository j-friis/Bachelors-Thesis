import unittest

from psql_functions import execQuery, execRangeQuery
from miss_data import add_missing_dates, add_missing_counts
from sample_range_query import load_range_queries_n_split

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

from con_obs import con_obs

class test_con_obs(unittest.TestCase):

    def test_height(self):
        c = con_obs(1.0, 2, data_dates[:32], data_counts[:32])
        self.assertEqual(c.h, 5)

        c = con_obs(1.0, 3, data_dates[:27], data_counts[:27])
        self.assertEqual(c.h, 3)

        c = con_obs(1.0, 4, data_dates[:64], data_counts[:64])
        self.assertEqual(c.h, 3)
    
    def test_padding(self):
            c = con_obs(1.0, 2, data_dates[:28], data_counts[:28])
            self.assertEqual(len(c.all_counts), 32)

            c = con_obs(1.0, 3, data_dates[:20], data_counts[:20])
            self.assertEqual(len(c.all_counts), 27)

            c = con_obs(1.0, 4, data_dates[:64], data_counts[:64])
            self.assertEqual(c.h, 3)
    
    def test_sum_tuple(self):
        self.assertEqual(sum((2, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()
