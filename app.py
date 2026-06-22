import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

st.title("🤖 Gemini AI Chatbot")

user_input = st.text_input("Ask me anything:")

if user_input:
    response = model.invoke(user_input)
    st.write(response.content)