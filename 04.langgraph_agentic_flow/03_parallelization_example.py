"""
03. LangGraph Parallelization Example
-------------------------------------
This example demonstrates how to run multiple nodes in parallel (Fan-out)
and then wait for all of them to finish before proceeding (Fan-in / Synthesis).

Core Concepts Highlighted:
- Reducers (Annotated & operator.add): When multiple nodes write to the same state
  key concurrently, a reducer is REQUIRED so updates are appended rather than overwritten.
- Fan-out Edges: Routing from one node to multiple nodes simultaneously.
- Fan-in Edges: Pointing multiple concurrent nodes precisely to a single downstream
  node. LangGraph automatically waits for all parallel dependencies upstream to finish 
  before executing the downstream node.

Flow:
1. Input Node: Receives a topic.
2. Parallel Execution (3 concurrent nodes):
   -> Analyze Pros
   -> Analyze Cons
   -> Analyze Financial Risks
3. Synthesis Node: Waits for all 3 above to finish, aggregates them, and creates a final report.
"""

import operator
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END

# ---------------------------------------------------------
# Core Component: State with Reducers
# ---------------------------------------------------------
# Highlight: `Annotated` with `operator.add` tells LangGraph how to merge
# values when multiple nodes return updates for the "analysis_results" concurrently.
class ParallelState(TypedDict):
    topic: str
    analysis_results: Annotated[List[str], operator.add]
    final_report: str

# ---------------------------------------------------------
# Core Component: Nodes
# ---------------------------------------------------------

def input_node(state: ParallelState):
    """1. Input Node: Starts the process."""
    print("--- Node: Input received ---")
    print(f"Topic: {state['topic']}")
    # Returns an empty list to initialize/clear the reducer state properly
    return {"analysis_results": []}

def analyze_pros(state: ParallelState):
    """2a. Parallel Node: Analyzes pros."""
    print("--- Parallel Execution: Analyzing Pros... ---")
    topic = state.get("topic", "")
    
    # Mock LLM insight
    insight = f"[PROS] High growth potential and innovation opportunities in {topic}."
    
    # Highlight: This list gets ADDED (not overwritten) to the shared state
    return {"analysis_results": [insight]}

def analyze_cons(state: ParallelState):
    """2b. Parallel Node: Analyzes cons."""
    print("--- Parallel Execution: Analyzing Cons... ---")
    topic = state.get("topic", "")
    
    insight = f"[CONS] regulatory uncertainty and complex logistics in {topic}."
    return {"analysis_results": [insight]}

def analyze_risks(state: ParallelState):
    """2c. Parallel Node: Analyzes financial risks."""
    print("--- Parallel Execution: Analyzing Risks... ---")
    topic = state.get("topic", "")
    
    insight = f"[RISKS] High initial capital expenditure required for {topic}."
    return {"analysis_results": [insight]}

def synthesis_node(state: ParallelState):
    """3. Fan-in Synthesis: Waits for all parallel nodes to finish."""
    print("\n--- Node: Synthesis / Fan-in ---")
    print("All parallel analyses completed. Synthesizing final report...")
    
    results = state.get("analysis_results", [])
    
    report = "### Executive Summary ###\n"
    for r in results:
        report += f"- {r}\n"
    report += "\nConclusion: Proceed with cautious optimism based on the above factors."
    
    return {"final_report": report}

# =========================================================
# Executing the Flow
# =========================================================

def build_parallel_graph():
    print("Building Fan-out/Fan-in LangGraph...")
    
    workflow = StateGraph(ParallelState)
    
    # Register all nodes
    workflow.add_node("input", input_node)
    workflow.add_node("pros", analyze_pros)
    workflow.add_node("cons", analyze_cons)
    workflow.add_node("risks", analyze_risks)
    workflow.add_node("synthesis", synthesis_node)
    
    # Define Edges Flow
    workflow.add_edge(START, "input")
    
    # Highlight: Fan-Out. Add independent edges from 'input' to the parallel nodes.
    # LangGraph will automatically execute these concurrently!
    workflow.add_edge("input", "pros")
    workflow.add_edge("input", "cons")
    workflow.add_edge("input", "risks")
    
    # Highlight: Fan-In. Point all parallel nodes to the final synthesis node.
    # LangGraph automatically handles the barrier sync, waiting for all 3 to finish!
    workflow.add_edge("pros", "synthesis")
    workflow.add_edge("cons", "synthesis")
    workflow.add_edge("risks", "synthesis")
    
    # End edge
    workflow.add_edge("synthesis", END)
    
    return workflow.compile()

if __name__ == "__main__":
    app = build_parallel_graph()
    
    print("\n==========================================")
    print("Starting LangGraph Parallel Execution")
    print("==========================================\n")
    
    initial_state = {
        "topic": "Global Commercial Space Travel",
        "analysis_results": [],
        "final_report": ""
    }
    
    # Execution
    final_output = app.invoke(initial_state)
    
    print("\n==========================================")
    print("Final Output:\n")
    print(final_output["final_report"])
