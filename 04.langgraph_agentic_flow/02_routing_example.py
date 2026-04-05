# Copyright (c) 2025 Marco Fago
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from typing import TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

# --- Core State Definition ---
class AgentState(TypedDict):
    request: str
    decision: str
    result: str

# --- LLM Node: Coordinator Classifier ---
def classify_request(state: AgentState) -> dict:
    """Uses LLM to classify the intent to decide routing."""
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    except Exception as e:
        print(f"Error initializing language model: {e}")
        return {"decision": "unclear"}
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Analyze the user's request and determine which specialist handler should process it.
        - If the request is related to booking flights or hotels, output 'booker'.
        - For all other general information questions, output 'info'.
        - If the request is unclear or doesn't fit either category, output 'unclear'.
        ONLY output one word: 'booker', 'info', or 'unclear'."""),
        ("user", "{request}")
    ])
    
    chain = prompt | llm
    
    try:
        decision = chain.invoke({"request": state["request"]}).content.strip().lower()
    except Exception as e:
        decision = "unclear"
        
    return {"decision": decision}

# --- Define Simulated Sub-Agent Handlers ---
def booking_handler(state: AgentState) -> dict:
    """Simulates the Booking Agent handling a request."""
    print("\n--- DELEGATING TO BOOKING HANDLER ---")
    return {"result": f"Booking Handler processed request: '{state['request']}'. Result: Simulated booking action."}

def info_handler(state: AgentState) -> dict:
    """Simulates the Info Agent handling a request."""
    print("\n--- DELEGATING TO INFO HANDLER ---")
    return {"result": f"Info Handler processed request: '{state['request']}'. Result: Simulated information retrieval."}

def unclear_handler(state: AgentState) -> dict:
    """Handles requests that couldn't be delegated."""
    print("\n--- HANDLING UNCLEAR REQUEST ---")
    return {"result": f"Coordinator could not delegate request: '{state['request']}'. Please clarify."}

# --- Router Logic ---
def route_decision(state: AgentState) -> Literal["booker", "info", "unclear"]:
    """Conditional routing based on LLM decision output."""
    decision = state.get("decision", "unclear")
    if decision == "booker":
        return "booker"
    elif decision == "info":
        return "info"
    return "unclear"

# --- Define State Graph ---
builder = StateGraph(AgentState)

# Add Nodes
builder.add_node("classify", classify_request)
builder.add_node("booker", booking_handler)
builder.add_node("info", info_handler)
builder.add_node("unclear", unclear_handler)

# Add Edges
builder.add_edge(START, "classify")

builder.add_conditional_edges(
    "classify",
    route_decision,
    {
        "booker": "booker",   # Maps logic return string to node name
        "info": "info",
        "unclear": "unclear"
    }
)

builder.add_edge("booker", END)
builder.add_edge("info", END)
builder.add_edge("unclear", END)

# Compile framework into a runnable application
app = builder.compile()

# --- Example Usage ---
def main():
    print("--- LangGraph Routing Example ---")
    
    print("\n--- Running with a booking request ---")
    request_a = "Book me a flight to London."
    result_a = app.invoke({"request": request_a})
    print(f"Final Result A: {result_a['result']}")
    
    print("\n--- Running with an info request ---")
    request_b = "What is the capital of Italy?"
    result_b = app.invoke({"request": request_b})
    print(f"Final Result B: {result_b['result']}")
    
    print("\n--- Running with an unclear request ---")
    request_c = "Tell me about quantum physics."
    result_c = app.invoke({"request": request_c})
    print(f"Final Result C: {result_c['result']}")

if __name__ == "__main__":
    main()
