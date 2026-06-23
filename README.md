# Groq AI Agent

An AI-powered agent built with Python, Streamlit, LangChain, LangGraph, and Groq's LLaMA 3.3 70B model. Features real-time web search via Tavily and a safe arithmetic calculator tool.

**Live Demo:** [https://ai-agent-7rjjyvlmepjdndqyd7ods4.streamlit.app](https://ai-agent-7rjjyvlmepjdndqyd7ods4.streamlit.app)

## Skills Used

| Skill | Details |
|---|---|
| **Python** | Core language for all logic and tooling |
| **Streamlit** | Frontend UI — chat interface, session state, sidebar |
| **LangChain** | Tool definitions (`@tool`), LLM wrappers (`ChatGroq`) |
| **LangGraph** | `create_react_agent` — ReAct loop orchestration |
| **Groq API** | LLaMA 3.3 70B as the underlying LLM |
| **Tavily Search API** | Live web search tool for real-time information |
| **python-dotenv** | Secure API key management via `.env` |
| **AST / operator** | Safe math expression evaluator (no `eval()`) |

## Chatbot vs AI Agent

| | Chatbot | AI Agent |
|---|---|---|
| **How it works** | Takes input → returns a response | Takes input → reasons → picks tools → acts → responds |
| **Tools** | None | Web search, calculator, APIs, etc. |
| **Real-time info** | No — only knows its training data | Yes — can search the web live |
| **Multi-step reasoning** | No | Yes — plans and executes across steps |
| **Example** | "What is 2+2?" → "4" | "What is 2+2?" → uses calculator tool → "4" |
| **This project** | — | Uses ReAct loop to decide when and which tool to call |

Ai agent demo:

<img width="1267" height="1468" alt="image" src="https://github.com/user-attachments/assets/cdd98172-4a27-4425-a700-037d9a22555a" />
