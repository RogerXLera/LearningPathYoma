"""
Roger Lera
19/10/2023
"""
import os
import numpy as np
import time
import csv
from read_files import *
import streamlit as st
import plotly.express as px

path_ = os.getcwd()
wd_ = 'results'
fields_path = os.path.join(path_,'field_dict.csv')
results_path = os.path.join(path_,'results')

try:
    field_dict = st.session_state['fields']
except:
    field_dict = read_fields(fields_path)
    st.session_state['fields'] = field_dict    



st.write("# Learning Path :trumpet: :doughnut:")
st.sidebar.selectbox(
    "Select a field.",
    field_dict.keys(),
    #index=None,
    #placeholder = "Unknown Field",
    key = "field"
)

ded_dict = {"Low (10 h)":5,
            "Medium (20 h)":10,
            "High (40 h)":20,
            "Super (80 h)":40}

ded_dict = {"Low (10 h)":5,
            "Medium (20 h)":10,
            "Trumpet master (40 h)":20,
            "Aristotelian expert (80 h)":40}

ded_emoji = {5:':smiley:',
             10:':nerd:',
             20:':sunglasses:',
             40:':brain:'}

ded_emoji = {5:':snail:',
             10:':doughnut:',
             20:':trumpet:',
             40:':books:'}

st.sidebar.selectbox(
    "Select a dedication.",
    ded_dict.keys(),
    #index=None,
    #placeholder = "Unknown Dedication",
    key = 'dedication',
)


if 'dedication' in st.session_state.keys() and 'field' in st.session_state.keys():
    
    ded = st.session_state['dedication']
    fie = st.session_state['field']

    file_path = os.path.join(results_path,f"{field_dict[fie]}-{ded_dict[ded]}.stdout")

    df,fa = read_path(file_path)
    J = read_field(f'{field_dict[fie]}')
    skills = read_skills(file_path)

    st.write(f"## Field: {fie}")
    st.write(f"### Dedication: {ded} {ded_emoji[ded_dict[ded]]}")

    st.write(df)

    st.write(f"#### Skill Learning: {fa:.0f} %")

    df_fa = pd.DataFrame({'name':['Learnt','Not learnt'],'percentage':[fa,100-fa]})
    pie = px.pie(df_fa, values='percentage', names='name', title='Skill Learning')
    st.plotly_chart(pie)

    st.write(f"#### Field Jobs")
    ja_df = job_field_affinity(J,skills,5)
    bar = px.bar(ja_df, x='Skill Learning (%)', y='Jobs', title='Learning Jobs',orientation='h')
    st.plotly_chart(bar)




st.markdown(
    """
    ### Want to learn more about Yoma?
    - Check out [Yoma](https://www.yoma.africa/)
    - Create your Yoma [profile](https://app.yoma.africa/)
    - Jump into our [opportunities](https://app.yoma.africa/opportunities) offer. 
"""
)

    






