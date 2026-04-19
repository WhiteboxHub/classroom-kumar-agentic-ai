"""
06_tool_code_execution.py
Demonstrates the tool use pattern with a Code Execution simulation using LangGraph.
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
            run_agent_with_tool("Execute a simple script to print 'hello world'"),
            run_agent_with_tool("What is 2 + 2? Write code to find out."),
            run_agent_with_tool("I need a script that runs complex algorithms.") # Should trigger default
        ]
        await asyncio.gather(*tasks)

    if __name__ == "__main__":
        nest_asyncio.apply()
        asyncio.run(main())
