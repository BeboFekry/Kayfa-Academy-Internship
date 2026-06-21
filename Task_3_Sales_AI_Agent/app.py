import streamlit as st
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "media", "kayfaio_logo2.png")
st.logo(logo_path)
st.set_page_config(page_icon='media/icon.png', page_title='Kayfa Chatbot')

home = st.Page(r"home.py", title="Home", icon=":material/home:", default=True)
chat = st.Page(r"chat.py", title="Chat", icon=":material/smart_toy:")

pages = {
    "": [home, chat]
}

pg = st.navigation(pages)
pg.run()
