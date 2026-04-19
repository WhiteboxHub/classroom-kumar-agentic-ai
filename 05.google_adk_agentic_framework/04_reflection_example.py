"""
04_reflection_example.py

This script demonstrates the use of a sequential agent pipeline in Google ADK 
for generating and reviewing text, acting as a one-pass Reflection architecture.

Execution Flow:
1. `generator` runs -> saves its paragraph to state['draft_text'].
2. `reviewer` runs -> reads state['draft_text'] and saves its dictionary output to state['review_output'].

The overall execution flow is that the generator produces text, which is then saved 
to the state. Subsequently, the reviewer reads this text from the state, performs 
its fact-checking, and saves its findings (the status and reasoning) back to the state. 
This pipeline allows for a structured process of content creation and review using 
separate agents.

Note: An alternative implementation utilizing ADK's `LoopAgent` is also available 
for those interested in continuous multi-turn self-correction loops.
"""

from google.adk.agents import SequentialAgent, LlmAgent

# Standard ADK Configuration
GEMINI_MODEL = "gemini-2.0-flash"

# ==========================================
# 1. Define the Generator Node
# ==========================================
# The first agent generates the initial draft.
generator = LlmAgent(
    name="DraftWriter",
    model=GEMINI_MODEL,
    description="Generates initial draft content on a given subject.",
    instruction="Write a short, informative paragraph about the user's subject.",
    output_key="draft_text"  # The output is saved to this state key.
)

# ==========================================
# 2. Define the Reviewer Node
# ==========================================
# The second agent critiques the draft from the first agent.
reviewer = LlmAgent(
    name="FactChecker",
    model=GEMINI_MODEL,
    description="Reviews a given text for factual accuracy and provides a structured critique.",
    instruction="""
    You are a meticulous fact-checker.
    1. Read the text provided in the state key 'draft_text' below.
    2. Carefully verify the factual accuracy of all claims.
    3. Your final output must be a dictionary containing two keys:
       - "status": A string, either "ACCURATE" or "INACCURATE".
       - "reasoning": A string providing a clear explanation for your
         status, citing specific issues if any are found.
         
    Evaluate the following draft:
    {draft_text}
    """,
    output_key="review_output"  # The structured dictionary is saved here.
)

# ==========================================
# 3. Create the Reflection Pipeline
# ==========================================
# The SequentialAgent ensures the generator runs before the reviewer.
review_pipeline = SequentialAgent(
    name="WriteAndReview_Pipeline",
    sub_agents=[generator, reviewer],
    description="Manages the execution order of the generation and review agents sequentially."
)

if __name__ == "__main__":
    print("\n--- Initializing Google ADK Sequential Reflection Pipeline ---")
    print("This pipeline allows for a structured process of content creation and review.")
    print("Step 1: The 'DraftWriter' agent generates an informative paragraph.")
    print("Step 2: The 'FactChecker' agent verifies its accuracy and outputs JSON.")
    print("\nPipeline Created. Enable ADK environment and call `review_pipeline.run()`.")
    
    # ==========================
    # Example Execution Context
    # ==========================
    # Assuming runtime execution:
    # result_state = review_pipeline.run("The history of quantum computing")
    # 
    # print("\nDraft Text Generated:")
    # print(result_state.get('draft_text'))
    #
    # print("\nFact Check Review:")
    # print(result_state.get('review_output'))
