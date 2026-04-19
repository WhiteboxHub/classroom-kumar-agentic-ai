"""
04c_supervisor_as_tool.py

Pattern 3: Supervisor as Tool
The Supervisor provides support (data, permissions, logic) to workers running the main flow.
"""
from langchain_core.tools import tool

@tool
def ask_supervisor_for_approval(budget_request: str) -> str:
    """Workers call this to request explicit permission or proprietary data from the supervisor."""
    return f"[Supervisor]: Approved budget action for '{budget_request}'."

def main():
    print("--- LangChain Pattern: Supervisor as a Tool ---")
    print("The Worker Agent carries out the core loop, treating the Supervisor simply as an oracle/tool.")
    
    # The worker holds the supervisor tool
    worker_tools = [ask_supervisor_for_approval]
    
    print("\nSimulating Execution:")
    print("Worker starts building infrastructure...")
    print("Worker encounters blocker -> invokes supervisor tool.")
    print(ask_supervisor_for_approval.invoke("Increase AWS Server Tier"))
    print("Worker resumes operation.")

if __name__ == "__main__":
    main()
