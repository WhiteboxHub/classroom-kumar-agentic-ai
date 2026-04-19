"""
07_tool_api_call.py
Demonstrates the tool use pattern with an API Call simulation using Google ADK.
"""
from google_adk.agents import Agent
from google_adk.tools import ToolRegistry
from google_adk.llms import GoogleGenAIModel

# Initialize the centralized ADK tool registry
registry = ToolRegistry()

@registry.register("fetch_api_data", description="Makes a RESTful API call to the system backend to fetch JSON data.")
def fetch_api_data(endpoint: str) -> str:
    print(f"\n--- 🌐 Tool Called: fetch_api_data for endpoint: '{endpoint}' ---")
    simulated_results = {
        "/users/1": '{"id": 1, "name": "John Doe", "email": "john@example.com"}',
        "/products/recent": '[{"id": 101, "item": "Laptop"}, {"id": 102, "item": "Keyboard"}]',
        "/status": '{"status": "online", "uptime": "99.99%"}',
        "default": '{"error": "404 - Endpoint not found or permission denied"}'
    }
    result = simulated_results.get(endpoint.strip(), simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result

def main():
    print("--- Initializing Google ADK Agent ---")
    try:
        model = GoogleGenAIModel(model_name="gemini-2.0-flash")
    except Exception as e:
        print(f"🛑 Error initializing language model: {e}")
        return

    # Create the ADK Agent, passing directly the tool from the registry
    agent = Agent(
        name="APIAssistant",
        instruction="You are an API integration assistant. Fetch data using provided endpoints to answer questions.",
        tools=[registry.get_tool("fetch_api_data")],
        model=model
    )

    queries = [
        "Can you get the user details for user ID 1?",
        "Fetch the recent products from the API, what's available?",
        "Check if the billing API /billing/1 is active."
    ]

    for q in queries:
        print(f"\n--- 🏃 Running Agent with Query: '{q}' ---")
        try:
             # We map the invocation back to agent.run(task=) natively
            response = agent.run(task=q)
            print("\n--- ✅ Final Agent Response ---")
            print(response)
        except Exception as e:
            print(f"\n🛑 An error occurred during agent execution: {e}")

if __name__ == "__main__":
    main()
