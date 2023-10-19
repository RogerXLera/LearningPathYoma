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

ded_dict = {"Medium (5 h/week)":5,
            "High (10 h/week)":10,
            "Super (20 h/week)":20}

ded_dict = {"Medium (5 h/week)":5,
            "High (10 h/week)":10,
            "Trumpet master (20 h/week)":20}

ded_emoji = {5:':smiley:',
             10:':nerd:',
             20:':sunglasses:'}

ded_emoji = {5:':snail:',
             10:':doughnut:',
             20:':trumpet:'}

st.sidebar.selectbox(
    "Select a field.",
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

    st.write(f"## Field: {fie}")
    st.write(f"### Dedication: {ded} {ded_emoji[ded_dict[ded]]}")

    st.write(f"Field affinity: {fa:.2f} %")

    st.write(df)


st.markdown(
    """
    ### Want to learn more about Yoma?
    - Check out [Yoma](https://www.yoma.africa/)
    - Create your Yoma [profile](https://app.yoma.africa/)
    - Jump into our [opportunities](https://app.yoma.africa/opportunities) offer. 
"""
)

    






