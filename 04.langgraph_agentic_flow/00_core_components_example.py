"""
LangGraph Intro: Internal Components and Flow

Core Modules:
- StateGraph: The primary orchestrator. It defines the structure (nodes/edges) and the schema of the shared state.
- Nodes: Regular Python functions. They take the current State as input and return a State Update (e.g., adding a new message).
- Edges: Define the transition. Conditional Edges use a "router" function to decide the next node based on the model's output.
- Checkpointer: A persistence layer (e.g., MemorySaver) that saves the state after every node, enabling "Time Travel" and error recovery.

Core Components:
- State Object: Shared data structure passed across all nodes
- Nodes: Units of execution, can be LLM calls, tools, or custom logic
- Edges: Define transitions between nodes, support branching and loops
- Router Logic: Decides next node based on state or LLM output
- Executor Runtime: Manages execution order, retries, and state updates
- Memory Integration: Maintains context across iterations

Simple Example: Task Automation Agent
Goal: "Summarize latest AI news and send email"
Flow:
1. Input Node receives query
2. Planner Node breaks into steps
3. Tool Node fetches news via API
4. LLM Node summarizes content
5. Action Node sends email
"""

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# ---------------------------------------------------------
# Core Component: State Object
# ---------------------------------------------------------
class AgentState(TypedDict):
    """Shared data structure passed across all nodes."""
    query: str
    steps: List[str]
    news_content: str
    summary: str
    email_status: str

# ---------------------------------------------------------
# Core Component: Nodes
# (Units of execution)
# ---------------------------------------------------------

# 1. Input Node is implicitly handled by passing initial state at START

def planner_node(state: AgentState):
    """2. Planner Node: Breaks into steps."""
    print("--- Node: Planner ---")
    query = state.get("query", "")
    print(f"Goal: '{query}'")
    
    # State Update
    return {
        "steps": [
            "Fetch latest AI news",
            "Summarize the news content",
            "Draft and send email with summary"
        ]
    }

def tool_node(state: AgentState):
    """3. Tool Node: Fetches news via API (Mocked)."""
    print("--- Node: Tool Execution ---")
    print("Fetching news via simulated API...")
    
    simulated_news = (
        "OpenAI releases new reasoning model. "
        "LangChain announces LangGraph improved checkpointer. "
        "Google introduces new Gemma 2 weights."
    )
    
    # State Update
    return {"news_content": simulated_news}

def llm_node(state: AgentState):
    """4. LLM Node: Summarizes content."""
    print("--- Node: LLM Summarization ---")
    content = state.get("news_content", "")
    print("Summarizing content...")
    
    # Mocking LLM summarization for simplicity
    summary = "\n".join([f"- {sentence.strip()}" for sentence in content.split(".") if sentence.strip()])
        
    # State Update
    return {"summary": summary}
    
def action_node(state: AgentState):
    """5. Action Node: Sends email."""
    print("--- Node: Action (Send Email) ---")
    summary = state.get("summary", "")
    print("\nDrafting email...")
    print(f"Subject: Latest AI News Summary\nBody:\n{summary}")
    print("Email sent successfully!")
    
    # State Update
    return {"email_status": "Success"}

# ---------------------------------------------------------
# Core Component: Router Logic
# ---------------------------------------------------------
def route_after_summary(state: AgentState) -> str:
    """Decides next node based on state."""
    print("--- Router Logic ---")
    summary = state.get("summary", "")
    
    if not summary:
        print("Router Decision: Summary empty -> Route to END")
        return "end"
    
    print("Router Decision: Summary present -> Route to Action (send_email)")
    return "send_email"

# =========================================================
# Executing the Flow (StateGraph setup & Executor Runtime)
# =========================================================

def build_and_run_graph():
    print("Initializing StateGraph...")
    # Initialize StateGraph with the shared state schema
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("tool", tool_node)
    workflow.add_node("summarize", llm_node)
    workflow.add_node("send_email", action_node)

    # Core Component: Edges (Define transitions)
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "tool")
    workflow.add_edge("tool", "summarize")

    # Core Component: Conditional Edges (Branching based on router)
    workflow.add_conditional_edges(
        "summarize",            # Starting node
        route_after_summary,    # Router function
        {
            "send_email": "send_email", # if router returns "send_email", go to "send_email" node
            "end": END                  # if router returns "end", go to END
        }
    )

    workflow.add_edge("send_email", END)

    # Core Component: Memory Integration (Checkpointer)
    memory_saver = MemorySaver()

    # Executor Runtime: Compile graph with Checkpointer
    # This enables Time Travel and error recovery by saving state at every step
    app = workflow.compile(checkpointer=memory_saver)

    print("\n==========================================")
    print("Executing Task Automation Agent Flow")
    print("==========================================\n")
    
    # Thread config is required for memory checkpointer
    config = {"configurable": {"thread_id": "thread-1"}}
    initial_state = {"query": "Summarize latest AI news and send email"}
    
    # Stream execution
    for event in app.stream(initial_state, config=config):
        # The execution automatically handles order and state updates.
        pass 
        
    print("\n==========================================")
    print("Execution Complete!")
    print("Final State Memory Snapshot:")
    
    final_state = app.get_state(config)
    for key, value in final_state.values.items():
         print(f"  {key}: {value}")

if __name__ == "__main__":
    build_and_run_graph()
