"""
Roger Lera
19/10/2023
"""
import csv
import pandas as pd
import os
from definitions import *
import numpy as np
import random as rd

def random_path(A,seed,dedication_week=5,n_weeks=2):
    """
    Random learning path
    """
    rd.seed(seed)
    
    len_A = len(A)
    indexes = list(range(0,len_A))
    rd.shuffle(indexes)
    total_dedication = dedication_week*n_weeks
    dedication_counter = 0
    dedication_counter_week = 0
    current_week = 1
    name = []
    st = []
    fi = []
    h = []
    for i in indexes:
        a = A[i]
        if total_dedication < dedication_counter + a.time:
            continue
        dedication_counter += a.time
        dedication_counter_week += a.time
        link = create_link(a.name,a.url)
        #name += [link]
        name += [a.name]
        st += [current_week]
        while dedication_counter_week >= dedication_week:
            dedication_counter_week -= dedication_week
            current_week += 1
        fi += [current_week]
        h += [a.time]
        if total_dedication == dedication_counter:
            break
    
    return pd.DataFrame({'Course':name,'Start Week':st,"End Week":fi,"Study Time (h)":h})



if __name__ == '__main__':
    from read_files import *
    path_ = os.getcwd()
    wd_ = 'results'
    fields_path = os.path.join(path_,'field_dict.csv')
    results_path = os.path.join(path_,'results')
    courses_path = os.path.join(path_,'courses')

    A = read_providers(courses_path)
    r = random_path(A,0,dedication_week=5,n_weeks=2)
    print(r)
