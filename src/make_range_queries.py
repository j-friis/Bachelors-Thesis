import numpy as np
import pandas as pd
from psql_functions import execQuery


np.random.seed(42)

from sample_range_query import sample_range_query

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
hh_degrees = np.array([2,3,4])

n_queries = 2500

#[100 196 256 324 400 484]
#[ 256, 324, 400, 484]
#[44,400,450,512]
hh_degree_2 = np.array([44, 324, 400, 484])
#[ 96 150 216 216 294 294]
#[ 216, 216, 294, 294]
#[230,300,500,800]
hh_degree_3 = np.array([ 216, 216, 294, 294])
#[ 72 128 128 200 200 288]
#[ 128, 200, 200, 288]
#[200,300,300,350]
hh_degree_4 = np.array([ 128, 200, 200, 288])

flat_degree_2 = np.array([4, 7, 22, 32, 42, 62])
flat_degree_3 = np.array([5, 8, 23, 33, 43, 63])
flat_degree_4 = np.array([6, 9, 24, 35, 44, 64])

query = """select time_ from _775147;"""
result = execQuery(param_dic, query)
dates = [(date[0]) for date in result]

query = """select count_ from _775147;"""
result = execQuery(param_dic, query)

counts = [(count[0]) for count in result]

all_dates = add_missing_dates(dates)
all_counts =  add_missing_counts(counts, dates, all_dates)

for idx, N in enumerate(hh_ns):
    for degree in hh_degrees:
        print(f'N = {N} and degree = {degree}')
        if degree == 2:
            length_array = hh_degree_2
            csv_name = 'range_queries/hh/' + f'hh_N={N}_B={degree}_r={hh_degree_2[idx]}.csv'
        elif degree== 3:
            length_array = hh_degree_3
            csv_name = 'range_queries/hh/' + f'hh_N={N}_B={degree}_r={hh_degree_3[idx]}.csv'
        elif degree== 4:
            length_array = hh_degree_4
            csv_name = 'range_queries/hh/' + f'hh_N={N}_B={degree}_r={hh_degree_4[idx]}.csv'
    
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

print('Range queries for experiments on flat')

flat_r_32 =  np.array([2, 4, 8, 12, 16, 20, 24])
flat_r_128 =  np.array([20, 40, 50, 60, 70, 80, 90])
flat_r_256 =  np.array([40, 60, 80, 100, 140, 200, 220])
flat_r_512 =  np.array([100, 150, 200, 250, 300, 400, 450])
flat_r_1024 =  np.array([200, 300, 400, 500, 600, 800, 900])
flat_r_2048 =  np.array([600, 800, 1000, 1250, 1500, 1700, 1800])

rs =  [flat_r_32, flat_r_128, flat_r_256, flat_r_512, flat_r_1024, flat_r_2048]
n_queries = 2500
for idx, N in enumerate(flat_ns):
    print(f'N = {N}')
    length_array = rs[idx]
    #print(length_array)
    #print(len(length_array))
    
    for idx, r in enumerate(length_array):
        print(f'N = {N} and r = {r}')
        csv_name = 'range_queries/flat_varying_r/' + f'flat_N={N}_r={r}.csv'
        queries = []
        
        for i in range(0, n_queries):
            queries.append(sample_range_query(length_array[idx],all_dates[:N]))
            
        np.savetxt(csv_name, queries, delimiter=';', fmt='%s, %s')

"""
con_ns = np.array([32,128,256,512,1024,2048])
con_degrees = np.array([2,3,4])
n_queries = 5000

con_degree_r = np.array([10, 30, 100, 200, 400, 600])

for idx, N in enumerate(con_ns):
    for degree in con_degrees:
        print(f'N = {N} and degree = {degree}')

        csv_name = 'range_queries/con_obs/' + f'con_obs_N={N}_B={degree}_r={con_degree_r[idx]}.csv'
    
        queries = []

        for i in range(0, n_queries):
            
            queries.append(sample_range_query(con_degree_r[idx],all_dates[:N]))

        np.savetxt(csv_name, queries, delimiter=';', fmt='%s, %s')
"""
