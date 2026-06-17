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
    st.subheader("Task 2 - AI & Data Anlytics Internship - Page 3")
with col2:
    st.image("logo_full_black.svg")
st.divider()



page0 = st.Page('db2.py')
if st.button('Back :material/keyboard_double_arrow_left:', type='tertiary'):
    st.switch_page(page0)
page = st.Page('db1.py')
if st.button('First Page :material/keyboard_double_arrow_right:', type='tertiary'):
    st.switch_page(page)
# st.divider()

# Q11
df = load_df_from_mongo('student_segmentation')
fig = px.scatter(
    df[df['total_watch_time']<30], 
    x='total_watch_time', 
    y=['score','attendance_rate'], 
    color='cluster',
    title='Student Segmentation according to attendance, engagement, average grade and number of failed concepts',
    labels={'total_watch_time':'Total Watch Time'},
    opacity=0.8
)
st.plotly_chart(fig)
st.write("Utilizes K-Means clustering to segment students based on engagement and performance metrics.")
st.info("Insight: Distinct behavioral clusters allow for highly targeted and automated email interventions.")
st.divider()
fig = px.scatter_3d(
    df, 
    x='attendance_rate', 
    y='score', 
    z='total_watch_time',
    color='cluster',
    title='Student Segmentation',
    labels={'attendance_rate': 'Attendance Rate', 'score': 'Average Grade %', 'total_watch_time': 'Total Watch Time'},
    opacity=0.8,
)
st.plotly_chart(fig)
st.write("A deep multidimensional view of the student body clustering separating high achievers from disengaged profiles.")
st.divider()


# Q12
df = load_df_from_mongo('group_sizes')
fig = px.bar(
    df, 
    x='group_id', 
    y=['stated_num_students', 'true_count'],
    barmode='group',
    text_auto='.0f',
    title='True vs Stated Group Sizes',
    labels={'group_id': 'Group ID', 'value': 'Number of Students','variable': 'Count Type'}
)

new_names = {'stated_num_students': 'Stated Count', 'true_count': 'True Count'}
fig.for_each_trace(lambda t: t.update(name=new_names.get(t.name, t.name)))
st.write("Contrasts the administrative reported group capacity against the actual active student count.")
st.info("Insight: Significant discrepancies in certain groups reveal administrative reporting gaps that need an immediate audit.")
st.plotly_chart(fig)
# st.divider()
# Q13
smallest_group = df.sort_values('true_count').iloc[0]['group_id']
st.markdown(f"Unviable Group: {smallest_group}")
st.write("Automatically identifies groups operating below sustainable operational capacities.")
st.info(f"Insight: {smallest_group} is economically unviable and should be merged with a matching cohort immediately.")
st.divider()

# Q14
df = load_df_from_mongo('students_in_risk')
fig = px.bar(
    df,
    x='Weighted_Risk',
    y='full_name',
    color='Risk_Factor_AR',
    barmode='stack',
    title='Top 10 students at risk',
    labels={
        'full_name': 'Full Name',
        'Weighted_Risk': 'Risk',
        'Risk_Factor_AR': 'Risk Factors'
    },
    hover_data={'email': True, 'total_risk_score': ':.1%'},
    color_discrete_sequence=px.colors.sequential.Oranges_r
)

fig.update_layout(
    xaxis_title="Risk Index",
    yaxis_title="Student Name",
    legend_title="Risk Factors",
    hovermode="y unified"
)
st.plotly_chart(fig)
st.write("Ranks students based on a combined risk score of poor attendance, engagement drops, and concept failures.")
st.info("Insight: Academic advisors must prioritize one-on-one outreach to these specific students to prevent academic dropouts.")
st.divider()
# print("="*60)
# for idx, student in top_10_at_risk.reset_index(drop=True).iterrows():
#     print(f"Rank {idx+1:02d} | Student: {student['full_name']:<25} | Email: {student['email']:<30} | Total Risk Score: {student['total_risk_score']:.1%}")
# print("="*60)

# Q15
df = load_df_from_mongo('groups_grade_for_successive_assesment')
fig = px.bar(df, 
             x='group_id',
             y='score_rate',
             text_auto='0.1f',
             color='score_rate',
             title='Average Grade for each Group only for successive assesment',
             labels={'group_id':'Group ID', 'score_rate':'Score Rate'},

             )
st.plotly_chart(fig)
st.divider()
df = load_df_from_mongo('groups_grade_for_successive_assesment_overtime')

fig = px.line(df.sort_values(by='date'), x='date', y='score', color='group_id', markers=True,
                title='Group Average Grades Across Successive Assessments')
st.plotly_chart(fig)
st.write("Maps the average grade trajectory of each group across sequential assessments to monitor momentum.")
st.info("Insight: Spotting downward-trending groups early enables proactive instructor support before final evaluations.")

st.divider()
# _________________________________________________________________________________________________________________________________________




