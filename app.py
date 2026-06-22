import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

if "messages" not in st.session_state:
    st.session_state.messages = []

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Gemini AI Chatbot")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    response = model.invoke(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.content}
    )

    with st.chat_message("assistant"):
        st.write(response.content)