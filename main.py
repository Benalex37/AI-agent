from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()



def main():

    model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

    tools =[]
    agent_executor = create_react_agent(model, tools)
    print(" welcome! I am your AI assistant. Type 'quit' to exit.")
    print("you can ask me anything.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "quit":
            break

        print("\nAssistant: ", end="")

        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")

        print()

if __name__ == "__main__":
    main()
