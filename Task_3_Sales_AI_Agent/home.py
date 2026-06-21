import streamlit as st
import streamlit.components.v1 as components

# st.title("KayfaBot")
# st.divider()


chat = st.Page("chat.py", title="Chatbot", icon=":material/smart_toy:")
st.set_page_config(page_title="KayfaBot/Home", initial_sidebar_state='collapsed', layout='wide')


if "language" not in st.session_state:
    st.session_state.language = "Arabic"

# Button
st.markdown("""
    <style>
    .glow-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 12px 25px;
        font-size: 18px;
        font-weight: bold;
        color: white !important;
        background: linear-gradient(90deg, #3498db, #2980b9); 
        border: none;
        border-radius: 50px;
        cursor: pointer;
        text-decoration: none !important;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        box-shadow: 0 0 15px rgba(52, 152, 219, 0.6);
        transition: all 0.3s ease-in-out;
        z-index: 1000;
    }
    .glow-button:hover {
        box-shadow: 0 0 25px rgba(41, 128, 185, 0.8);
        transform: scale(1.05);
        background: linear-gradient(90deg, #2980b9, #3498db);
    }
    .sparkle {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <a href="chat" target="_self" class="glow-button">
        <span class="sparkle">✨</span> Ask KayfaBot!
    </a>
    """,
    unsafe_allow_html=True
)


with open('html.txt','rb') as f:
    particles_js = f.read()


col1, col2, col3 = st.columns([1,4,1])
with col1:
    components.html(particles_js, height=400, scrolling=False)
with col3:
    components.html(particles_js, height=400, scrolling=False)
with col2:
    col11, col22 = st.columns([1,1])

    st.header("The Smartest AI Sales Assistant\n\n## Ready to Chat!", text_alignment='center')
    st.markdown(':rainbow[Courses recommentdation, database resources, add sales tickets, speech recognition, decision supports]', text_alignment='center')
    mt = st.empty()
    st.columns([1.47,1,1], vertical_alignment='top')[1].image(r"media\Ai Robot Vector Art.gif")

    col1, col2, col3, col4 = st.columns([3,1.1,1.1,3])
    with col2:
        st.link_button(":material/play_arrow: Demo", type='secondary', url='', width='stretch')
    with col3:
        if st.button(":material/chat: Chat", type='primary', width='stretch'):
            st.switch_page(chat)
    st.divider()