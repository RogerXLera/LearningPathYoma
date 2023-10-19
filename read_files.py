"""
Roger Lera
19/10/2023
"""
import csv
import pandas as pd
import os
from definitions import *


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
        detect_act = "Activity:"
        detect_fa = "Job affinity:"
        for row in f_lines:
            if row[:len(detect_act)] == detect_act:
                nam,s,fi_,h_ = process_line(row)
                name += [nam]
                st += [s]
                fi += [fi_]
                h += [h_]
            elif row[:len(detect_fa)] == detect_fa:
                fa = float(row.split(detect_fa)[1].split(' ')[1])
                
    
    return pd.DataFrame({'Course':name[1:],'Start Week':st[1:],"End Week":fi[1:],"Dedication (h)":h[1:]}),fa

def read_job(file_name):
    
    with open(file_name,'r') as file_:
        reader = csv.reader(file_)
        row_ = []
        for row in reader:
            row_.extend(row)

        j = Job(row_[0],row_[1],row_[2])
        skills_ = row_[3].split(";;")
        presence_ = row_[4].split(";;")
        for i in range(len(skills_)):
            if presence_[i] == 'nan':
                s_ = Skill(skills_[i],1,presence=0.1)
            else:
                s_ = Skill(skills_[i],1,presence=presence_[i])
            j.skills.append(s_)
       
    return j

def read_field(field_id):
    """
        Read the jobs within the field and save the skills
    """

    path_ = os.getcwd()
    dir = os.path.join(os.path.join(path_,'jobs'),'jobs')
    files = os.listdir(dir)
    field_id = str(field_id)
    len_field = len(field_id)
    J = []
    for file in files:
        j_ = read_job(os.path.join(dir,file))
        if str(j_.id)[:len_field] == field_id:
            J += [j_]

    return J

def read_skill(line):
    """
    This function reads the line and returns the skills
    """
    line_split = line.split('\t')
    if len(line_split) == 3:
        return line_split[-1][1:-1]
    else:
        return None

def read_skills(file_path):
    """
    This function reads the learning paths and returns the skills gained with the learning path
    """
    trigger_s = "Skills per Unit"
    trigger_e = "Skills for Job"
    skill_extraction = False
    skills = []
    with open(file_path,'r') as f:

        f_lines = f.readlines()
        for row in f_lines:
            if row[:len(trigger_s)] == trigger_s:
                skill_extraction = True
            elif row[:len(trigger_e)] == trigger_e:
                skill_extraction = False
                break
            elif skill_extraction:
                skill = read_skill(row)
                if skill == None:
                    continue
                else:
                    skills += [skill]

    return skills

def job_field_affinity(J,skills,n_jobs):
    """
    This function returns a df with the job affinity of the jobs belonging to a given field, 
    given the skills provided by the plan
    """
    jobs = []
    for j in J:
        ja_counter = 0
        l_skills = len(j.skills)
        for s in j.skills:
            if s.name in skills:
                ja_counter += 1
        jobs += [{'Jobs':j.name,'Percentage of Required Skills Acquired with this Pathway (%)':ja_counter/l_skills*100}]

    def order_dict(e):
        return e['Percentage of Required Skills Acquired with this Pathway (%)']
    
    jobs.sort(reverse=False,key=order_dict)

    return pd.DataFrame(jobs[:n_jobs])