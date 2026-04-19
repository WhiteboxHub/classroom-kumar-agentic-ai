"""
05_tool_google_search.py
Demonstrates the tool use pattern with a Google Search simulation using LangGraph.
"""
import os, getpass
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool as langchain_tool
from langgraph.prebuilt import create_react_agent

# UNCOMMENT to prompt the user securely and set API keys as environment variables
# load_dotenv()
# os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")

try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    print(f"✅ Language model initialized: {llm.model}")
except Exception as e:
    print(f"🛑 Error initializing language model: {e}")
    llm = None

@langchain_tool
def google_search(query: str) -> str:
    """
    Provides factual information from the web on a given topic using Google Search.
    Use this tool to find answers to phrases like 'capital of France' or 'weather in London?'.
    """
    print(f"\n--- 🔍 Tool Called: google_search with query: '{query}' ---")
    simulated_results = {
        "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
        "capital of france": "The capital of France is Paris.",
        "population of earth": "The estimated population of Earth is around 8 billion people.",
        "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
        "default": f"Simulated search result for '{query}': No specific information found on the web."
    }
    result = simulated_results.get(query.lower(), simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result

tools = [google_search]

if llm:
    # Use LangGraph's prebuilt ReAct agent instead of LangChain's AgentExecutor
    agent = create_react_agent(llm, tools)

    async def run_agent_with_tool(query: str):
        print(f"\n--- 🏃 Running Agent with Query: '{query}' ---")
        try:
            # LangGraph agents use 'messages' array in their StateGraph state object 
            result = await agent.ainvoke({"messages": [("user", query)]})
            
            # The final appended message is the agent's textual response
            final_message = result["messages"][-1].content
            print("\n--- ✅ Final Agent Response ---")
            print(final_message)
        except Exception as e:
            print(f"\n🛑 An error occurred during agent execution: {e}")

    async def main():
        tasks = [
            run_agent_with_tool("What is the capital of France?"),
            run_agent_with_tool("What's the weather like in London?"),
            run_agent_with_tool("Tell me something about dogs.") 
        ]
        await asyncio.gather(*tasks)

    if __name__ == "__main__":
        nest_asyncio.apply()
        asyncio.run(main())
