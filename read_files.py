"""
Roger Lera
19/10/2023
"""
import csv
import pandas as pd


def read_fields(field_path):
    """
    This function reads the field names and returns a dict
    """

    with open(field_path,'r') as f:

        f_read = csv.reader(f)
        dict_ = {}
        for row in f_read:
            dict_.update({row[0]:row[1]})

    return dict_

def process_line(line):
    """
    This function process the lines of the .stdout file
    """
    detect_act = "Activity:"
    detect_st = "Start Period:"
    detect_ft = "End Period:"
    
    name = line.split(detect_act)[1].split('(')[0]
    st = int(line.split(detect_st)[1].split(' ')[1])
    fi = int(line.split(detect_ft)[1].split(' ')[1])
    h = float(line.split(')')[-2].split('(')[-1])

    return name,st,fi,h


def read_path(file_path):
    """
    This function reads the learning paths and returns a pd.Dataframe and the field affinity
    """

    with open(file_path,'r') as f:

        f_lines = f.readlines()
        name = []
        st = []
        fi = []
        h = []
        fa = 0
        init_act = "Initial Activity "
        detect_act = "Activity:"
        detect_fa = "Job affinity:"
        for row in f_lines:
            if row[:len(detect_act)] == detect_act:
                print(row)
                nam,s,fi_,h_ = process_line(row)
                if nam == init_act:
                    continue
                name += [nam]
                st += [s]
                fi += [fi_]
                h += [h_]
            elif row[:len(detect_fa)] == detect_fa:
                fa = float(row.split(detect_fa)[1].split(' ')[1])
                
    
    return pd.DataFrame({'Course':name,'Start Week':st,"End Week":fi,"Dedication (h)":h}),fa