"""
04_reflection_example.py

This script demonstrates an AI reflection loop using LangGraph.
It replicates the self-correction loop where an agent generates code,
and a "senior software engineer" agent critiques it until it's perfect
or hits a max iteration limit.

Core LangGraph components used:
- StateGraph: To manage the flow of data (task, code, critiques, counters).
- Nodes ('generate', 'reflect'): Representing the distinct LLM calls.
- Conditional Edges: To define when the loop should break (perfection or timeout).
"""

import os
from typing import TypedDict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

# --- Configuration ---
# Load environment variables from .env file (for OPENAI_API_KEY)
load_dotenv()

# Check if the API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")

# Initialize the Chat LLM. We use gpt-4o for its advanced reasoning capabilities.
# A temperature of 0.1 is used to ensure more deterministic and consistent outputs.
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

# ==========================================
# 1. Define the State
# ==========================================
class ReflectionState(TypedDict):
    """
    The State dictates what information is dynamically passed 
    between nodes in the graph as execution progresses.
    """
    task: str
    current_code: str
    critique: str
    iterations: int

# ==========================================
# 2. Define the Nodes
# ==========================================

def generate_node(state: ReflectionState) -> ReflectionState:
    """
    Node responsible for generating or refining the Python code.
    If it's the first iteration, it creates code from the task.
    If it's a subsequent iteration, it refines the code using the critique.
    """
    task = state["task"]
    current_code = state.get("current_code", "")
    critique = state.get("critique", "")
    iterations = state.get("iterations", 0)

    print(f"\n{'='*25} REFLECTION LOOP: ITERATION {iterations + 1} {'='*25}")

    messages = [HumanMessage(content=task)]
    
    if current_code and critique:
        print("\n>>> STAGE 1: REFINING code based on previous critique...")
        # Add context from the previous state for accurate refinement
        messages.append(SystemMessage(content=f"Previous Code:\n{current_code}\n\nCritique to apply:\n{critique}"))
        messages.append(HumanMessage(content="Please refine the code using the critiques provided."))
    else:
        print("\n>>> STAGE 1: GENERATING initial code...")

    # Invoke the language model
    response = llm.invoke(messages)
    new_code = response.content

    print(f"\n--- Generated Code (v{iterations + 1}) ---\n{new_code}")

    # Return key-value pairs that need to be updated in the State
    return {
        "current_code": new_code, 
        "iterations": iterations + 1
    }

def reflect_node(state: ReflectionState) -> ReflectionState:
    """
    Node responsible for critiquing the generated code.
    Acts as a senior software engineer providing structured feedback.
    """
    print("\n>>> STAGE 2: REFLECTING on the generated code...")
    
    task = state["task"]
    current_code = state["current_code"]

    reflector_prompt = [
        SystemMessage(content="""
        You are a senior software engineer and an expert in Python.
        Your role is to perform a meticulous code review.
        Critically evaluate the provided Python code based on the original task requirements.
        Look for bugs, style issues, missing edge cases, and areas for improvement.
        If the code is perfect and meets all requirements, respond with the single phrase 'CODE_IS_PERFECT'.
        Otherwise, provide a bulleted list of your critiques.
        """),
        HumanMessage(content=f"Original Task:\n{task}\n\nCode to Review:\n{current_code}")
    ]

    response = llm.invoke(reflector_prompt)
    critique = response.content

    if "CODE_IS_PERFECT" in critique:
        print("\n--- Critique ---\nNo further critiques found. The code is satisfactory based on requirements.")
    else:
        print("\n--- Critique ---\n" + critique)

    # Return updated critique to be saved in the State
    return {"critique": critique}

# ==========================================
# 3. Define the Conditional Routing Logic
# ==========================================

def should_continue(state: ReflectionState) -> str:
    """
    Conditional logic to determine the next step after reflection.
    Returns the string name of the next node to mathematically execute.
    """
    critique = state["critique"]
    iterations = state["iterations"]
    max_iterations = 3

    if "CODE_IS_PERFECT" in critique:
        # Code is perfect, exit the loop
        return END
    elif iterations >= max_iterations:
        # Reached limit, forcefully exit the loop
        print(f"\n[INFO] Reached max iterations ({max_iterations}). Stopping reflection loop.")
        return END
    else:
        # Back to generation/refinement
        return "generate"

# ==========================================
# 4. Build and Compile the Graph
# ==========================================

def compile_reflection_graph():
    """
    Assembles the state, nodes, and edges into an executable LangGraph app.
    """
    # Initialize the graph builder with the custom TypedDict state
    builder = StateGraph(ReflectionState)

    # Add the operational nodes
    builder.add_node("generate", generate_node)
    builder.add_node("reflect", reflect_node)

    # Define the core flow schema
    # Execution begins at START and immediately enters 'generate' node
    builder.add_edge(START, "generate")
    # 'generate' deterministically proceeds to 'reflect'
    builder.add_edge("generate", "reflect")
    
    # After 'reflect', we execute conditional logic to decide the next outcome.
    builder.add_conditional_edges(
        "reflect",
        should_continue,
        {
            # A map between exact strings returned by `should_continue` 
            # and the name of the next target node.
            "generate": "generate",
            END: END
        }
    )

    # Compile the graph architecture into a runnable application
    return builder.compile()

# ==========================================
# 5. Run the Workflow
# ==========================================

def main():
    task_prompt = """
    Your task is to create a Python function named `calculate_factorial`.
    This function should do the following:
    1. Accept a single integer `n` as input.
    2. Calculate its factorial (n!).
    3. Include a clear docstring explaining what the function does.
    4. Handle edge cases: The factorial of 0 is 1.
    5. Handle invalid input: Raise a ValueError if the input is a negative number.
    """

    print("--- Starting LangGraph Reflection Loop ---")
    graph = compile_reflection_graph()

    # Pass the seed data to jumpstart the pipeline 
    initial_state = {
        "task": task_prompt,
        "current_code": "",
        "critique": "",
        "iterations": 0
    }

    # Execute the core workflow starting with the initial_state
    final_state = graph.invoke(initial_state)

    print("\n" + "="*30 + " FINAL RESULT " + "="*30)
    print("\nFinal refined code after the reflection process:\n")
    print(final_state["current_code"])

if __name__ == "__main__":
    main()
