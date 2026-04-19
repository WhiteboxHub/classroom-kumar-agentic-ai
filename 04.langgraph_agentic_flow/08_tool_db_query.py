"""
08_tool_db_query.py
Demonstrates the tool use pattern with a Database Query simulation using LangGraph.
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
def run_sql_query(sql: str) -> str:
    """
    Executes a SELECT SQL query against the internal company PostgreSQL database.
    Schema hints:
    - Table 'employees' has columns: id, name, department
    - Table 'sales' has columns: id, total_amount, status
    - Table 'metrics' has columns: key, value
    """
    print(f"\n--- 🗄️ Tool Called: run_sql_query with query:\n'{sql}' ---")
    
    # We use basic string matching for the simulation
    db_lower = sql.lower().strip()
    result = "No records found matching query."
    
    if "employees" in db_lower:
        result = "id: 1, name: Alice, department: Engineering\nid: 2, name: Bob, department: HR"
    elif "sales" in db_lower:
        result = "total rows: 1450, total revenue: 450000"
    elif "metrics" in db_lower:
        result = "key: Q1_revenue, value: $1.2M\nkey: YOY_growth, value: 15%"
        
    print(f"--- TOOL RESULT: {result} ---")
    return result

tools = [run_sql_query]

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
            run_agent_with_tool("Can you list our current employees?"),
            run_agent_with_tool("How are our sales doing?"),
            run_agent_with_tool("Pull the Q1 metrics for me, please.")
        ]
        await asyncio.gather(*tasks)

    if __name__ == "__main__":
        nest_asyncio.apply()
        asyncio.run(main())
