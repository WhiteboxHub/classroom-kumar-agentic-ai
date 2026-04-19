"""
05_tool_google_search.py
Demonstrates the tool use pattern with a Google Search simulation using Google ADK.
"""
from google_adk.agents import Agent
from google_adk.tools import ToolRegistry
from google_adk.llms import GoogleGenAIModel

# Initialize the centralized ADK tool registry
registry = ToolRegistry()

@registry.register("google_search", description="Provides factual information from the web on a given topic.")
def google_search(query: str) -> str:
    print(f"\n--- 🔍 Tool Called: google_search with query: '{query}' ---")
    simulated_results = {
        "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
        "capital of france": "The capital of France is Paris.",
        "population of earth": "The estimated population of Earth is around 8 billion people.",
        "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
        "default": f"Simulated search result for '{query}': No specific information found on the web."
    }
    result = simulated_results.get(query.lower(), simulated_results["default"])
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
        name="SearchAssistant",
        instruction="You are a helpful assistant mapping questions to search queries. Use the search tool provided.",
        tools=[registry.get_tool("google_search")],
        model=model
    )

    queries = [
        "What is the capital of France?",
        "What's the weather like in London?",
        "Tell me something about dogs."
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
