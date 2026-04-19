"""
08_tool_db_query.py
Demonstrates the tool use pattern with a Database Query simulation using Google ADK.
"""
from google_adk.agents import Agent
from google_adk.tools import ToolRegistry
from google_adk.llms import GoogleGenAIModel

# Initialize the centralized ADK tool registry
registry = ToolRegistry()

@registry.register("run_sql_query", description="Executes a SELECT SQL query against the internal PostgreSQL database.")
def run_sql_query(sql: str) -> str:
    print(f"\n--- 🗄️ Tool Called: run_sql_query with query:\n'{sql}' ---")
    
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

def main():
    print("--- Initializing Google ADK Agent ---")
    try:
        model = GoogleGenAIModel(model_name="gemini-2.0-flash")
    except Exception as e:
        print(f"🛑 Error initializing language model: {e}")
        return

    # Create the ADK Agent, passing directly the tool from the registry
    agent = Agent(
        name="DataAnalyst",
        instruction="You are a data analyst. Convert user questions into SQL to query our structured datasets.",
        tools=[registry.get_tool("run_sql_query")],
        model=model
    )

    queries = [
        "Can you list our current employees?",
        "How are our sales doing?",
        "Pull the Q1 metrics for me, please."
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
