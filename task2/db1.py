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
    st.subheader("Task 2 - AI & Data Anlytics Internship - Page 1")
with col2:
    st.image("logo_full_black.svg")
st.divider()



page0 = st.Page('db3.py')
if st.button('Last Page :material/keyboard_double_arrow_left:', type='tertiary'):
    st.switch_page(page0)
page = st.Page('db2.py')
if st.button('Next :material/keyboard_double_arrow_right:', type='tertiary'):
    st.switch_page(page)

# Q1
group_attendance = load_df_from_mongo('group_attendance')
platform_avg = group_attendance['attendance_rate'].mean()
fig = px.bar(group_attendance.sort_values(by='group_id'), 
              x='group_id', 
              y='attendance_rate', 
              title='Attendance Rate per Group', 
              labels={'group_id':'Group Id', 'attendance_rate':'Attendance Rate %'},
              color='attendance_rate', 
              text_auto='0.1f',
              color_continuous_scale='RdYlBu')
fig.add_hline(y=platform_avg, 
               line_dash="dash", 
               annotation_text=f"Platform Avg: {platform_avg:.1%}", 
               line_color="red")
st.plotly_chart(fig)
st.write("This chart visualizes the average attendance rate across different student groups compared to the overall platform average.")
st.info("Insight: Group 7 and Group 10 are below the red baseline require immediate attention from instructors to improve their engagement and participation.")
st.divider()

# Q2
df = load_df_from_mongo('assesment_grades')
fig = px.bar(df, 
              x='type', 
              y='score', 
              title='Score Rate per Assesment Type', 
              labels={'type':'Assesment Type', 'score':'Score Rate %'},
              color='type', 
              text_auto='0.1f',
              color_continuous_scale='RdYlBu')
st.plotly_chart(fig)
st.write("A comparison of student performance across different assessment formats.")
st.info("Insight: Assignment scores lag significantly behind quizzes and exams, highlighting a student struggle with practical, open-ended tasks.")
st.divider()

# Q3
df = load_df_from_mongo('courses_grades')
fig = px.bar(df, 
              x='course_name', 
              y='average_percentage', 
              title='Score Rate per Course', 
              labels={'course_name':'Course Name', 'average_percentage':'Score Rate %'},
              color='course_name', 
              text_auto='0.1f',
              color_continuous_scale='RdYlBu')
st.plotly_chart(fig)
st.write("Displays the average grades achieved by students broken down by their respective courses.")
st.info("Insight: Digital Marketing underperforms significantly compared to UI/UX Design, highlighting an urgent need for curriculum review.")
st.divider()


# Q4
df = load_df_from_mongo('student_attendance_grades')
fig = px.bar(df, 
              x='attendance_ratio', 
              y='attendance_rate', 
              title='Relation between Score Rate and Attendance Rate', 
              color='attendance_ratio', 
              text_auto='0.1f',
              labels={'attendance_ratio':'Attendance Ratio','attendance_rate':'Attendance Rate'}
            )
st.plotly_chart(fig)
st.write("Groups students by their attendance ratio bands to observe the corresponding average scores.")
st.info("Insight: A clear upward trend confirms that consistent physical or virtual presence directly translates to higher academic outcomes.")
st.divider()

# Q5
df = load_df_from_mongo('login_frequency_grades')
fig = px.scatter(df, x='total_watch_time', y='avg_grade', color='avg_grade', labels={'total_watch_time':'Total Watch Time in Minutes', 'avg_grade':'Average Grade %'},
                  title='Engagement vs Academic Performance')
st.plotly_chart(fig)
st.write("A scatter plot correlating the total platform video watch time with average student grades.")
st.info("Insight: Increased engagement time leads to higher grades up to a certain threshold, proving the effectiveness of digital materials.")
st.divider()

