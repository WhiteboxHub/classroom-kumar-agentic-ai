"""
12_hierarchical_model.py

Pattern 4: Hierarchical Model in LangGraph
Multi-level structuring using nested StateGraphs (Subgraphs).
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict): pass

# --- Level 2 Subgraph Definition ---
def junior_eng(state): return {}
eng_subgraph = StateGraph(State)
eng_subgraph.add_node("JuniorEng", junior_eng)
eng_subgraph.add_edge(START, "JuniorEng")
eng_subgraph.add_edge("JuniorEng", END)
compiled_eng_team = eng_subgraph.compile()

# --- Level 1 Main Graph Definition ---
def director(state): return {}

def main():
    print("--- LangGraph Pattern: Hierarchical Model ---")
    print("Leveraging Subgraphs natively: A Graph within a Graph.")
    
    workflow = StateGraph(State)
    workflow.add_node("Director", director)
    
    # The Subgraph acts equivalently to a single Node at the Director level
    workflow.add_node("EngineeringTeam", compiled_eng_team)

    workflow.add_edge(START, "Director")
    workflow.add_edge("Director", "EngineeringTeam")
    # Subgraph yields back to the Director
    workflow.add_edge("EngineeringTeam", "Director")

    print("\nHierarchical Subgraph routing successfully initialized.")

if __name__ == "__main__":
    main()
