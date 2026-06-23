import os
import ast
import operator

import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

load_dotenv()

# --------------------
# TOOLS
# --------------------

# Safe arithmetic evaluator (no eval()) — supports + - * / ** and parentheses
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def _safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression")

@tool
def calculator(expression: str) -> str:
    """Evaluate basic mathematical expressions (+, -, *, /, **)."""
    try:
        tree = ast.parse(expression, mode="eval")
        return str(_safe_eval(tree.body))
    except Exception:
        return "Invalid calculation"

search_tool = TavilySearch(
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

# --------------------
# MODEL (Groq only)
# --------------------

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    st.error("GROQ_API_KEY is missing. Check your .env file.")
    st.stop()

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=groq_key,
)

# --------------------
# AGENT
# --------------------

tools = [calculator, search_tool]
agent = create_react_agent(model, tools)

# --------------------
# STREAMLIT
# --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚙️ Settings")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Groq AI Agent")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask anything...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.spinner("Thinking..."):
            result = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]}
            )
            assistant_response = result["messages"][-1].content
    except Exception as e:
        err_text = str(e)
        if "429" in err_text or "RESOURCE_EXHAUSTED" in err_text or "rate" in err_text.lower():
            assistant_response = "⚠️ Rate limit hit on Groq. Please wait a moment and try again."
        else:
            assistant_response = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.write(assistant_response)