import numpy as np
import pandas as pd
from scipy.stats import laplace
from datetime import datetime
from datetime import timedelta  

class central_flat:
    def __init__(self, epsilon, dates, counts):
        """Setup of the datastructere
        Parameters:
        epsilon (float): The epsilon for differintial privacy
        dates (Array): The dates of the stream
        counts (Array): The count for each of the dates
        Returns:
        A epsilon differintial datastructure
        """
        
        self.epsilon = epsilon
        self.all_dates = dates
        self.all_counts = counts
        
        if len(dates) < (dates[-1]-dates[0]).days:
            self.all_dates = self.__add_missing_dates(dates)
            self.all_counts = self.__add_missing_counts(counts,dates)
            
        #Make dict for date indexing
        values = np.arange(0,len(self.all_dates))
        zip_iterator = zip(self.all_dates, values)
        self.idx_dict =  dict(zip_iterator)
        
        self.noisy_counts = self.__process(self.all_counts)
        
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

    def __process(self, counts):
        N = len(counts)
        laplaces = laplace(scale=1/self.epsilon).rvs(N)
        noise_counts = counts + laplaces
                
        return noise_counts
    
    def answer(self, dates):
        """Calculates the differintial private answear

        Parameters:
        dates (tuple of string): Two dates in the format string 2000-12-19. 

        Returns:
        float: The private range count
        """
        if (len(dates) < 2):
            #There is only one date
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()

            idx = self.idx_dict[date_obj_0]
            noise_count = self.noisy_counts[idx]
            return noise_count
            
        else:
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()
            date_obj_1 = datetime.strptime(dates[1],'%Y-%m-%d').date()

            noise_sum = np.sum(self.noisy_counts[self.idx_dict[date_obj_0]: self.idx_dict[date_obj_1]+1])  
            return noise_sum
    
    def real_answer(self, dates):
        """Calculates the real answer to a range query

        Parameters:
        dates (tuple of string): Two dates in the format string 2000-12-19. 

        Returns:
        float: The real range count
        """
        if len(dates) < 2:
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()
            return self.all_counts[self.idx_dict[date_obj_0]]
        else:
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()
            date_obj_1 = datetime.strptime(dates[1],'%Y-%m-%d').date()
            sum_ = np.sum(self.all_counts[self.idx_dict[date_obj_0]: self.idx_dict[date_obj_1]+1])  
            return sum_ 


