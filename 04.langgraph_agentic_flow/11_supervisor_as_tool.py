"""
11_supervisor_as_tool.py

Pattern 3: Supervisor as Tool in LangGraph
Workers operate linearly but interrupt with conditional jumps to a Supervisor Support node.
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    needs_approval: bool

def worker(state): return {"needs_approval": True} # Simulates needing help
def supervisor_tool(state): return {"needs_approval": False} # Resolves block

def main():
    print("--- LangGraph Pattern: Supervisor as a Tool ---")
    print("Worker acts as the main runner. Conditionally invokes SupervisorTool node when trapped.")
    
    workflow = StateGraph(State)
    workflow.add_node("Worker", worker)
    workflow.add_node("SupervisorTool", supervisor_tool)

    workflow.add_edge(START, "Worker")
    
    # Worker checks if it needs supervisor support before ending
    workflow.add_conditional_edges(
        "Worker", 
        lambda s: "SupervisorTool" if s.get("needs_approval") else END
    )
    
    # Supervisor tool injects data and yields control BACK to the same worker
    workflow.add_edge("SupervisorTool", "Worker")

    print("\nGraph generated allowing workers to interrupt flow and query supervisor resources.")

if __name__ == "__main__":
    main()
