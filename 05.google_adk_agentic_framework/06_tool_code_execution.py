"""
06_tool_code_execution.py
Demonstrates the tool use pattern with a Code Execution simulation using Google ADK.
"""
from google_adk.agents import Agent
from google_adk.tools import ToolRegistry
from google_adk.llms import GoogleGenAIModel

# Initialize the centralized ADK tool registry
registry = ToolRegistry()

@registry.register("execute_python_code", description="Executes Python code safely to evaluate math or scripts.")
def execute_python_code(code: str) -> str:
    print(f"\n--- 💻 Tool Called: execute_python_code with code:\n{code}\n---")
    simulated_results = {
        "print('hello world')": "hello world\n",
        'print("hello world")': "hello world\n",
        "2 + 2": "4",
        "import math\nmath.sqrt(16)": "4.0",
        "default": f"Simulated execution output for code executed successfully with exit code 0."
    }
    clean_code = code.strip()
    result = simulated_results.get(clean_code, simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result

def main():
    print("--- Initializing Google ADK Agent ---")
    try:
        model = GoogleGenAIModel(model_name="gemini-2.0-flash")
    except Exception as e:
        print(f"🛑 Error initializing language model: {e}")
        return

    # Create the ADK Agent, passing directly the tool from the registry
    agent = Agent(
        name="PythonCoder",
        instruction="You are a helpful Python coding assistant. Execute code to answer user questions.",
        tools=[registry.get_tool("execute_python_code")],
        model=model
    )

    queries = [
        "Execute a simple script to print 'hello world'.",
        "What is 2 + 2? Write code to find out.",
        "I need a script that runs complex algorithms."
    ]

    for q in queries:
        print(f"\n--- 🏃 Running Agent with Query: '{q}' ---")
        try:
            # We map the invocation back to agent.run(task=) natively
            response = agent.run(task=q)
            print("\n--- ✅ Final Agent Response ---")
            print(response)
        except Exception as e:
            print(f"\n🛑 An error occurred during agent execution: {e}")

if __name__ == "__main__":
    main()
