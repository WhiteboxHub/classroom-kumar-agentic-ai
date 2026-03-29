import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- 1. Define Functions ---
def create_file(filename: str, content: str) -> str:
    """Create a new file with the specified content."""
    try:
        with open(filename, "w") as f:
            f.write(content)
        return f"Successfully created '{filename}'"
    except Exception as e:
        return f"Error creating file '{filename}': {e}"

def list_directory(path: str = ".") -> str:
    """List the contents of a given directory path."""
    try:
        files = os.listdir(path)
        return f"Contents of '{path}': {', '.join(files)}"
    except Exception as e:
        return f"Error listing directory '{path}': {e}"

# A dictionary to safely expose our available functions
AVAILABLE_FUNCTIONS = {
    "create_file": create_file,
    "list_directory": list_directory
}

# --- 2. Build the System Prompt ---
# The prompt explicitly teaches the LLM to output function calls in a specific text format.
SYSTEM_PROMPT = """
You are a helpful assistant. You can perform actions on the user's computer by calling specific functions.

You have access to the following Python functions:
1. create_file(filename, content) - Creates a file with the given content.
2. list_directory(path) - Lists files in the given path.

When you need to use a function to answer the user's request, you must output a text block in exactly this format:
<tool_call>function_name("arg1", "arg2")</tool_call>

You can perform one action at a time. The system will then run the function and give you the result.
If you know the answer without a tool, or after you have received the tool's output, simply reply in plain text.

Examples:
User: Please create a file named "greet.txt" that says "Hello".
Assistant: I will do that for you right now. 
<tool_call>create_file("greet.txt", "Hello")</tool_call>

User: What's inside the current folder?
Assistant: Let me check.
<tool_call>list_directory(".")</tool_call>
"""

def extract_and_execute_call(response_text: str) -> str:
    """
    Parses the response for a <tool_call> tag, extracts the function and arguments,
    and executes it dynamically.
    """
    # Regex to find <tool_call>...</tool_call>
    match = re.search(r"<tool_call>(.*?)</tool_call>", response_text, re.DOTALL)
    
    if match:
        # e.g., create_file('hello.txt', 'hello')
        call_string = match.group(1).strip()
        print(f"\n[Environment] Extracted tool call: {call_string}")
        
        # --- 3. Execute dynamically using code (e.g., eval()) ---
        # We use eval here with a restricted dictionary of available functions.
        try:
            print(f"[Environment] Executing dynamically...")
            # Evaluate the string as a Python expression mapping strictly to our functions
            result = eval(call_string, {"__builtins__": {}}, AVAILABLE_FUNCTIONS)
            return str(result)
        except Exception as e:
            return f"Execution Error: {e}"
            
    return None

def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Please set your OPENAI_API_KEY environment variable. You can use a .env file.")
        return

    client = OpenAI(api_key=api_key)
    print("Welcome to the Toolformer-style Agent (Type 'exit' to quit)\n")
    
    # Initialize conversation history with our custom system prompt instructions
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        messages.append({"role": "user", "content": user_input})
        
        # We loop to allow the agent to use a tool, get the result, and reply again.
        while True:
            response = client.chat.completions.create(
                model="gpt-4", # Or gpt-3.5-turbo if preferred
                messages=messages,
                temperature=0.0
            )
            
            assistant_reply = response.choices[0].message.content
            print(f"\nAssistant: {assistant_reply}")
            messages.append({"role": "assistant", "content": assistant_reply})
            
            # --- 4. Check if the LLM generated actions as text ---
            tool_result = extract_and_execute_call(assistant_reply)
            
            if tool_result is not None:
                # We have a result from the dynamic execution.
                print(f"[Environment Result]: {tool_result}")
                # We feed the simulated tool outcome back for the LLM to interpret.
                # Notice we treat the environment as "system" here because there are no native tool roles in this old approach.
                messages.append({
                    "role": "system", 
                    "content": f"Tool execution result: {tool_result}"
                })
            else:
                # No format detected, LLM is done with its turn.
                break

if __name__ == "__main__":
    main()
