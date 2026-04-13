"""
05. Parallelization Example (LangChain)
---------------------------------------
This example demonstrates how to run multiple independent tasks concurrently
using LangChain's Expression Language (LCEL). We use RunnableParallel to execute
three distinct LLM queries (summarize, generate questions, identify key terms)
at the same time, and then synthesize their results into a final response.

Core Classes highlighted:
- ChatOpenAI: The LLM interface for interacting with OpenAI.
- ChatPromptTemplate: Defines the structure of the input prompts.
- StrOutputParser: Parses the LLM's raw output stream into a string.
- RunnableParallel: Executes multiple runnables (chains) in parallel.
- RunnablePassthrough: Passes input unchanged to the next step.
"""

import os
import asyncio
from typing import Optional

# Highlight: Core LangChain Modules
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough

# --- 1. Configuration ---
# Ensure your API key environment variable is set (e.g., OPENAI_API_KEY)
llm: Optional[ChatOpenAI] = None
try:
    # Highlight: ChatOpenAI initialization
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
except Exception as e:
    print(f"Error initializing language model: {e}")

# --- 2. Define Independent Chains ---
# These three chains represent distinct tasks that can be executed concurrently.
# Highlight: Using LCEL (|) to pipeline prompt -> LLM -> parser

summarize_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Summarize the following topic concisely:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

questions_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Generate three interesting questions about the following topic:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

terms_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Identify 5-10 key terms from the following topic, separated by commas:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

# --- 3. Build the Parallel + Synthesis Chain ---

# Step A: Define the block of tasks to run in parallel.
# Highlight: RunnableParallel maps multiple keys to concurrently executed runnables.
map_chain = RunnableParallel(
    {
        "summary": summarize_chain,
        "questions": questions_chain,
        "key_terms": terms_chain,
        
        # Highlight: Pass the original topic through without modification
        "topic": RunnablePassthrough(),
    }
)

# Step B: Define the final synthesis prompt which combines the parallel results.
synthesis_prompt = ChatPromptTemplate.from_messages([
    ("system", """Based on the following information:
    
Summary: {summary}
Related Questions: {questions}
Key Terms: {key_terms}

Synthesize a comprehensive answer."""),
    ("user", "Original topic: {topic}")
])

# Step C: Construct the full execution chain.
# The `map_chain` produces a dictionary of results, which is pipelined into `synthesis_prompt`.
full_parallel_chain = map_chain | synthesis_prompt | llm | StrOutputParser()

# --- 4. Execution ---
async def run_parallel_example(topic: str) -> None:
    """
    Asynchronously invokes the parallel processing chain with a specific topic
    and prints the synthesized result.
    """
    if not llm:
        print("LLM not initialized. Cannot run example.")
        return

    print(f"\n--- Running Parallel LangChain Example for Topic: '{topic}' ---")
    try:
        # Highlight: ainvoke allows asynchronous execution of the entire chain,
        # which is critical for actually reaping the concurrency benefits of RunnableParallel
        response = await full_parallel_chain.ainvoke(topic)
        
        print("\n--- Final Response ---")
        print(response)
    except Exception as e:
        print(f"\nAn error occurred during chain execution: {e}")

if __name__ == "__main__":
    test_topic = "The history of space exploration"
    
    # Highlight: Standard asyncio loop execution to run the coroutine
    asyncio.run(run_parallel_example(test_topic))
