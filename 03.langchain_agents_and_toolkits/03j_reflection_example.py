"""
03j_reflection_example.py
This script demonstrates an AI reflection loop (also known as a critic or self-correction loop)
to progressively improve a generated Python function.

The process:
1. Start with a task prompt.
2. Generate initial code.
3. Iteratively reflect on the code using a simulated "senior software engineer" critique.
4. Refine the code based on the critiques.
5. Stop when the code is deemed perfect or the maximum number of iterations is reached.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# --- Configuration ---
# Load environment variables from .env file (for OPENAI_API_KEY)
load_dotenv()

# Check if the API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")

# Initialize the Chat LLM. We use gpt-4o for its advanced reasoning capabilities.
# A temperature of 0.1 is used to ensure more deterministic and consistent outputs.
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

def run_reflection_loop():
    """
    Executes a multi-step AI reflection loop to iteratively write and 
    improve a Python function that calculates factorials.
    """
    
    # ==========================================
    # 1. Define the Core Task
    # ==========================================
    task_prompt = """
    Your task is to create a Python function named `calculate_factorial`.
    This function should do the following:
    1. Accept a single integer `n` as input.
    2. Calculate its factorial (n!).
    3. Include a clear docstring explaining what the function does.
    4. Handle edge cases: The factorial of 0 is 1.
    5. Handle invalid input: Raise a ValueError if the input is a negative number.
    """

    # ==========================================
    # 2. Setup the Reflection Loop
    # ==========================================
    max_iterations = 3
    current_code = ""
    
    # We maintain a conversation history to provide context of the task, previous code,
    # and previous critiques during each iteration.
    message_history = [HumanMessage(content=task_prompt)]

    for i in range(max_iterations):
        print(f"\n{'='*25} REFLECTION LOOP: ITERATION {i + 1} {'='*25}")

        # ------------------------------------------
        # STAGE 1: GENERATE / REFINE
        # ------------------------------------------
        # First iteration generates the initial code. 
        # Subsequent iterations refine it based on previous critiques.
        if i == 0:
            print("\n>>> STAGE 1: GENERATING initial code...")
            response = llm.invoke(message_history)
            current_code = response.content
        else:
            print("\n>>> STAGE 1: REFINING code based on previous critique...")
            # Instruct the model to apply the critiques found during the Reflection stage.
            message_history.append(HumanMessage(content="Please refine the code using the critiques provided."))
            response = llm.invoke(message_history)
            current_code = response.content

        print(f"\n--- Generated Code (v{i + 1}) ---\n{current_code}")
        
        # Add the generated code to history so the loop has context of the current state
        message_history.append(response)

        # ------------------------------------------
        # STAGE 2: REFLECT (Critique)
        # ------------------------------------------
        print("\n>>> STAGE 2: REFLECTING on the generated code...")
        
        # Create a specific prompt for the reflector agent. This agent acts as a strict reviewer.
        reflector_prompt = [
            SystemMessage(content="""
            You are a senior software engineer and an expert in Python.
            Your role is to perform a meticulous code review.
            Critically evaluate the provided Python code based on the original task requirements.
            Look for bugs, style issues, missing edge cases, and areas for improvement.
            If the code is perfect and meets all requirements, respond with the single phrase 'CODE_IS_PERFECT'.
            Otherwise, provide a bulleted list of your critiques.
            """),
            HumanMessage(content=f"Original Task:\n{task_prompt}\n\nCode to Review:\n{current_code}")
        ]

        critique_response = llm.invoke(reflector_prompt)
        critique = critique_response.content

        # ------------------------------------------
        # STAGE 3: STOPPING CONDITION
        # ------------------------------------------
        if "CODE_IS_PERFECT" in critique:
            print("\n--- Critique ---\nNo further critiques found. The code is satisfactory based on requirements.")
            break
            
        print("\n--- Critique ---\n" + critique)
        
        # Add the critique to the history so the next refinement loop knows what to fix.
        message_history.append(HumanMessage(content=f"Critique of the previous code:\n{critique}"))

    # ==========================================
    # 3. Final Output
    # ==========================================
    print("\n" + "="*30 + " FINAL RESULT " + "="*30)
    print("\nFinal refined code after the reflection process:\n")
    print(current_code)

if __name__ == "__main__":
    run_reflection_loop()
