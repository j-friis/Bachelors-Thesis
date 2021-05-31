import numpy as np
import pandas as pd
from psql_functions import execQuery

from miss_data import add_missing_dates, add_missing_counts

from datetime import timedelta  

param_dic = {
    "host"      : "localhost",
    "database"  : "bachelorBesoeg2014",
    "user"      : "postgres",
    "password"  : "password",
    "port"      : "5432"
}

hh_ns = np.array([256,512,1024,2048])
degrees = np.array([2,3,4])

n_queries = 5000

#[100 196 256 324 400 484]
#[ 256 324 400 484]
hh_degree_2 = np.array([44,400,450,512])
#[ 96 150 216 216 294 294]
#[ 216 216 294 294]
hh_degree_3 = np.array([230,300,500,800])
#[ 72 128 128 200 200 288]
#[ 128 200 200 288]
hh_degree_4 = np.array([200,300,300,350])

flat_degree_2 = np.array([4, 7, 22, 32, 42, 62])
flat_degree_3 = np.array([5, 8, 23, 33, 43, 63])
flat_degree_4 = np.array([6, 9, 24, 35, 44, 64])

def load_range_queries(file):
    return pd.read_csv(file, sep=',',header=None).to_numpy().flatten()

def load_range_queries_n_split(file, n_structures):
    all_queries = pd.read_csv(file, sep='\n',header=None).to_numpy().flatten()
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

query = """select time_ from _775147;"""
result = execQuery(param_dic, query)
dates = [(date[0]) for date in result]

query = """select count_ from _775147;"""
result = execQuery(param_dic, query)

counts = [(count[0]) for count in result]

all_dates = add_missing_dates(dates)
all_counts =  add_missing_counts(counts, dates, all_dates)

for idx, N in enumerate(hh_ns):
    for degree in degrees:
        print(f'N = {N} and degree = {degree}')
        if degree == 2:
            length_array = hh_degree_2
            csv_name = 'range_queries/local_hh/' + f'hh_N={N}_B={degree}_r={hh_degree_2[idx]}.csv'
        elif degree== 3:
            length_array = hh_degree_3
            csv_name = 'range_queries/local_hh/' + f'hh_N={N}_B={degree}_r={hh_degree_3[idx]}.csv'
        elif degree== 4:
            length_array = hh_degree_4
            csv_name = 'range_queries/local_hh/' + f'hh_N={N}_B={degree}_r={hh_degree_4[idx]}.csv'
    
        qurries = []

        for i in range(0, n_queries):
            
            qurries.append(sample_range_query(length_array[idx],all_dates[:N]))

        np.savetxt(csv_name, qurries, delimiter=';', fmt='%s, %s')

flat_ns = np.array([32,128,256,512,1024,2048])

for idx, N in enumerate(flat_ns):
    print(f'N = {N} and degree = {degree}')

    if degree == 2:
        length_array = flat_degree_2
        csv_name = 'range_queries/flat/' + f'flat_N={N}_r={flat_degree_2[idx]}.csv'
    elif degree== 3:
        length_array = flat_degree_3

        csv_name = 'range_queries/flat/' + f'flat_N={N}_r={flat_degree_3[idx]}.csv'
    elif degree== 4:
        length_array = flat_degree_4
        csv_name = 'range_queries/flat/' + f'flat_N={N}_r={flat_degree_4[idx]}.csv'
        
    qurries = []

        
    for i in range(0, n_queries):
            
        qurries.append(sample_range_query(length_array[idx],all_dates[:N]))

    np.savetxt(csv_name, qurries, delimiter=';', fmt='%s, %s')