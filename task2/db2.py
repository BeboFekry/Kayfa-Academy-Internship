import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pymongo import MongoClient



password = st.secrets['mongo_db_pass']
uri = f"mongodb+srv://abdallahfekry95:{password}@cluster0.tihyjgn.mongodb.net/?appName=Cluster0"

def get_db_connection(uri):
    client = MongoClient(uri)
    db = client["kayfa_academy_db"]
    return db

def save_df_to_mongo(df, collection_name, uri=uri):
    db = get_db_connection(uri)
    data = df.to_dict(orient="records")
    db[collection_name].insert_many(data)
    print(f"uploaded {len(data)} document {collection_name} successfully!")

def load_df_from_mongo(collection_name, uri=uri):
    db = get_db_connection(uri)
    data = list(db[collection_name].find({}, {"_id": 0}))
    return pd.DataFrame(data)


col1, col2 = st.columns([2,1], vertical_alignment='center')
with col1:
    st.header("Student Analysis Dashboard", divider='blue', width='content')
    st.subheader("Task 2 - AI & Data Anlytics Internship - Page 2")
with col2:
    st.image("logo_full_black.svg")
st.divider()


page0 = st.Page('db1.py')
if st.button('Back :material/keyboard_double_arrow_left:', type='tertiary'):
    st.switch_page(page0)

page = st.Page('db3.py')
if st.button('Next :material/keyboard_double_arrow_right:', type='tertiary'):
    st.switch_page(page)


# Q6
df = load_df_from_mongo('concepts_failure')
highest_failure = list(df[df['failure_rate'] == df['failure_rate'].max()].values[0])
weakest_concept = highest_failure[0]
fig = px.bar(df, 
              x='concept_name', 
              y='failure_rate', 
              title=f"Failure rate for each Concept, The Weakest is \"{highest_failure[0]}\" with rate: {round(highest_failure[1], 2)} %, found in Course: Python Programming", 
              labels={'concept_name':'Concept Name', 'failure_rate':'Failure Rate %'},
              color='failure_rate', 
              text_auto='0.1f',
              color_continuous_scale='blues'
              )
st.plotly_chart(fig)
st.write("Highlights specific curriculum concepts with the highest student failure rates across the platform.")
st.info("Insight: Recursion is the absolute primary bottleneck. Dedicated remedial workshops are highly recommended.")
st.divider()

# Q7
df = load_df_from_mongo('recursion_over_time')

fig = px.bar(df, 
             x='timestamp', 
             y='score_pct',
             text_auto='0.1f',
             labels={'timestamp':'Time Stamp', 'score_pct':'Score Percentage'},
             title=f'Cohort Mastery Over Time for: {weakest_concept}')
st.plotly_chart(fig)
st.write("Tracks the performance trend of the weakest concept across successive evaluation periods.")
st.info("Insight: Mastery remains consistently flat over time, showing that current teaching iterations for this concept are not working.")
st.divider()

# Q8
df = load_df_from_mongo('submition_time_state')
fig = px.scatter(df, 
                  x='buffer_hours', 
                  y='score', 
                  color='is_late',
                  labels={'score':'Score', 'buffer_hours':'Buffer Hours'},
                  title='Submission Buffer vs Score (Negative buffer = Late)')
fig.add_vline(x=0, line_dash="dash", line_color="red")
st.plotly_chart(fig)
st.write("Evaluates how early or late submissions impact the final assignment grade on an individual level.")
st.info("Insight: Submissions marked as late fall significantly behind the average grade threshold.")
st.divider()
# ___________________-
df = load_df_from_mongo('submition_time_range_state')
fig = px.bar(df, 
             x='buffer_hours', 
             y='score_pct', 
             text_auto='0.1f',
             color='score_pct',
             labels={'buffer_hours':'Buffer Hours', 'score_pct':'Score Percentage'},
             title='Submission Buffer vs Average Score (Negative buffer = Late)')
st.plotly_chart(fig)
st.write("Aggregates student scores based on their submission time buffer relative to the strict deadline.")
st.info("Insight: Encouraging early submissions could drastically improve overall averages as students who submit early perform better.")
st.divider()

# Q9
df = load_df_from_mongo('attendance_overtime')
fig = px.line(df.sort_values(by='week'), 
              x='week', 
              y='metric_value', 
              color='type',
              labels={'week':'Week', 'metric_value':'Metric Value'}, 
              title='Attendance & Engagement Over Term')
st.plotly_chart(fig)
st.write("Monitors weekly changes in attendance rates and normalized engagement volume to detect sudden drops.")
st.info("Insight: Synchronized dips across both metrics suggest external factors like mid-term periods affecting overall participation.")
st.divider()

# Q10
df = load_df_from_mongo('student_age_bounds')
fig = px.bar(df, 
             x='age_band', 
             y=['score', 'attendance','total_watch_time_in_hrs'], 
             barmode='group',  
             text_auto='0.1f',
             labels={'age_band':'age_band'},
             title='Outcomes by Age Band')
st.plotly_chart(fig)
st.write("Compares average scores, attendance, and watch time across different student age demographics.")
st.info("Insight: Mature learners (26-30) demonstrate peak engagement, while younger demographics may need distinct motivational strategies.")
st.divider()



