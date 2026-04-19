"""
07_tool_api_call.py
Demonstrates the tool use pattern with an API Call simulation using LangGraph.
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
def fetch_api_data(endpoint: str) -> str:
    """
    Makes a RESTful API call to the system backend to fetch JSON data.
    Valid endpoints to fetch from are '/users/1', '/products/recent', or '/status'.
    """
    print(f"\n--- 🌐 Tool Called: fetch_api_data for endpoint: '{endpoint}' ---")
    simulated_results = {
        "/users/1": '{"id": 1, "name": "John Doe", "email": "john@example.com"}',
        "/products/recent": '[{"id": 101, "item": "Laptop", "price": 999.99}, {"id": 102, "item": "Keyboard"}]',
        "/status": '{"status": "online", "uptime": "99.99%"}',
        "default": '{"error": "404 - Endpoint not found or permission denied"}'
    }
    result = simulated_results.get(endpoint.strip(), simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result

tools = [fetch_api_data]

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
        """Runs all agent queries concurrently."""
        tasks = [
            run_agent_with_tool("Can you get the user details for user ID 1?"),
            run_agent_with_tool("Fetch the recent products from the API, what's available?"),
            run_agent_with_tool("Check if the billing API /billing/1 is active.") # Will trigger default error
        ]
        await asyncio.gather(*tasks)

    if __name__ == "__main__":
        nest_asyncio.apply()
        asyncio.run(main())
