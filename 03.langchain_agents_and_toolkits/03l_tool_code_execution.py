"""
03l_tool_code_execution.py
Demonstrates the tool use pattern with a Code Execution simulation.
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
def execute_python_code(code: str) -> str:
    """
    Executes Python code in a safe sandbox environment.
    Use this tool to evaluate math, format strings, or execute simple scripts.
    """
    print(f"\n--- 💻 Tool Called: execute_python_code with code:\n{code}\n---")
    simulated_results = {
        "print('hello world')": "hello world\n",
        'print("hello world")': "hello world\n",
        "2 + 2": "4",
        "import math\nmath.sqrt(16)": "4.0",
        "default": f"Simulated execution output for code executed successfully with exit code 0."
    }
    # Naive cleanup for exact matching simulation
    clean_code = code.strip()
    result = simulated_results.get(clean_code, simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result

tools = [execute_python_code]

# --- Create a Tool-Calling Agent ---
if llm:
    # This prompt template requires an `agent_scratchpad` placeholder for the agent's internal steps.
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful Python coding assistant. Execute code to answer the user's mathematical or programming questions."),
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
            run_agent_with_tool("Execute a simple script to print 'hello world'"),
            run_agent_with_tool("What is 2 + 2? Write code to find out."),
            run_agent_with_tool("I need a script that runs complex algorithms.") # Should trigger default
        ]
        await asyncio.gather(*tasks)

    if __name__ == "__main__":
        nest_asyncio.apply()
        asyncio.run(main())
