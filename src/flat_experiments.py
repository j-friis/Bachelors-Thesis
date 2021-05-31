import re
import numpy as np
import pandas as pd

from psql_functions import execQuery
from miss_data import add_missing_dates, add_missing_counts
from sample_range_query import load_range_queries_n_split
from flat_olh import OLH_flat
import os
owd = os.getcwd()


def model_answers(model, query):
    estimation = model.answer(query)
    correct = model.real_answer(query)  
    return estimation, correct

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

all_dates = add_missing_dates(dates)
all_counts =  add_missing_counts(counts, dates, all_dates)

epsilons = np.array([2,1.4,1.2,1,0.8,0.6,0.5,0.3])
n = np.array([32,128,256,512,1024,2048])

os.chdir(os.getcwd()+'/'+'range_queries/flat/')
os.getcwd()

#We have 50 datastruces
n_data_structures = 50

epsilons = np.array([2,1.4,1.2,1,0.8,0.6,0.5,0.3])
n = np.array([32,128,256,512,1024,2048])
degrees = np.array([2,3,4])
os.chdir(owd)
#We have 50 datastruces

#This is a list of array of array [[[],[],[],[]]]
    
os.getcwd()
os.chdir(os.getcwd()+'/'+'range_queries/flat')
files = [f for f in os.listdir('.') if re.match(r'.*\.csv', f)]

n_32_flat = []
n_128_flat = []
n_256_flat = []
n_512_flat = []
n_1024_flat = []
n_2048_flat = []

for f in files:
    if 'N=32' in f:
        n_32_flat.append(load_range_queries_n_split(f, n_data_structures))
    if 'N=128' in f:
        n_128_flat.append(load_range_queries_n_split(f, n_data_structures))
    if 'N=256' in f:
        n_256_flat.append(load_range_queries_n_split(f, n_data_structures))
    if 'N=512' in f:
        n_512_flat.append(load_range_queries_n_split(f, n_data_structures))
    if 'N=1024' in f:
        n_1024_flat.append(load_range_queries_n_split(f, n_data_structures))
    if 'N=2048' in f:
        n_2048_flat.append(load_range_queries_n_split(f, n_data_structures))

n_32_flat = [item for sublist in n_32_flat for item in sublist]
n_128_flat = [item for sublist in n_128_flat for item in sublist]
n_256_flat = [item for sublist in n_256_flat for item in sublist]
n_512_flat = [item for sublist in n_512_flat for item in sublist]
n_1024_flat = [item for sublist in n_1024_flat for item in sublist]
n_2048_flat = [item for sublist in n_2048_flat for item in sublist]

#Load querys where 
os.chdir(owd)
os.chdir(os.getcwd()+'/'+'range_queries/local_hh')
files = [f for f in os.listdir('.') if re.match(r'.*\.csv', f)]


#This is a list of array of array [[[],[],[],[]]]
n_256_hh = []
n_512_hh = []
n_1024_hh = []
n_2048_hh = []

for f in files:
    if 'N=256' in f:
        n_256_hh.append(load_range_queries_n_split(f, n_data_structures))
    if 'N=512' in f:
        n_512_hh.append(load_range_queries_n_split(f, n_data_structures))
    if 'N=1024' in f:
        n_1024_hh.append(load_range_queries_n_split(f, n_data_structures))
    if 'N=2048' in f:
        n_2048_hh.append(load_range_queries_n_split(f, n_data_structures))

#Flatten so we get [[],[],[],[]]
n_256_hh = [item for sublist in n_256_hh for item in sublist]
n_512_hh = [item for sublist in n_512_hh for item in sublist]
n_1024_hh = [item for sublist in n_1024_hh for item in sublist]
n_2048_hh = [item for sublist in n_2048_hh for item in sublist]


for e in epsilons:
    for N in n:
        for degree in degrees:
            csv_name_est_flat = 'results/sample_querys/flat/' + f'est_flat_queries_e={e}_N={N}_B={degree}.csv'
            csv_name_cor_flat = 'results/sample_querys/flat/' + f'cor_flat_queries_e={e}_N={N}_B={degree}.csv'
        
            csv_name_est_hh = 'results/sample_querys/flat/' + f'est_hh_queries_e={e}_N={N}_B={degree}.csv'
            csv_name_cor_hh = 'results/sample_querys/flat/' + f'cor_hh_queries_e={e}_N={N}_B={degree}.csv'
        
            answers_flat = []
            correct_answers_flat = []
        
            answers_hh = []
            correct_answers_hh = []

            for i in range(0,n_data_structures):
                """
                degree = 4
                local_HH = HH_OLH_degree(epsilon, degree, all_dates[:], all_counts[:])
                """
                FLAT_OLH = OLH_flat(e, all_dates[:N], all_counts[:N])

                if N == 32:
                    for query in n_32_flat[i]:
                        dates_split = query.split(', ')
                        res = tuple(dates_split)

                        est, cor = model_answers(FLAT_OLH, res)
                        answers_flat.append(est)
                        correct_answers_flat.append(cor)

                if N == 128:
                    for query in n_128_flat[i]:

                        dates_split = query.split(', ')
                        res = tuple(dates_split)

                        est, cor = model_answers(FLAT_OLH, res)
                        answers_flat.append(est)
                        correct_answers_flat.append(cor)


                if N == 256:
                    for query in n_32_flat[i]:
                        dates_split = query.split(', ')
                        res = tuple(dates_split)
                        est, cor = model_answers(FLAT_OLH, res)
                        answers_flat.append(est)
                        correct_answers_flat.append(cor)             

                if N == 512:
                    for query in n_512_flat[i]:
                        dates_split = query.split(', ')
                        res = tuple(dates_split)

                        est, cor = model_answers(FLAT_OLH, res)
                        answers_flat.append(est)
                        correct_answers_flat.append(cor)

                    for query in n_512_hh[i]:
                        dates_split = query.split(', ')
                        res = tuple(dates_split)

                        est, cor = model_answers(FLAT_OLH, res)
                        answers_hh.append(est)
                        correct_answers_hh.append(cor)

                if N == 1024:
                    for query in n_1024_flat[i]:
                        dates_split = query.split(', ')
                        res = tuple(dates_split)

                        est, cor = model_answers(FLAT_OLH, res)
                        answers_flat.append(est)
                        correct_answers_flat.append(cor)

                    for query in n_1024_hh[i]:
                        dates_split = query.split(', ')
                        res = tuple(dates_split)
                        est, cor = model_answers(FLAT_OLH, res)
                        answers_hh.append(est)
                        correct_answers_hh.append(cor)

                if N == 2048:
                    for query in n_2048_flat[i]:
                        dates_split = query.split(', ')
                        res = tuple(dates_split)

                        est, cor = model_answers(FLAT_OLH, res)
                        answers_flat.append(est)
                        correct_answers_flat.append(cor)

                    for query in n_2048_hh[i]:
                        dates_split = query.split(', ')
                        res = tuple(dates_split)

                        est, cor = model_answers(FLAT_OLH, res)
                        answers_hh.append(est)
                        correct_answers_hh.append(cor)


                        
            np.savetxt(csv_name_est_flat, answers_flat, delimiter=',')
            np.savetxt(csv_name_cor_flat, correct_answers_flat, delimiter=',')

            np.savetxt(csv_name_est_hh, answers_hh, delimiter=',')
            np.savetxt(csv_name_cor_hh, correct_answers_hh, delimiter=',')
        