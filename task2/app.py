import streamlit as st


st.set_page_config(layout='wide', page_icon='icon.png', page_title='Kayfa Task 2')
st.logo("kayfaio_logo2.png", size='large')

db1 = st.Page("db1.py", title="Dashboard 1", icon=":material/analytics:", default=True)
db2 = st.Page("db2.py", title="Dashboard 2", icon=":material/analytics:")
db3 = st.Page("db3.py", title="Dashboard 3", icon=":material/analytics:")

pg = st.navigation({"Dashboards":[db1, db2, db3]})

pg.run()