# 01 - Vanilla Text-to-Action Framework (Toolformer Approach)

This folder contains a simple classroom example demonstrating how early agentic frameworks (inspired by papers like [Toolformer](https://arxiv.org/abs/2302.04761) or ReAct) connected Large Language Models to external functions *without* relying on specialized framework abstractions like LangChain, LlamaIndex, or native OpenAI Function Calling API.

## Core Concepts (How It Works)

1. **Define functions:** 
   We define typical Python functions to represent our tools (e.g., `create_file()`, `list_directory()`).
2. **Prompts define the API:** 
   The exact tool usage format is embedded into the `System Prompt`. The LLM is literally taught how to format a string in order to invoke an action, e.g., `<tool_call>function_name("arg1", "arg2")</tool_call>`.
3. **Parse and Execute Dynamically:** 
   Code continuously intercepts the AI's textual response, searches for the parsed string format utilizing Regex, and crucially executes it **dynamically** (using python's `eval()` mapped directly to predefined callable functions). 
4. **Iterative Feedback Loop:** 
   The result from the environment is appended back to the conversation stack so the LLM receives the outcome and reasons the next steps towards answering the query.

## Explaining The Files
- `01.llm_function_call_in_prompt.py`: High Level Concept — The foundational baseline demonstrating how early iteration language models interact purely with raw textual tags implicitly mapped into functional Python logic. Focuses on the manual `eval()` mapping without abstracted APIs.
- `requirements.txt`: Explicit Python package requirements.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Establish your `OPENAI_API_KEY`:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   *(Or just place it inside a `.env` file in the same directory using `OPENAI_API_KEY=your-api-key`)*

3. Run the application:
   ```bash
   python 01.llm_function_call_in_prompt.py
   ```

## Example interactions
Once running the agent, try prompting:
- *"What's inside the current directory?"*
- *"Can you create a file called notes.txt with the content 'Agentic AI class is starting'?"*
- *"Based on what's in this directory, what files have the suffix '.py'?"*
