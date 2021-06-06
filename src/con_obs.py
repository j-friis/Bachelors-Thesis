import numpy as np
import pandas as pd
from scipy.stats import laplace
from datetime import datetime

class cen_hh:
    
    def __init__(self, epsilon, dates, counts, degree):
        """Setup of the datastructere

        Parameters:
        T (int): The lenght of the stream
        epsilon (float): The height of the full binary tree. 
        dates (Array): The dates of the stream
        counts (Array): The count for each of the dates
        Returns:
        A epsilon differintial datastructe
        """
        
        self.degree = degree
        
        self.all_dates = dates
        self.all_counts = counts
        #Check if we are we have missing dates.
        if len(dates) < (dates[-1]-dates[0]).days:  
            self.all_dates = self.__add_missing_dates(dates)
            self.all_counts = self.__add_missing_counts(counts,dates)
        
        self.all_dates = self.pad_dates(dates)
        self.all_counts = self.pad_counts(counts)
        
        #Make dict for date indexing
        values = np.arange(0,len(self.all_dates))
        zip_iterator = zip(self.all_dates, values)
        self.idx_dict =  dict(zip_iterator)
        
        # We need the stream to be a power of the degree
        self.T = int(np.ceil(np.log(len(self.all_counts)) / np.log(self.degree))+1)
        self.epsilon = epsilon
        self.zeta = (np.log2(self.T))/epsilon
            
        # The height of the "adic tree"
        self.n_layers = int(np.log(self.T)/np.log(self.degree))
        
        # Get laplace for each node
        self.laplaces = self.init_laplace()
        self.histogram = self.build_histogram(self.all_counts)
        self.tree_levels = self.__process(self.all_counts)
    
    def init_laplace(self):
        """
        returns: list of arrays with the correct size of laplaces variabels.
        """
        laplaces = []
        for i in np.arange(0,self.T):
            rvs = laplace(scale=self.zeta).rvs(int(self.degree**np.ceil(i)))
            laplaces.append(rvs)
        
        return laplaces
    
    def build_histogram(self, counts):
        #print(counts)
        #print(get_group(counts,degree))
        tree = []
        left = counts
        for level in range(0, int(np.ceil(np.log(len(counts)) / np.log(self.degree)))):
            split_ratio = self.degree**level
            left = np.array_split(counts, split_ratio)

            sums = [np.sum(a) for a in left]
            tree.append(sums)
                     
        tree.append(counts)
        return tree   
        
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
    
    def pad_counts(self, counts):
        levels = int(np.ceil(np.log(len(counts)) / np.log(self.degree)))

        n_missing_counts =  self.degree**levels -len(counts)

        missing = np.zeros(n_missing_counts, dtype=int)
        new_counts = np.concatenate((counts,missing))
        return new_counts

    def pad_dates(self, dates):
        levels = int(np.ceil(np.log(len(dates)) / np.log(self.degree)))
        n_missing_dates =  self.degree**levels - len(dates)

        start_date = datetime.strptime(str(dates[-1]),'%Y-%m-%d').date()
        result = pd.date_range(start = start_date, periods = n_missing_dates).to_pydatetime().tolist()

        new_dates = np.concatenate((dates,result))
        return new_dates
    
    def __process(self, counts):
        hh = []
        for i in range(0,len(self.laplaces)):
            level = self.laplaces[i] + self.histogram[i]
            hh.append(level)
        return hh  
    
    def get_index(self, date_idx, n_layers):
        """Calculates the path of index in full binary string

        Parameters:
        date_idx (int): The node in the bouttom layer we want to calculate a path to. 
        The bottom layer has index from 0 to 2**h-1
        n_layers (int): The height of the full binary tree. 

        Returns:
        list: of index in the path from the starting from the bottom and going up
        """
        idx = []
        for i in np.arange(0,n_layers):
            if i == 0:
                idx.append(int(date_idx))
            else:
                idx.append(int(idx[i-1]//2))
        idx.append(0)
        return idx
    
    def get_group(self, idx, level):
        """Calculates the path of index in full binary string

        Parameters:
        date_idx (int): The node in the bouttom layer we want to calculate a path to. 
        The bottom layer has index from 0 to 2**h-1
        n_layers (int): The height of the full binary tree. 0 index

        Returns:
        list: of index in the path from the starting from the bottom and going up

        """
        if level == 0:
            return 0
        else:
            group_index = idx //self.degree
            level_indicis = np.arange(0,self.degree**level)

            split_ratio = (len(level_indicis) // self.degree)
            level_indicis_split = np.array_split(level_indicis, split_ratio)

            return level_indicis_split[group_index]
    
    def turns_right(self, path):
        #0 is left 1 is right
        direction_lst = []
        for i in range(len(path)-1):
            current = path[i]
            nxt = path[i+1]
            if nxt == 0:
                #We went left
                direction_lst.append(0)
            elif current == 0 and current < nxt:
                #We went right
                direction_lst.append(1)
            elif self.degree * current < nxt:
                #We went right
                direction_lst.append(1)
            else:
                #print('else')            
                direction_lst.append(0)

        return direction_lst

    def turns_left(self, path):
        #0 is left 1 is right
        direction_lst = []
        for i in range(len(path)-1):
            current = path[i]
            nxt = path[i+1]
            #Checks
            if nxt == 0:
                #We went left
                direction_lst.append(0)
            #Checks
            elif nxt == current*self.degree + self.degree - 1:
                #We went right
                direction_lst.append(1)
            elif current == 0 and current < nxt:
                #We went left
                direction_lst.append(0)
            else:
                direction_lst.append(0)

        return direction_lst
    
    def answer(self, dates):
        """Calculates the path of index in full binary string

        Parameters:
        dates (tuple of string): Two dates in the format string 2000-12-19. 

        Returns:
        float: The private range count
        """
        print('_____________')
        print(dates)
        print(type(dates))
        
        date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()
        date_obj_1 = datetime.strptime(dates[1],'%Y-%m-%d').date()


        idx_0 = self.idx_dict[date_obj_0]
        idx_1 = self.idx_dict[date_obj_1]
        
        #print(idx_0)
        #print(idx_1)
        idx_left = idx_0-1
        idx_right = idx_1+1
        
        path_to_left = np.flip(np.array(self.get_index(idx_left,self.T)))
        path_to_right = np.flip(np.array(self.get_index(idx_right,self.T)))
        
        left_or_right_list_leftside = self.turns_left(path_to_left)
        left_or_right_list_rightside = self.turns_right(path_to_right)
        #Starting in 0
        
        range_count = 0.0
        
        if idx_0 == 0 and idx_1 == np.max(np.fromiter(self.idx_dict.values(), dtype = int)):
            node = self.tree_levels[0]
            range_count = node
            
        elif idx_0 == 0:
            level_offset = 1
            #print(f'level_offset = {level_offset}')

            for i in range(len(left_or_right_list_rightside)):
                if left_or_right_list_rightside[i] == 1:
                    group = self.get_group(path_to_right[i+level_offset], i+level_offset)
                    idx_sss = np.where(group == path_to_right[i+level_offset])[0][0]

                    count_nodes = self.tree_levels[i+level_offset][group[:idx_sss]]
                    for node in count_nodes:
                        #print(node)
                        range_count = range_count + node
    
        elif idx_1 == np.max(np.fromiter(self.idx_dict.values(), dtype = int)):
            #print('MAX')
            
            level_offset = 1
            #print(f'level_offset = {level_offset}')

            for i in range(len(left_or_right_list_leftside)):
                if left_or_right_list_leftside[i] == 0:

                    group = self.get_group(path_to_left[i+level_offset], i+level_offset)
                    idx_sss = np.where(group == path_to_left[i+level_offset])[0][0]

                    count_nodes = self.tree_levels[i+level_offset][group[idx_sss+1:]]
                    for node in count_nodes:
                        #print(node)
                        range_count = range_count + node
                    
                    
        else:
            level_offset = 1
            #print(f'level_offset = {level_offset}')
            left_count = []
            left_count_group = []

            for i in range(len(left_or_right_list_rightside)):
                if left_or_right_list_rightside[i] == 1:
                    group = self.get_group(path_to_right[i+level_offset], i+level_offset)
                    idx_sss = np.where(group == path_to_right[i+level_offset])[0][0]

                    left_count_group.append(group[:idx_sss]) 

                    count_nodes = self.tree_levels[i+level_offset][group[:idx_sss]]
                    left_count.append(count_nodes)

                else:
                    left_count_group.append(np.array([]))
                    left_count.append(np.array([]))

            #The search right side
            right_count = []
            right_count_group = []

            for i in range(len(left_or_right_list_leftside)):
                if left_or_right_list_leftside[i] == 0:

                    group = self.get_group(path_to_left[i+level_offset], i+level_offset)
                    idx_sss = np.where(group == path_to_left[i+level_offset])[0][0]

                    right_count_group.append(group[idx_sss+1:]) 

                    count_nodes = self.tree_levels[i+level_offset][group[idx_sss+1:]]
                    right_count.append(count_nodes)

                else:
                    right_count_group.append(np.array([]))
                    right_count.append(np.array([]))

            #print('Counting nodes')
            #print(left_count)
            #print(right_count)
            for i in range(len(left_count_group)):
                #print(f'At level {level_offset + i}')
                """
                print('Left size')
                print(left_count_group[i].size)
                print('right size')
                print(right_count_group[i].size)
                """
                if left_count_group[i].size != 0 and right_count_group[i].size != 0:
                    #print('Both not zero')
                    group_left = self.get_group(left_count_group[i][0], i+ level_offset)
                    group_right = self.get_group(right_count_group[i][0], i+ level_offset)

                    if not (np.array_equal(group_left,group_right)):
                        for node in left_count_group[i]:
                            range_count = range_count + node
                            #print(node)
                        for node in right_count_group[i]:
                            range_count = range_count +node
                            #print(node)
                    else:
                        #print(left_count_group[i])
                        #print(right_count_group[i])
                        #print(np.intersect1d(left_count_group[i], right_count_group[i]))
                        count_nodes = np.intersect1d(left_count_group[i], right_count_group[i])
                        for node in count_nodes:
                            range_count = range_count + node
                            #print(node)

                if left_count_group[i].size != 0 and right_count_group[i].size == 0:
                    #print('Left not zero')
                    for node in left_count_group[i]:
                        range_count = range_count + node
                        #print(node)
                if right_count_group[i].size != 0 and left_count_group[i].size == 0:
                    #print('Right not zero')
                    for node in right_count_group[i]:
                        #print(node) 
                        range_count = range_count +node

                    #print(OLH_answer(count, epsilon, np.sum(OLH_count), D))
                    #D = len(all_dates) 
        return range_count 
            
        
    def real_answer(self, dates):
        if len(dates) < 2:
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()
            return self.all_counts[self.idx_dict[date_obj_0]]
        else:
            date_obj_0 = datetime.strptime(dates[0],'%Y-%m-%d').date()
            date_obj_1 = datetime.strptime(dates[1],'%Y-%m-%d').date()
            sum_ = np.sum(self.all_counts[self.idx_dict[date_obj_0]: self.idx_dict[date_obj_1]+1])  
            return sum_

        
        

