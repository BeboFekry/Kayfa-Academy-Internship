import streamlit as st
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import speech_recognition as sr
import pandas as pd
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
import datetime
import random
from pymongo import MongoClient
import os

about = """Your about info"""
menu_items = {
"Get help": "mailto:@abdallahfekry95@gmail.com",
"About": about}
st.set_page_config(page_title="Kayfa Chtbot", initial_sidebar_state='collapsed', layout='wide', menu_items=menu_items)

if 'retriever' not in st.session_state:
    st.session_state.embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    st.session_state.vector_database = Chroma(
        persist_directory=r".\MyVectorDB",
        embedding_function=st.session_state.embeddings_model
    )
    st.session_state.retriever = st.session_state.vector_database.as_retriever(search_type="similarity", search_kwargs={'k': 4})

if "first" not in st.session_state:
    st.session_state.first = True

if "chat" not in st.session_state:
    st.session_state.chat = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "language" not in st.session_state:
    st.session_state.language = "Arabic"

# __________________________________________________________________________________________________________

password = st.secrets['mongo_db_pass']
uri = f"mongodb+srv://abdallahfekry95:{password}@cluster0.tihyjgn.mongodb.net/?appName=Cluster0"
def get_db_connection(uri=uri):
    client = MongoClient(uri)
    db = client["kayfa_academy_db"]
    return db

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, r"Ai-Analytics Intern at Kayfa Task3 Data and its Summary","data","json","kayfa_courses.json")
courses = pd.read_json(path)
path = os.path.join(current_dir, r"Ai-Analytics Intern at Kayfa Task3 Data and its Summary","data","json","kayfa_roadmaps.json")
roadmaps = pd.read_json(path)
retriever = st.session_state.vector_database.as_retriever(search_type="similarity", search_kwargs={'k': 4})

@tool
def search_courses_db(name: str, track: str = None, max_price: float = None, level: str = None) -> str:
    """
    Use this tool for a detailed search of the course database (course names, prices, duration, level).
    Do not use it to search for policies or general details.
    """
    filtered_df = courses.copy()

    if name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(name, case=False, na=False)]
    if track:
        filtered_df = filtered_df[filtered_df['track'].str.contains(track, case=False, na=False)]
    if level:
        filtered_df = filtered_df[filtered_df['level'].str.contains(level, case=False, na=False)]
    if filtered_df.empty:
        return "can't find any courses with these search filters."
    return filtered_df.to_json(orient='records', force_ascii=False)

@tool
def search_roadmaps_db(name: str, track: str = None, skills:str = None) -> str:
    """Use this tool to find out details of the Roadmaps, the number of courses within the roadmap, and the tools used in it."""
    filtered_df = roadmaps.copy()
    if name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(name, case=False, na=False)]
    if track:
        filtered_df = filtered_df[filtered_df['track'].str.contains(track, case=False, na=False)]
    if skills:
        filtered_df = filtered_df[filtered_df['skills'].str.contains(skills, case=False, na=False)]
    if filtered_df.empty:
        return "can't find any roadmaps with these search filters."
    return filtered_df.to_json(orient='records', force_ascii=False)

@tool
def query_knowledge_base(question: str) -> str:
    """
    Use this tool to search the academy's files knowledge base for:
    - Refund policies and frequently asked questions (FAQs).
    - Details about specific diplomas (SOC, AI, Fullstack, Data Science, Pentest) and how to apply.
    - Free and paid content.
    - Information about the company and instructors.
    """
    docs = retriever.invoke(question)

    if not docs:
        return "No informations found at the knowledge base"

    formatted_context = "\n\n".join(
        f"source: {doc.metadata.get('label', 'unknown')}\ninformations: {doc.page_content}"
        for doc in docs
    )
    return f"founded informations:\n{formatted_context}"

# Name, phone / WhatsApp, email, city or country, preferred language & dialect, and best contact channel and time.
@tool
def capture_crm_lead(name: str, phone: str, email:str = None, country: str =None, language:str=None, interest: str =None, conversation_summary: str = None, state: str =None) -> str:
    """
    Use this tool only when the customer shows a clear intent to purchase or requests registration.
    The tool saves customer data to the MongoDB database.
    """

    ticket = {
        "Name": name,
        "Phone Number": phone,
        "Email": email,
        "Country": country,
        'language':language,
        "Interest": interest,
        "Conversational Summary": conversation_summary,
        'state':state
    }

    db = get_db_connection(uri)
    collection = db["tickets"]

    current_year = datetime.datetime.now().year
    random_id = random.randint(1000, 9999)
    ticket_id = f"LEAD-{current_year}-{random_id}"

    result = collection.insert_one(ticket)

    print(f"New Ticket have been recorded: {ticket}\n\n{result}")
    return f"Customer data have been saved successfully! {result}"


if 'messages' not in st.session_state:
    system_message = """You are a professional sales assistant for Kayfa Academy.
                    Your tasks:
                    1. Understand the client's needs and answer accurately using the available tools.
                    2. Do not invent any information (prices, durations, policies). If you are unsure, use the 'query_knowledge_base' tool.
                    3. For questions about a specific diploma (such as SOC or Data Science), use the 'query_knowledge_base' to gather marketing and persuasive details.
                    4. To search for prices and courses, use 'search_courses_db' or 'search_roadmaps_db'.
                    5. Start with individual/free courses for hesitant clients, and direct serious clients to diplomas.
                    6. If the client expresses interest in registering, ask for their name and number, then use the 'capture_crm_lead' tool to silently save the data, and then inform them that the process is complete.
                    7. Speak in natural and friendly Arabic.
                    8. Your name is KayfaBot
                    """
    st.session_state.messages = {
        "messages": [
            ("system", system_message),
        ]
    }

if "agent" not in st.session_state:
    API = st.secrets['GeminiAPI']
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", google_api_key=API, temperature=0.1)
    tools = [search_courses_db, search_roadmaps_db, query_knowledge_base, capture_crm_lead]
    st.session_state.agent = create_react_agent(llm, tools)

def add_message(sender,message):
    if sender=='ai':
        st.session_state.messages['messages'].append(('ai',message))
    elif sender=='human':
        st.session_state.messages['messages'].append(('human',message))
    else:
        return f"Value Error '{sender}': Sender must be either 'ai' or 'human' not {sender}!"

def chat(text):
    try:
        add_message('human', text)
        with loading.chat_message("assistant", avatar='media/bot avatar.png'):
            col1, col2 = st.columns([1,15], vertical_alignment='center', gap=None)
            with col1:
                st.image('media/Sparkles Loop Loader ai.gif')
            with col2:
                st.markdown("AI Decision...")
            response_state = st.session_state.agent.invoke(st.session_state.messages)
        final_message = response_state['messages'][-1]

        if isinstance(final_message.content, list):
            response_text = final_message.content[0].get('text', '')
        else:
            response_text = final_message.content
            
        add_message('ai', response_text)
        return response_text
    except Exception as e:
        return str(e)

def speech_to_text(path, language):
    """
    Voice_To_Text
    Takes the "path of a voice file" and convert it into text
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
    if language == 'Arabic':
        text = recognizer.recognize_google(audio, language="ar-EG")
    else:
        text = recognizer.recognize_google(audio, language="en-US")
    return text

# =========================================================================================================================================

# Chat history
col1, col2, col3 = st.columns([1,3,1])
if st.session_state.chat:
        counter = 0
        for c in st.session_state.chat:
            # Show the text messages
            if c['parts'][0].get('text'):
                current_dir = os.path.dirname(os.path.abspath(__file__))
                user_path = os.path.join(current_dir, "media","user avatar.png")
                bot_path = os.path.join(current_dir, "media","bot avatar.png")
                st.chat_message('user' if c['role']=="user" else "assistant", avatar=user_path if c['role']=="user" else bot_path).markdown(c['parts'][0]['text'], text_alignment='right', width='stretch')
            # Show the audio messages
            if c['parts'][0].get('audio'):
                # Autoplay the last voice note
                if counter == len(st.session_state.chat)-1:
                    st.chat_message('user' if c['role']=="user" else "assistant", avatar=user_path if c['role']=="user" else bot_path).audio(c['parts'][0]['audio'], autoplay=False)
                else:
                    st.chat_message('user' if c['role']=="user" else "assistant", avatar=user_path if c['role']=="user" else bot_path).audio(c['parts'][0]['audio'])
            counter += 1
        current = st.empty()
        loading = st.empty()
        
        if st.button(":material/save: Save conversation", type='tertiary'):
            st.session_state.chat_history.append({'chat':st.session_state.chat})
            st.success("Your chat stored successfully!")
else:
    with col2:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bot_path = os.path.join(current_dir, "media","bot avatar.png")
        st.chat_message('ai', avatar=bot_path).write("اهلا 👋, انا كيفَبوت أقدر اساعادك ازاي النهاردة؟")
        # loading = st.empty()
        current = st.empty()
        loading = st.empty()
# ========================================================================================================================

message = st.chat_input("Say Something...", accept_audio=True)

if message:
    # if message.files:
    #     pass
    if message.text:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        user_path = os.path.join(current_dir, "media","user avatar.png")
        current.chat_message('user', avatar=user_path).markdown(message.text)
        response = chat(message.text)
        loading.empty()
        st.session_state.chat.append({"role":"user","parts":[{"text":message.text}]})
        st.session_state.chat.append({"role":"model","parts":[{"text":response}]})
        st.rerun()
    if message.audio:
        current.chat_message('user', avatar=user_path).audio(message.audio, autoplay=False)
        with open("user_voice.mp3", "wb") as f:
            f.write(message.audio.read())
        try:
            text = speech_to_text("user_voice.mp3", st.session_state.language)
        except KeyError as e:
            st.error(f"{e}\nYour current Language is {st.session_state.language} use the specified language or change it and use a quiet place to use the speech tool")
        response = chat(text)
        loading.empty()
        # st.session_state.chat.append({"role":"user","parts":[{"text":text}]})
        st.session_state.chat.append({"role":"user","parts":[{"audio":message.audio}]})
        st.session_state.chat.append({"role":"model","parts":[{"text":response}]})
        st.rerun()

# Rate
if len(st.session_state.messages['messages'])>1:
    col11, col22 = st.columns([1,15], vertical_alignment='center', gap=None)
    with col11:
        st.write("**Rate** me:")
    with col22:
        fb = st.feedback(options='faces')
    if st.session_state.first:
        st.session_state.fb = fb
    if fb or fb==0:
        if  fb >= 3:
            if st.session_state.first or st.session_state.fd != fb:
                st.session_state.first = False
                st.balloons()
                st.success("Great, we are happy for your experience 😍")
                st.session_state.fd = fb
        elif fb<2:
            if st.session_state.first or st.session_state.fd != fb:
                st.session_state.first = False
                st.error("Sorry for that, we made our effort 😔")
                st.session_state.fd = fb
        else:
            if st.session_state.first or st.session_state.fd != fb:
                st.session_state.first = False
                st.warning("Okay, not bad 👉👈")
                st.session_state.fd = fb
# ______________________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________________


# Chat history
if st.session_state.chat_history:
    with st.sidebar:
        st.header(":material/chat: Chat history", divider='blue')
        col1, col2 = st.columns([8,1])
        # st.title("Chat history", )
        with col1:
            if st.button(":material/add: New chat", width='stretch',type='tertiary'):
                st.session_state.chat = []
                st.session_state.products = []
                st.session_state.category = []
                st.session_state.top_product = []
                st.rerun()
        with col2:
            st.space('medium')

        k = len(st.session_state.chat_history)
        for h in range(len(st.session_state.chat_history)-1, -1, -1):
            with col1:
                if st.button(f'chat {k}', width='stretch', type='tertiary'):
                    st.session_state.chat = st.session_state.chat_history[h]['chat']
                    st.rerun()
            with col2:
                if st.button(':material/delete:', key=k, type='tertiary'):
                    st.session_state.chat_history.remove(st.session_state.chat_history[h])
                    st.rerun()
            k-=1
else:
    with st.sidebar:
        if st.button(":material/add: New chat", width='stretch',type='tertiary'):
            st.session_state.chat = []
            st.session_state.data = []
            st.rerun()

# Settings
with st.sidebar:
    st.divider()
    st.header(":material/settings: Settings")
    new_lang = st.selectbox(f"**Language** (current is {st.session_state.language})", ('Arabic', 'English'), placeholder='Language..', index=None)
    if new_lang and new_lang != st.session_state.language:
        st.write(f"Language will be change into :orange[{new_lang}]")
        if st.button("Save changes", type='primary'):
            st.session_state.language = new_lang
            st.rerun()

