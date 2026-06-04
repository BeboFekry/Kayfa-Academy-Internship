import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

df = pd.read_csv('data.csv')

st.logo("kayfaio_logo2.jpg")
st.header("HR Attrition Dashboard", divider='blue')

col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment='center', border=True)
with col1:
    ratio = f"{round((int(df[df['attrition']=='Left'].count()['employee_id']) / len(df))*100, 2)} %"
    st.metric(label=":blue[Ratio of Attrition]", value=ratio)
with col2:
    ratio = round(float(df['monthly_income'].mean()), 2)
    st.metric(label=":blue[Averay Salaries]", value=f"{ratio} $")
with col3:
    ratio = round(float(df['years_at_company'].mean()), 2)
    st.metric(label=":blue[Average Years in company]", value=f"{ratio} years")
with col4:
    ratio = int(df[df['attrition']=='Stayed'].count()['employee_id'])
    st.metric(label=":blue[Number of stayed employees]", value=ratio)
with col5:
    ratio = int(df['age'].mean())
    st.metric(label=":blue[Average Ages]", value=f"{ratio} years")

tab1, tab2 = st.tabs(['According to Company', 'According to Employee'])
with tab1:
    st.subheader("According to :blue[Company]")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.space()
        st.bar_chart(df.groupby('attrition')['monthly_income'].mean(), y_label='Monthly Salary', x_label='Attrition', horizontal=True)
        st.bar_chart(df.groupby('attrition')['number_of_dependents'].mean(), y_label='Number of Dependents', x_label='Attrition', horizontal=True)
        
    with col2:
        st.bar_chart(df[df['attrition']=='Left'].groupby('job_role')['attrition'].count().sort_values(ascending=False), 
                     x_label='Job Domain', y_label='Number of Attrition Employees', sort=False)
    with col3:
        st.bar_chart(df[df['attrition']=='Left'].groupby('employee_recognition')['attrition'].count().sort_values(ascending=False), 
                     x_label='Employee Recognition', y_label='Number of Attrition Employees', sort=False)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.line_chart(df[df['attrition']=='Left'].groupby('years_at_company')['attrition'].count(), x_label='years at company', y_label='number of attrition')
    with col2:
        st.bar_chart(df[df['attrition']=='Left'].groupby('company_size')['attrition'].count().sort_values(ascending=False), 
                     x_label='Company Size', y_label='Number of Attrition', sort=False, horizontal=True)
        
        st.bar_chart(df[df['attrition']=='Left'].groupby('company_reputation')['attrition'].count().sort_values(ascending=False), 
                     x_label='Company Reputation', y_label='Number of Attrition', sort=False, horizontal=True)
    with col3:
        st.bar_chart(df[df['attrition']=='Left'].groupby('number_of_promotions')['attrition'].count().sort_values(ascending=False), 
                     x_label='Number of Promotions', y_label='Number of Attrition Employees', sort=False)
        
with tab2:
    st.subheader("According to :blue[Employee]")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.bar_chart(df[df['attrition']=='Left'].groupby('job_satisfaction')['attrition'].count().sort_values(ascending=False), 
                     x_label='Job Satisfaction', y_label='Number of Attrition Employees', sort=False)
    with col2:
        st.bar_chart(df[df['attrition']=='Left'].groupby('remote_work')['attrition'].count().sort_values(ascending=False), 
                     y_label='Remote Work', x_label='N. Attrition', sort=False, horizontal=True)
        st.bar_chart(df[df['remote_work']=='No'].groupby('attrition')['distance_from_home'].mean().sort_values(ascending=False), 
                     y_label='Average distance from home for onsite employees', x_label='N. Attrition', sort=False, horizontal=True)
    with col3:
        st.bar_chart(df[df['attrition']=='Left'].groupby('job_satisfaction')['attrition'].count().sort_values(ascending=False), 
                     x_label='Job Satisfaction', y_label='Number of Attrition', sort=False)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.bar_chart(df[df['attrition']=='Left'].groupby('job_level')['attrition'].count().sort_values(ascending=False), 
                     x_label='Job Level', y_label='Number of Attrition Employees', sort=False)
    with col2:
        df2 = pd.DataFrame({"values":df[df['attrition']=='Left'].groupby('work-life_balance')['attrition'].count().values,
       'index':df[df['attrition']=='Left'].groupby('work-life_balance')['attrition'].count().index})
        fig = px.pie(df2, values='values', names='index', title='Work Life Balance')
        st.plotly_chart(fig)
        del df2
    with col3:
        st.bar_chart(df[df['attrition']=='Left'].groupby('performance_rating')['attrition'].count().sort_values(ascending=False), 
                     x_label='Performance Rating', y_label='Number of Attrition', sort=False)
    
    

