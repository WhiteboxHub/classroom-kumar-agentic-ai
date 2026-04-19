"""
09_network_decentralized.py

Pattern 1: Network (Decentralized) in LangGraph
StateGraph where agents route directly to other agents via conditional edges.
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    current_agent: str
    task: str

def agent_a(state): return {"current_agent": "B"}
def agent_b(state): return {"current_agent": "C"}
def agent_c(state): return {"current_agent": "END"}

# Peer-to-peer conditional routing function
def router(state):
    route = state.get("current_agent", "END")
    return route if route in ["B", "C"] else END

def main():
    print("--- LangGraph Pattern: Network (Decentralized) ---")
    print("Any node can arbitrarily route to any other node organically.")
    
    workflow = StateGraph(State)
    workflow.add_node("AgentA", agent_a)
    workflow.add_node("AgentB", agent_b)
    workflow.add_node("AgentC", agent_c)

    # Edge configuration
    workflow.add_edge(START, "AgentA")
    
    # AgentA routes straight to AgentB or AgentC peer-to-peer
    workflow.add_conditional_edges("AgentA", router, {"B": "AgentB", "C": "AgentC", END: END})
    workflow.add_conditional_edges("AgentB", router, {"C": "AgentC", END: END})
    workflow.add_edge("AgentC", END)
    
    print("\nGraph successfully compiled mapping direct communication pathways.")

if __name__ == "__main__":
    main()
