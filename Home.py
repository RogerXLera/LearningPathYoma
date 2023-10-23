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
import plotly.graph_objects as go

path_ = os.getcwd()
wd_ = 'results'
fields_path = os.path.join(path_,'field_dict.csv')
results_path = os.path.join(path_,'results')

try:
    field_dict = st.session_state['fields']
except:
    field_dict = read_fields(fields_path)
    st.session_state['fields'] = field_dict    



st.write("# Learning Path :books:")
st.sidebar.selectbox(
    "Select a employment category.",
    field_dict.keys(),
    #index=None,
    #placeholder = "Unknown Field",
    key = "field"
)

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

st.sidebar.selectbox(
    "Select the available time for study.",
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

    st.write(f"## Employment Category: {fie}")
    st.write(f"### Available time for study: {ded} {ded_emoji[ded_dict[ded]]}")


    # Define custom CSS to increase font size
    css = """
    <style>
    .stDataFrame th, .stDataFrame td {
        font-size: 30px;
    }
    </style>
    """

    # Display the DataFrame with custom styling
    st.markdown(css, unsafe_allow_html=True)
    st.dataframe(df,hide_index=True)

    st.write(f"##### Skills required by this employment category that you would acquire if you follow this learning pathway: {fa:.0f} %")

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

    st.write(f"##### Jobs for which you would be more employable within this employment category")
    ja_df = job_field_affinity(J,skills,5)
    bar = px.bar(ja_df, x='ja', y='Jobs', orientation='h')
    bar.update_xaxes(title_text = "Percentage of Required Skills Acquired with this Pathway (%)",
                     range=[0, 100],
                     tickfont=dict(size=14))
    bar.update_yaxes(tickfont=dict(size=14))
    bar.update_layout(yaxis=dict(title=dict(font=dict(size=16))),
                      xaxis=dict(title=dict(font=dict(size=16))))
    st.plotly_chart(bar)


    






