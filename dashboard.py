import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide', page_icon='icon.png', page_title='Kayfa Task 1')

df = pd.read_csv('data.csv')

st.logo("kayfaio_logo2.jpg")

col1, col2 = st.columns([2,0.5])
with col1:
    st.header("HR Attrition Dashboard", divider='blue', width='content')
with col2:
    st.image("logo_full_black.svg")

# applying filters conditions
# [df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)]

# Filters
with st.sidebar:
    st.header("Filters", divider='blue')
    state = st.radio("Employee State", ['Left', 'Stayed'], horizontal=True)
    age_range = st.slider("Employee age",18,59, (18,59))
    company_years = st.slider("Years at Company", df['years_at_company'].min(),df['years_at_company'].max(), (df['years_at_company'].min(),df['years_at_company'].max()))
    company_size = st.multiselect('Company Size', ['Small','Medium', 'Large'], default=['Small','Medium', 'Large'])
    gender = st.pills("Gender", ['Male', 'Female'], selection_mode='multi', default=['Male','Female'])
    remote = st.pills("Workplace", ['Onsite', 'Remote'], selection_mode='multi', default=['Onsite','Remote'])
    remote = ['Yes' if i=='Remote' else 'No' for i in remote]
    st.divider()
    # if st.button("Reset values", type='primary'):
    #     age_range = (18,59); company_years=(1,51); company_size=['Small', 'Medium', 'Large']; gender = ['Male', 'Female']; remote=['Yes','No']


# Metrics: albayanat ally fo2
col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment='center', border=True)
with col1:
    ratio = int(df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)].count()['employee_id'])
    st.metric(label=":blue[Total Employees]", value=ratio)
with col2:
    ratio = f"{round((int(df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].count()['employee_id']) / len(df))*100, 2)} %"
    st.metric(label=":blue[Ratio of Attrition]", value=ratio)
with col3:
    ratio = round(float(df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)]['monthly_income'].mean()), 2)
    st.metric(label=":blue[Averaye Salaries]", value=f"{ratio} $")
with col4:
    ratio = round(float(df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)]['years_at_company'].mean()), 2)
    st.metric(label=":blue[Average Years in company]", value=f"{ratio} years")
with col5:
    ratio = int(df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)]['age'].mean())
    st.metric(label=":blue[Average Ages]", value=f"{ratio} years")

tab1, tab2 = st.tabs(['According to Company', 'According to Employee'])

# asbab mota3aleka balsherka nafsaha
with tab1:
    st.subheader("According to :blue[Company]")

    q = "Is the reason financial or non-financia?"
    st.subheader(q)
    col1, col2 = st.columns(2, vertical_alignment='center', border=True)
    with col1:
        d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['company_size'].isin(company_size)][df['gender'].isin(gender)].groupby('attrition')['monthly_income'].mean().reset_index(name='average_income')

        # fig = px.pie(d,
        #             names='attrition',
        #             values='average_income',
        #             title='Salaries Ration beteen stayed and left emplyees',
        #             hole=0.3,
        #             )
        # fig.update_traces(textinfo='percent+value')
        d = df[['monthly_income', 'job_level', 'attrition']].groupby(['job_level','attrition'])['monthly_income'].mean().reset_index(name='average salary')

        fig = px.bar(
            d,
            x='job_level',
            y='average salary',
            title='Salaries rate for each job level and attrition rate',
            text_auto='0.1f',
            barmode='group',
            labels={'job_level': 'Job Level'},
            color='attrition'
        )
        st.plotly_chart(fig)

    with col2:
        d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['company_size'].isin(company_size)][df['gender'].isin(gender)].groupby('attrition')['number_of_dependents'].mean().reset_index(name='number_of_dependents')
        fig = px.pie(d,
                    names='attrition',
                    values='number_of_dependents',
                    title='Average Number of Dependents Ration beteen stayed and left emplyees',
                    hole=0.3,
                    )
        fig.update_traces(textinfo='percent+value')
        st.plotly_chart(fig)

    st.info("By compairing job levels and their average salaries, the entry level, mid level, and senior level average salaries are very near to each other, these considered that there is no chance to enhance or increasing in the salaries.")
    st.success("**Sugest:** to make a clear slaries system for employees, that is fair and offer opportunities for development and income improvements as they go more experienced.")
    st.divider()
    # ____________________________________________________________________________

    q = "What is the most job domain have attrition employees?"
    st.subheader(q)
    col1, col2 = st.columns(2, vertical_alignment='center')
    with col1:
        with st.container(border=True):
            d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['company_size'].isin(company_size)][df['gender'].isin(gender)][df['attrition']=='Left'].groupby('job_role')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')

            fig = px.bar(
                d, 
                x='job_role',
                y='attrition_number',
                title='Number of job domain and attrition number',
                labels={'job_role': 'Job Role', 'attrition_number': 'Number of Attritions'},
                text_auto='.1f',
                color='job_role'
            )
            st.plotly_chart(fig)
    with col2:
        with st.container(border=True):
            d = (df.assign(is_left=(df['attrition']=='Left').astype(int))
                .groupby('job_role')['is_left']
                .mean()
                .reset_index(name='attrition_rate')
                )
            d['attrition_rate'] = d['attrition_rate']*100

            fig = px.bar(
                d, 
                x='job_role',
                y='attrition_rate',
                title='Ratio of job domain and attrition number',
                labels={'job_role': 'Job Role', 'attrition_rate': r'Percentage % of Attritions'},
                text_auto='.1f',
                color='job_role'
            )
            st.plotly_chart(fig)
            
    st.info("Most domain is Technology these beacause there is a large number of employees works in the tech")
    st.divider()
    # ____________________________________________________________________________

    q = "What factors can affect on the employees attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns(2, vertical_alignment='center')
    with col1:
        with st.container(border=True):
            d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('employee_recognition')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')

            fig = px.bar(
                d, 
                x='employee_recognition',
                y='attrition_number',
                title='Ratio of employee recognition and attrition number',
                labels={'employee_recognition':'Employee Recognition', 'attrition_number':'Atrrition Rate'},
                text_auto='.1f',
                color='employee_recognition'
            )
            st.plotly_chart(fig)
    with col2:
        st.container()
        st.info("There is an inverse relation between the employee recognition and the attrition rate:")
        st.success("**Suggest:** Making weekly or even monthly meeting share there knowledge and thouts, to make all employees feels that they are recognised.")
    st.divider()
    # ____________________________________________________________________________

    q = "What factors can affect on the employees attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns(2, vertical_alignment='center')
    with col1:
        with st.container(border=True):
            d = (df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])].assign(is_left=(df['attrition']=='Left').astype(int))
                .groupby('company_size')['is_left']
                .mean()
                .reset_index(name='attrition_rate')
                )
            d['attrition_rate'] = d['attrition_rate']*100

            d = d.sort_values(by='company_size', key=lambda x:x.map({'Small':1,'Medium':2,'Large':3}))

            d['Percent'] = d.apply(lambda x: f"{round(x['attrition_rate'], 2)} %", axis=1)

            fig = px.bar(
                d,
                x='company_size',
                y='attrition_rate',
                title='Attrition rate according to company size',
                labels={'company_size':'Company Size', 'attrition_rate':'Atrrition Rate'},
                text='Percent',
                color='company_size',
                width=1000
            )
            st.plotly_chart(fig)
    with col2:
        st.container()
        st.info("The Smaller companies is exposed to attrition rate more than medium and large companies with small rate")
    st.divider()
    # ____________________________________________________________________________

    q = "What factors can affect on the employees attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns(2, vertical_alignment='center')
    with col1:
        with st.container(border=True):
            d = (df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])].assign(is_left=(df['attrition']=='Left').astype(int))
                .groupby('company_reputation')['is_left']
                .mean()
                .reset_index(name='attrition_rate')
                )
            d['attrition_rate'] = d['attrition_rate']*100

            d = d.sort_values(by='company_reputation', key=lambda x:x.map({'Poor':1,'Fair':2,'Good':3,'Excellent':4}))

            d['Percent'] = d.apply(lambda x: f"{round(x['attrition_rate'], 2)} %", axis=1)

            fig = px.bar(
                d,
                x='company_reputation',
                y='attrition_rate',
                title='Attrition rate according to company reputation',
                labels={'company_reputation':'Company Reputation', 'attrition_rate':'Atrrition Rate'},
                text='Percent',
                color='company_reputation',
                width=1000
            )
            st.plotly_chart(fig)
    with col2:
        st.container()
        st.info("More poor reputition companies are exposed to attrition rate more than good and excellent companies")
    st.divider()
    # ____________________________________________________________________________

    q = "What factors can affect on the employees attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns([1.8,1], vertical_alignment='center')
    with col1:
        with st.container(border=True):
            d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('number_of_promotions')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')

            total = d['attrition_number'].sum()
            d['Percent'] = (d['attrition_number'] / total) * 100

            d['Percent'] = d.apply(lambda row: f"{row['attrition_number']}   ({row['Percent']:.1f}%)", axis=1)

            fig = px.bar(
                d, 
                x='number_of_promotions',
                y='attrition_number',
                title='Ratio of number of promotions and attrition number',
                labels={'number_of_promotions':'Number of Promotions', 'attrition_number':'Atrrition Number'},
                color='number_of_promotions',
                text='Percent'
            )
            st.plotly_chart(fig)
    with col2:
        st.container()
        st.info(r"Only 1 promotion will decrease the attrition rate with **+50%**")
        st.success("**Sugest** to increase promotions for the deserving employees")
    st.divider()
    # ____________________________________________________________________________

    q = "What factors can affect on the employees attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns([1.5,1], vertical_alignment='center')
    with col1:
        with st.container(border=True):
            st.write("**Relation between number of years at comany and number of attrition employees**")
            st.space('medium')
            st.line_chart(df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('years_at_company')['attrition'].count(), x_label='years at company', y_label='number of attrition')
    with col2:
        with st.container(border=True):
            d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('job_level')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')

            total = d['attrition_number'].sum()
            d['Percent'] = (d['attrition_number'] / total) * 100

            d['Percent'] = d.apply(lambda row: f"{row['attrition_number']}   ({row['Percent']:.1f}%)", axis=1)

            fig = px.bar(
                d, 
                x='job_level',
                y='attrition_number',
                title='Ratio of job level and attrition number',
                labels={'job_level':'Job Level', 'attrition_number':'Attrition Rate'},
                color='job_level',
                text='Percent'
            )
            st.plotly_chart(fig)
    st.info(r"There is inverse relation with the number of years at the company and the number of attrition employees")
    st.success("**Sugest** to focus on new commers, increase follow-up and guidance from their leaders")
    st.divider()


# =======================================================================================================================================================
# asbab al mowazaf
with tab2:
    st.subheader("According to :blue[Employee]")

    q = "Does the job satisfaction and performance affect the attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns(2, vertical_alignment='center')
    with col1:
        with st.container(border=True):
            d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('job_satisfaction')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')

            total = d['attrition_number'].sum()
            d['Percent'] = (d['attrition_number'] / total) * 100
            
            d = d.sort_values(by='job_satisfaction', key=lambda x:x.map({'Low':1,'Medium':2,'High':3,'Very High':4}))

            d['Percent'] = d.apply(lambda row: f"{row['attrition_number']}   ({row['Percent']:.1f}%)", axis=1)

            fig = px.bar(
                d, 
                x='job_satisfaction',
                y='attrition_number',
                title='Ratio of job satisfaction and attrition number',
                labels={'job_satisfaction':'Job Satisfaction', 'attrition_number':'Attrition Rate'},
                color='job_satisfaction',
                text='Percent'
            )
            st.plotly_chart(fig)
    with col2:
        with st.container(border=True):
            d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('performance_rating')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')

            total = d['attrition_number'].sum()
            d['Percent'] = (d['attrition_number'] / total) * 100
            
            d = d.sort_values(by='performance_rating', key=lambda x:x.map({'Low':1,'Below Average':2,'Average':3,'High':4}))

            d['Percent'] = d.apply(lambda row: f"{row['attrition_number']}   ({row['Percent']:.1f}%)", axis=1)

            fig = px.bar(
                d, 
                x='performance_rating',
                y='attrition_number',
                title='Ratio of performance rating and attrition number',
                labels={'performance_rating':'Performance Rating', 'attrition_number':'Attrition Rate'},
                color='performance_rating',
                text='Percent'
            )
            st.plotly_chart(fig)
    st.info("According to the charts, employees with high and very high job satisfaction and employees whith average to high performance are more exposed to left their companies. This may be happened bacouse of over qualification reasons")
    st.success("**Suggest:** to evaluate employees before offering them a job and refused under-qualified and over-qualified employees")

    st.divider()
    # ____________________________________________________________________________

    q = "Does the remote work can affect the employees attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns([1,1], vertical_alignment='center')
    with col1:
        with st.container(border=True):
            # d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('remote_work')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')
            d = (df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)].assign(is_left=(df['attrition']=='Left').astype(int))
                .groupby('remote_work')['is_left']
                .mean()
                .reset_index(name='attrition_rate')
                )
            d['remote_work'] = d['remote_work'].map(lambda x: 'Remote' if x=='Yes' else 'Onsite')
            d['attrition_rate'] = d['attrition_rate']*100

            # d = d.sort_values(by='remote_work', key=lambda x:x.map({'Poor':1,'Fair':2,'Good':3,'Excellent':4}))

            d['Percent'] = d.apply(lambda x: f"{round(x['attrition_rate'], 2)} %", axis=1)

            fig = px.bar(
                d,
                x='remote_work',
                y='attrition_rate',
                title='Attrition rate according to company reputation',
                # text_auto='0.1f',
                labels={'remote_work':'Remote Work', 'attrition_rate':'Attrition Rate'},
                text='Percent',
                color='remote_work',
                width=1000
            )
            st.plotly_chart(fig)
    with col2:
        with st.container(border=True):
            d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)].groupby('attrition')['distance_from_home'].mean().sort_values(ascending=False).reset_index(name='distance_from_home')

            fig = px.bar(
                d, 
                x='attrition',
                y='distance_from_home',
                text_auto='0.1f',
                title='Average distance from home by miles for stayed and left employees',
                labels={'distance_from_home':'Distance from Home in miles', 'attrition':'Attrition'},
                color='attrition',
            )
            st.plotly_chart(fig)
    st.info(r"Employees that are works onsite are more exposed to left their companies than remote work by **double**.")
    st.success("**Sugest:** to increase the remote work and hybrid work for the employees with job that allow this option.")
    st.divider()
    # ____________________________________________________________________________
    q = "Does the age range can affect the employees attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns([1,1], vertical_alignment='center')
    with col1:
        with st.container(border=True):
            # d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('work-life_balance')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')

            d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('age')['attrition'].count().reset_index(name='attrition')

            d = (d.map(lambda x: '18 - 29' if x>=18 and x<=29 else x)
            .map(lambda x: '30 - 39' if type(x)==int and x>=30 and x<=39 else x)
            .map(lambda x: '40 - 49' if type(x)==int and x>=40 and x<=49 else x)
            .map(lambda x: '50 - 59' if type(x)==int and x>=50 and x<=59 else x))

            d = d.groupby('age')['attrition'].sum().reset_index(name='attrition')

            fig = px.bar(
                d,
                x='age',
                y='attrition',
                title='Age ranges and number of attrition',
                text_auto='0.1f',
                labels={'age':'Age Range','attrition':'Attrition Number'},
                color='age'
            )
            st.plotly_chart(fig)
    with col2:
        st.container()
        st.info(r"Employees of age range between 18-29 are more exposed to left their jobs")
    st.divider()
    # _____________________________________________________________________________
    q = "Does the martial status can affect the employees attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns([1,1], vertical_alignment='center')
    with col1:
        with st.container(border=True):
            # d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('work-life_balance')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')

            # d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('age')['attrition'].count().reset_index(name='attrition')

            d = (df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)].assign(is_left=(df['attrition']=='Left').astype(int))
                .groupby('marital_status')['is_left']
                .mean()
                .reset_index(name='attrition_rate')
                )

            d['attrition_rate'] = d['attrition_rate']*100

            d = d.sort_values(by='marital_status', key=lambda x:x.map({'Single':1,'Married':2,'Divorced':3}))

            d['Percent'] = d.apply(lambda x: f"{round(x['attrition_rate'], 2)} %", axis=1)

            fig = px.bar(
                d,
                x='marital_status',
                y='attrition_rate',
                title='Attrition rate according to company reputation',
                labels={'marital_status':'Marital Status','attrition_rate':'Attrition Number'},
                text='Percent',
                color='marital_status',
                width=1000
            )
            st.plotly_chart(fig)
    with col2:
        st.container()
        st.info(r"Employees that are not married have more chance with **74%** to left their jobs")
    st.divider()
    # _____________________________________________________________________________

    q = "What factors can affect on the employees attrition rate?"
    st.subheader(q)
    col1, col2 = st.columns([1,1], vertical_alignment='center')
    with col1:
        with st.container():
            # d = df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)][df['attrition']=='Left'].groupby('work-life_balance')['attrition'].count().sort_values(ascending=False).reset_index(name='attrition_number')

            d = (df[df['remote_work'].isin(remote)][(df['years_at_company'] >= company_years[0]) & (df['years_at_company'] <= company_years[1])][(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])][df['gender'].isin(gender)][df['company_size'].isin(company_size)].assign(is_left=(df['attrition']=='Left').astype(int))
                .groupby('company_reputation')['is_left']
                .mean()
                .reset_index(name='attrition_rate')
                )
            d['attrition_rate'] = d['attrition_rate']*100

            d = d.sort_values(by='company_reputation', key=lambda x:x.map({'Poor':1,'Fair':2,'Good':3,'Excellent':4}))

            # d['percent'] = str(d['attrition_rate']) + ' %'

            d['Percent'] = d.apply(lambda x: f"{round(x['attrition_rate'], 2)} %", axis=1)

            fig = px.bar(
                d,
                x='company_reputation',
                y='attrition_rate',
                title='Attrition rate according to company reputation',
                labels = {'company_reputation':"Company Reputation",'attrition_rate':'Attrition Rate'},
                text='Percent',
                color='company_reputation',
                width=1000
            )
            st.plotly_chart(fig)
    with col2:
        st.container()
        st.info(r"Employees of Poor and Fair work life balance are more exposed to left their jobs")
    st.divider()
    

st.header("Final Suggetions:")
st.write("""**1.** Increase the remote work and hybrid work for the employees with job that allow this option.
         
**2.** Making weekly or even monthly meeting share there knowledge and thouts, to make all employees feels that they are recognised.

**3.** to Increase promotions for the deserving employees.

**4.** Focus on new commers, increase follow-up and guidance from their leaders.

**5.** Evaluate employees before offering them a job and refused under-qualified and over-qualified employees.

**6.** Make a clear slaries system for employees, that is fair and offer opportunities for development and income improvements as they go more experienced.""")




