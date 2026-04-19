"""
03n_tool_db_query.py
Demonstrates the tool use pattern with a Database Query simulation.
"""
import os, getpass
import asyncio
import nest_asyncio
from typing import List
from dotenv import load_dotenv
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

# UNCOMMENT to prompt the user securely and set API keys as environment variables
# load_dotenv()
# os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")

try:
    # A model with function/tool calling capabilities is required.
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    print(f"✅ Language model initialized: {llm.model}")
except Exception as e:
    print(f"🛑 Error initializing language model: {e}")
    llm = None

# --- Define a Tool ---
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

# --- Create a Tool-Calling Agent ---
if llm:
    # This prompt template requires an `agent_scratchpad` placeholder for the agent's internal steps.
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a data analyst assistant. Convert user queries into SQL to query our structured datasets, run the SQL, and summarize the results clearly."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # Create the agent, binding the LLM, tools, and prompt together.
    agent = create_tool_calling_agent(llm, tools, agent_prompt)
    
    # AgentExecutor is the runtime that invokes the agent and executes the chosen tools.
    agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)

    async def run_agent_with_tool(query: str):
        """Invokes the agent executor with a query and prints the final response."""
        print(f"\n--- 🏃 Running Agent with Query: '{query}' ---")
        try:
            response = await agent_executor.ainvoke({"input": query})
            print("\n--- ✅ Final Agent Response ---")
            print(response["output"])
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
