import numpy as np
import pandas as pd
from scipy.stats import laplace
from datetime import datetime
from datetime import timedelta 

class OLH_flat:
    def __init__(self, epsilon, dates, counts):
        """Setup of the datastructere
        Parameters:
        T (int): The lenght of the stream
        epsilon (float): The height of the full binary tree. 
        dates (Array): The dates of the stream
        counts (Array): The count for each of the dates
        Returns:
        A epsilon differintial datastructe
        """
        
        self.epsilon = epsilon
        self.all_dates = dates
        self.all_counts = counts
        
        if len(dates) < (dates[-1]-dates[0]).days:
            print('here')
            self.all_dates = self.__add_missing_dates(dates)
            self.all_counts = self.__add_missing_counts(counts,dates)
            
        #Make dict for date indexing
        values = np.arange(0,len(self.all_dates))
        zip_iterator = zip(self.all_dates, values)
        self.idx_dict =  dict(zip_iterator)
        
        self.noise_counts = self.__process(self.all_dates, self.all_counts)
        #Check if we are we have missing dates.
        
        self.p = np.exp(self.epsilon)/(np.exp(self.epsilon)+len(self.all_dates)-1)
        self.var = self.OLH_var(self.p, len(self.all_dates))
        
    def __add_missing_dates(self, old_dates):
        """Add missing dates in a list
        Parameters:
        old_dates (list of datetime.date): List of dates that is not countious
        Returns:
        List of countious starting with the first value of 
        """
        start_date = old_dates[0]
        end_date = old_dates[-1]
        all_dates = pd.date_range(start = start_date, end = end_date).to_pydatetime().tolist()
        return [(date.date()) for date in all_dates]
    
    def OLH_var(self, p, N):
        return 4*p*(1-p)/(N*(2*p-1)**2)
    
    def __add_missing_counts(self, old_counts, old_dates):
        """Adds 0 to the list of counts where there was missing dates
        Parameters:
        old_counts (list of int): List counts for each day with 
        old_dates (list of datetime.date): List of dates that is not countious
        Returns:
        List of countious starting with the first value of 
        """
        zip_iterator = zip(old_dates, old_counts)
        missing_dict =  dict(zip_iterator)
        all_counts = np.zeros(len(self.all_dates))
        for i, date in enumerate(self.all_dates):
            val = missing_dict.get(date, 0)
            all_counts[i] = val
            
        return all_counts
    
    def OLH_func(self, x, g):
        if np.random.uniform(0,1) < np.exp(self.epsilon)/(np.exp(self.epsilon)+g-1):
            return x
        else:
            return np.random.randint(low = 0, high = g)
    
    def OLH_aggre(self, count, N, g):
        p = np.exp(self.epsilon)/(np.exp(self.epsilon)+g-1)
        #print(p - 1/g)
        #print(f'p = {p}')
        return (count - (1-p)*N/g) / (p)

    def OLH_answer(self, count, N, g):
        p = np.exp(self.epsilon)/(np.exp(self.epsilon)+g-1)
        #print(p - 1/g)
        #print(f'p = {p}')
        return (count- N/g) / (p)

    def __process(self, dates, counts):
        OLH_count = np.zeros(len(counts))
        D = len(dates)
        
        for idx, count in enumerate(counts):
            for i in range(0,int(count)):
                response = self.OLH_func(idx, D)
                OLH_count[response] = OLH_count[response] + 1
                
        return OLH_count
    
    def answer(self, dates):
        """Calculates the path of index in full binary string

        Parameters:
        dates (tuple of string): Two dates in the format string 2000-12-19. 

        Returns:
        float: The private range count
        """
        N = np.sum(self.noise_counts)
        D = len(self.noise_counts)
        if (len(dates) < 2):
            #There is only one date
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()

            idx = self.idx_dict[date_obj_0]
            noise_count = self.noise_counts[idx]
            return self.OLH_answer(noise_count, N, D)
            
        else:
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()
            date_obj_1 = datetime.strptime(dates[1],'%Y-%m-%d').date()
            idx_0 = self.idx_dict[date_obj_0]
            idx_1 = self.idx_dict[date_obj_1]
            #print(idx_0)
            #print(idx_1)
            #idx_0 is not 0
            noise_sum = 0.0
            for i in range(idx_0, idx_1+1):
                #print(i)
                #print(self.OLH_answer(self.noise_counts[i], N, D))
                noise_sum = noise_sum + self.OLH_aggre(self.noise_counts[i], N, D)
            return noise_sum
    
    def real_answer(self, dates):
        if len(dates) < 2:
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()
            return self.all_counts[self.idx_dict[date_obj_0]]
        else:
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()
            date_obj_1 = datetime.strptime(dates[1],'%Y-%m-%d').date()
            #print(self.all_counts[self.idx_dict[date_obj_0]: self.idx_dict[date_obj_1]+1])
            sum_ = np.sum(self.all_counts[self.idx_dict[date_obj_0]: self.idx_dict[date_obj_1]+1])  
            return sum_ 
"""
query_dates = ('2014-01-02','2014-01-9')
epsilon = 0.7
FLAT_OLH = OLH_flat(epsilon, all_dates[:32], all_counts[:32])
print(FLAT_OLH.answer(query_dates))
print(FLAT_OLH.real_answer(query_dates))
print(FLAT_OLH.noise_counts)
print(FLAT_OLH.var)
"""