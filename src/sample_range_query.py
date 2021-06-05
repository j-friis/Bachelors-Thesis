import numpy as np
import pandas as pd

from datetime import timedelta  


def load_range_queries(path, file):
    return pd.read_csv(path + file, sep=',',header=None).to_numpy().flatten()

def load_range_queries_n_split(path, file, n_structures):
    all_queries = pd.read_csv(path + file, sep='\n',header=None).to_numpy().flatten()
    split_queries = np.array_split(all_queries, n_structures)
    return split_queries

def myfunc_dis(x, b):
    return 2*b*int(np.ceil(np.log(x) / np.log(b)))**2

def sample_range_query(length, dates):
    """
    Samples two dates of with distance of lenght
    """
    while True:
        start_date_idx = np.random.randint((dates[-1]-dates[0]).days+1)
        start_date = dates[start_date_idx]
        end_date = dates[start_date_idx] + timedelta(days=(int(length-1)))
        if dates[-1] > end_date:
            return (str(start_date), str(end_date))
