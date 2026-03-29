import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- 1. Define Functions (Same as Example 01) ---
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

# A dictionary to map the tool names back to actual Python functions
AVAILABLE_FUNCTIONS = {
    "create_file": create_file,
    "list_directory": list_directory
}

# --- 2. Provide functions as structured definitions (JSON Schema format) ---
# The OpenAI Native API relies on structured definitions natively rather than prompt injection.
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Create a new file with the specified text content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name or path of the file to create, e.g., 'hello.txt'."
                    },
                    "content": {
                        "type": "string",
                        "description": "The text content to write into the file."
                    }
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List the contents of a given directory path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to list, e.g., '.' for current directory."
                    }
                },
                "required": ["path"]
            }
        }
    }
]

def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Please set your OPENAI_API_KEY environment variable. You can use a .env file.")
        return

    client = OpenAI(api_key=api_key)
    print("Welcome to the OpenAI Native Function Calling Agent (Type 'exit' to quit)\n")
    
    # We NO LONGER need to teach the LLM string formatting inside the prompt.
    # The API structure inherently handles this.
    messages = [
        {"role": "system", "content": "You are a helpful assistant. You have tools available to assist with computer capabilities."}
    ]
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        messages.append({"role": "user", "content": user_input})
        
        # Iteration Loop: The LLM could potentially trigger multiple consecutive tool queries.
        while True:
            # --- 3. Model decides when to call them ---
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # Or gpt-4
                messages=messages,
                tools=tools,
                tool_choice="auto", # Allows the model to decide if a tool should be executed
                temperature=0.0
            )
            
            response_message = response.choices[0].message
            
            # Did the model decide to invoke a tool?
            if response_message.tool_calls:
                print("\n[AI] Decided to invoke external capability...")
                
                # Natively push the "assistant's request" onto the history stack 
                messages.append(response_message)
                
                # --- 4. Returns arguments as JSON ---
                # Iterate through any tools the LLM requested.
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = AVAILABLE_FUNCTIONS.get(function_name)
                    
                    if function_to_call:
                        # Arguments are nicely formatted as a loaded JSON dictionary
                        function_args = json.loads(tool_call.function.arguments)
                        print(f"    [Environment] Calling `{function_name}` with arguments: {function_args}")
                        
                        # --- 5. Execute function safely in code ---
                        if function_name == "create_file":
                            function_response = function_to_call(
                                filename=function_args.get("filename"),
                                content=function_args.get("content")
                            )
                        elif function_name == "list_directory":
                            function_response = function_to_call(
                                path=function_args.get("path", ".")
                            )
                            
                        print(f"    [Environment Result]: {function_response}")
                        
                        # --- 6. Feed result back to model ---
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        })
                    else:
                        print(f"    [Environment Error] Model requested unknown function: {function_name}")
                
            else:
                # No tools initiated, just print the standard chat reply
                assistant_reply = response_message.content
                print(f"Assistant: {assistant_reply}")
                messages.append({"role": "assistant", "content": assistant_reply})
                break # Exit inner tool invocation loop to wait for new user input
                
if __name__ == "__main__":
    main()
