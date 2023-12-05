"""
Roger Lera
19/10/2023
"""
import os
import numpy as np
import time
import csv
from read_files import *
from random_paths import *
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def load_secrets(id_):
    user_info = st.secrets.user_db
    try:
        id_ = int(id_)
    except:
        return None,None,None
    
    if id_ in user_info.user_id:
        index_ = user_info.user_id.index(id_)
        name_ = user_info.user_name[index_]
        group_ = user_info.user_group[index_]
        field_ = user_info.user_field[index_]
        return name_,group_,field_
    else:
        return None,None,None
    
def pie_chart(fa):
    st.write(f"##### Skills required by this job field that you would acquire if you follow this learning pathway: {fa:.0f} %")
    df_fa = pd.DataFrame({'name':['Learnt Skills','Unlearnt Skills'],'percentage':[fa,100-fa]})
    pie = px.pie(df_fa, values='percentage', names='name',color='name',
                color_discrete_map={'Learnt Skills':'green',
                                'Unlearnt Skills':'red'},
                category_orders={'name':['Learnt Skills','Unlearnt Skills']})
    pie = px.pie(df_fa, values='percentage', names='name',color='name',
                category_orders={'name':['Learnt Skills','Unlearnt Skills']})
    pie.update_layout(legend=dict(font=dict(size=16)),
                    font_size=16)
    
    st.plotly_chart(pie)
    return None

def bar_chart(J,skills,n_jobs=5):
    st.write(f"##### Jobs for which you would be more employable within this job field")
    ja_df = job_field_affinity(J,skills,n_jobs)
    bar = px.bar(ja_df, x='ja', y='Jobs', orientation='h')
    bar.update_xaxes(title_text = "Percentage of Required Skills Acquired with this Pathway (%)",
                    range=[0, 100],
                    tickfont=dict(size=14))
    bar.update_yaxes(tickfont=dict(size=14))
    bar.update_layout(yaxis=dict(title=dict(font=dict(size=16))),
                    xaxis=dict(title=dict(font=dict(size=16))))
    st.plotly_chart(bar)
    return None


path_ = os.getcwd()
wd_ = 'results'
fields_path = os.path.join(path_,'field_dict.csv')
results_path = os.path.join(path_,'results')
courses_path = os.path.join(path_,'courses')


ded_dict = {"Low (10 h)":5,
            "Medium (20 h)":10,
            "Trumpet master (40 h)":20,
            "Aristotelian expert (80 h)":40}

ded_dict = {"Low (10 h)":5,
            "Medium (20 h)":10,
            "High (40 h)":20,
            "Very High (80 h)":40}

ded_dict = {"10 h":5,
            "20 h":10,
            "40 h":20,
            "80 h":40}

ded_emoji = {5:':snail:',
             10:':doughnut:',
             20:':trumpet:',
             40:':books:'}

ded_emoji = {5:':smiley:',
             10:':sunglasses:',
             20:':nerd_face:',
             40:':brain:'}


try:
    field_dict = st.session_state['fields']
    A = st.session_state['activities']
    user_db = st.secrets.db_credentials
    
except:
    A = read_providers(courses_path)
    field_dict = read_fields(fields_path)
    st.session_state['activities'] = A   
    st.session_state['fields'] = field_dict

st.write("# Learning Path :books:")

#st.sidebar.number_input(
#        "Introduce ID.",
#        min_value=1000,
#        max_value=9999,
#        key = "id"
#    )

#st.sidebar.text_input(
#        "Introduce ID.",
#        placeholder='0000',
#        key = "id"
#    )

st.text_input(
        "Introduce ID.",
        placeholder='0000',
        key = "id"
    )

if 'id' in st.session_state.keys():
    
    name_,group_,field_list_ = load_secrets(st.session_state['id'])
    if name_ == None and st.session_state['id'] == '':
        st.info("Introduce your personal ID to visualize the learning pathway.", icon='💡' )
    elif name_ == None:
        st.error('Incorrect ID', icon='🚨')
    else:
        st.session_state['name'] = name_
        st.session_state['group'] = group_
        st.session_state['field_list'] = field_list_
        

        name = st.session_state['name']
        group = st.session_state['group']
        field_list = st.session_state['field_list']

        st.write(f"### Hello {name},")
        st.write(f"""From the results of the #Job Safari questionnaire, we selected job fields that might be interesting for you. 
                        Then, we created learning pathways with a different study time (10, 20, 40 and 80 hours) for each selected job field.
                        Explore the different learning pathways created for you and take a look at the courses that we recommend you.
                        Once you finish looking at the learning pathways, complete the following [form](https://docs.google.com/forms/d/e/1FAIpQLSf7Ciho82zyAW2Z2UQA7hJFdYPC_ek6iszOcSgZzNSJqrGYAA/viewform?usp=sf_link).
                     """)

        #st.sidebar.selectbox(
        #    "Select a job field.",
        #    field_list,
            #index=None,
            #placeholder = "Unknown Field",
        #    key = "field"
        #)
        st.selectbox(
            "Select a job field.",
            field_list,
            #index=None,
            #placeholder = "Unknown Field",
            key = "field"
        )

        #st.sidebar.selectbox(
        #    "Select the available time for study.",
        #    ded_dict.keys(),
        #    index=2,
            #placeholder = "Unknown Dedication",
        #    key = 'dedication',
        #)

        st.selectbox(
            "Select the available time for study.",
            ded_dict.keys(),
            index=2,
            #placeholder = "Unknown Dedication",
            key = 'dedication',
        )


        if 'dedication' in st.session_state.keys() and 'field' in st.session_state.keys():
            
            ded = st.session_state['dedication']
            fie = st.session_state['field']

            if group == 's' or group == 'm':

                file_path = os.path.join(results_path,f"{field_dict[fie]}-{ded_dict[ded]}.stdout")

                df,fa = read_path(file_path,A)
                J = read_field(f'{field_dict[fie]}')
                skills = read_skills(file_path)

            elif group == 'c':
                index_fie = list(field_list).index(fie)
                field_list_id = [field_dict[fie] for f in field_list]
                new_fields = change_field(field_list_id,list(field_dict.values()),seed=int(st.session_state['id']))
                fie_val = new_fields[index_fie]

                file_path = os.path.join(results_path,f"{fie_val}-{ded_dict[ded]}.stdout")

                df,fa = read_path(file_path,A)
                J = read_field(f'{fie_val}')
                skills = read_skills(file_path)

            elif group == 'r':

                file_path = os.path.join(results_path,f"{field_dict[fie]}-{ded_dict[ded]}.stdout")

                df,fa = read_path(file_path,A)
                J = read_field(f'{field_dict[fie]}')
                skills = read_skills(file_path)
                df = random_path(A,seed=int(st.session_state['id'])*int(field_dict[fie]),dedication_week=ded_dict[ded],n_weeks=2)

            
            

            st.write(f"## Job Field: {fie}")
            st.write(f"### Available time for study: {ded} {ded_emoji[ded_dict[ded]]}")

            styler = df.style.hide_index()
            
            st.write(styler.to_html(escape=False, index=False), unsafe_allow_html=True)

            """
            
            """

            pie_chart(fa)

            bar_chart(J,skills,n_jobs=5)

else:
    st.info("Introduce your personal ID to visualize the learning pathway.", icon='💡' )


    






