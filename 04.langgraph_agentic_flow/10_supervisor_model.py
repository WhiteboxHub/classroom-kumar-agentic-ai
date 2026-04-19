"""
10_supervisor_model.py

Pattern 2: Supervisor Model in LangGraph
A central node distributes work payload and workers strictly route back to the supervisor.
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    next_node: str

def supervisor(state): return {"next_node": "Worker1"}  # Simulates routing choice
def worker_1(state): return {}
def worker_2(state): return {}

def main():
    print("--- LangGraph Pattern: Supervisor Model ---")
    print("Centralizing control logic: Supervisor -> Worker -> Supervisor")
    
    workflow = StateGraph(State)
    workflow.add_node("Supervisor", supervisor)
    workflow.add_node("Worker1", worker_1)
    workflow.add_node("Worker2", worker_2)

    # Hub config
    workflow.add_edge(START, "Supervisor")
    
    # Supervisor routes out
    workflow.add_conditional_edges(
        "Supervisor", 
        lambda s: s["next_node"], 
        {"Worker1": "Worker1", "Worker2": "Worker2", END: END}
    )
    
    # Workers are strictly bound to return to the supervisor
    workflow.add_edge("Worker1", "Supervisor")
    workflow.add_edge("Worker2", "Supervisor")
    
    print("\nGraph successfully structured a star-topology Hub & Spoke architecture.")

if __name__ == "__main__":
    main()
