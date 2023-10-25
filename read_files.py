"""
Roger Lera
19/10/2023
"""
import csv
import pandas as pd
import os
from definitions import *

def skill_extraction(line_,a,object_="Activity"):
    """
        This function extracts the skills aquired and the prerequisites of a given activity
            INPUT: line_ (of the dataframe)
                    a (activity object)
    """
    # we start with the skills
    if object_ == "Activity":
        try:
            #skills = line_['Skills Acquired'].split(',')
            #skills_level = line_['Level Skills Acquired'].split(',')
            skills = line_['Skills Acquired'].split(';;')
            skills_level = line_['Prob Skills Acquired'].split(';;')
        except:
            skills = []
            skills_level = []
        try:
            #prereq = line_['Skills Required'].split(',')
            #prereq_level = line_['Level Skills Required'].split(',')
            prereq = line_['Skills Required'].split(';;')
            prereq_level = line_['Prob Skills Required'].split(';;')
        except:
            prereq = []
            prereq_level = []
    else:
        try:
            skills = line_['Skills Required'].split(';;')
            skills_level = line_['Prob Skills Required'].split(';;')
        except:
            skills = []
            skills_level = []
        prereq = []
        prereq_level = []
    
    if len(skills) != len(skills_level):
        raise ValueError(f"Different number of skills ({len(skills)}) and levels {len(skills_level)} for activity {a.name}.")
    for i in range(len(skills)):
        s = Skill(name=skills[i],level=1,probability=float(skills_level[i])) #creating a skill object
        s.add_skill(a.skills)

    if len(prereq) != len(prereq_level):
        raise ValueError(f"Different number of skills ({len(prereq)}) and levels {len(prereq_level)} for activity {a.name}.")
    for i in range(len(prereq)):
        s = Skill(name=prereq[i],level=1,probability=float(prereq_level[i])) #creating a skill object
        s.add_skill(a.prerequisites)

    return None

def read_activities(file_path):
    """
        This function reads the file containing the activities and 
    """
    df = pd.read_csv(file_path,sep=',') #store file in pandas.DataFrame
    provider = file_path.split('/')[-1].split('.')[0]
    activities = []
    for i in range(len(df)):

        line_ = df.iloc[i] #df line
        id_ = line_['ID']
        name_ = line_['Title']
        try:
            time_ = float(line_['Hours dedicated'])
        except:
            time_ = 10.0
        if type(line_['Money']) == str and len(line_['Money']) == 0:
            cost_= 0.0
        else:
            cost_= float(line_['Money'])
        url_ = line_['URL']
        if cost_ <= 0:
            course_ = True
        else:
            course_ = False
        a = Activity(id=id_,name=name_,time=time_,cost=cost_,course=course_,url=url_,provider=provider) #create activity object
        skill_extraction(line_,a)
        activities.append(a)
    
    return activities

def read_providers(folder_path):
    """
        This function saves all the activities from all providers
    """
    files = os.listdir(folder_path)
    A = [Activity(id=0,name='Initial Activity',cost=0)]
    for file in files:
        file_path = os.path.join(folder_path,file)
        activities = read_activities(file_path)
        A += activities

    return A


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

    return name[1:-1],st,fi,int(h)

def select_activity(name,A):

    len_ = len(name)
    for a in A:
        if name == a.name[:len_]:
            return a

    raise ValueError(f"{name} does not correspond to any activity.")

def create_link(name,url):
    return f'<a target="_blank" href="{url}">{name}</a>'

def read_path(file_path,A):
    """
    This function reads the learning paths and returns a pd.Dataframe and the field affinity
    """

    with open(file_path,'r') as f:

        f_lines = f.readlines()
        name = []
        st = []
        fi = []
        h = []
        url = []
        fa = 0
        detect_act = "Activity:"
        detect_fa = "Job affinity:"
        for row in f_lines:
            if row[:len(detect_act)] == detect_act:
                nam,s,fi_,h_ = process_line(row)
                a = select_activity(nam,A)
                #name += [a.name]
                link = create_link(a.name,a.url)
                name += [link]
                st += [s]
                fi += [fi_]
                h += [h_]
                url += [a.url]
            elif row[:len(detect_fa)] == detect_fa:
                fa = float(row.split(detect_fa)[1].split(' ')[1])
                
    
    #return pd.DataFrame({'Course':name[1:],'Start Week':st[1:],"End Week":fi[1:],"Study Time (h)":h[1:],"URL":url[1:]}),fa
    return pd.DataFrame({'Course':name[1:],'Start Week':st[1:],"End Week":fi[1:],"Study Time (h)":h[1:]}),fa
    
    #return {'Course':name[1:],'Start Week':st[1:],"End Week":fi[1:],"Study Time (h)":h[1:]},fa


def print_dataframe(df):
    """
    This function prints the DataFrame
    """
    #col1,col2,col3,col4 = st.columns(4)
    return None

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
        jobs += [{'Jobs':j.name,'ja':ja_counter/l_skills*100}]

    def order_dict(e):
        return e['ja']
    
    jobs.sort(reverse=False,key=order_dict)

    return pd.DataFrame(jobs[:n_jobs])