import streamlit as st

st.logo("media/kayfaio_logo2.png")
st.set_page_config(page_icon='media/icon.png', page_title='Kayfa Chatbot')

home = st.Page(r"home.py", title="Home", icon=":material/home:", default=True)
chat = st.Page(r"chat.py", title="Chat", icon=":material/smart_toy:")

pages = {
    "": [home, chat]
}

pg = st.navigation(pages)
pg.run()
