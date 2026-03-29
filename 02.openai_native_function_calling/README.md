# 02 - OpenAI Function Calling API

This folder demonstrates the modern "standard way" to connect Large Language Models with external tools, bypassing the need for explicit text parsing formats (like implemented in Example `01`), by leveraging OpenAI's native API parameter bindings.

## How It Works:

1. **Provide functions as structured definitions:**
   Instead of formatting the LLM's system prompt to write HTML-like tags, we pass an explicit JSON schema describing our Python dictionary implementations (`create_file`, `list_directory`) natively via the `tools=[...]` API payload.
2. **Model decides when to call them:**
   The language model internally utilizes its optimized instruction tuning to dictate when a query warrants external augmentation, triggering an internal decision flag automatically (`tool_choice="auto"`).
3. **Returns arguments as JSON:**
   If it decides it needs a tool, the API's response bypasses raw string completion. Instead, it surfaces structured objects (`response_message.tool_calls`) where arguments are reliably guaranteed to be valid JSON strings, neutralizing Regex fragility.
4. **Execute function safely in code:**
   Our Python routine directly references the exact mapped system function via `AVAILABLE_FUNCTIONS.get(function_name)` and passes the native `json.loads` dictionary components; significantly abstracting dangerous dynamic `eval()` workflows. 
5. **Feed result back to model:**
   The executed code result is formally appended back to context using the dedicated `"role": "tool"`. The LLM naturally recognizes this external metadata injection, interpolates the context, and derives its conclusive answer for the end-user.

## Files
- `02.openai_function_calling.py`: Contains the logic demonstrating native Function Calling with the exact same two functions from previous classroom modules.
- `requirements.txt`: Python package requirements.

## How to Run

1. Change directory and install dependencies:
   ```bash
   cd 02
   pip install -r requirements.txt
   ```

2. Establish your `OPENAI_API_KEY`:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. Run the interactive classroom script:
   ```bash
   python 02.openai_function_calling.py
   ```
