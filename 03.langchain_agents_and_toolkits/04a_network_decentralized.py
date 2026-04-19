"""
04a_network_decentralized.py

Pattern 1: Network (Decentralized)
Demonstrates peer-to-peer communication among agents in LangChain.
Agents operate without a central hub, directly invoking each other using equipped tools.
"""
from langchain_core.tools import tool

# Simulate Peer Agent B (Research)
@tool
def consult_research_agent(query: str) -> str:
    """Agent A calls this to speak to Agent B for detailed research."""
    return f"[ResearchAgent]: Analyzed data for '{query}'."

# Simulate Peer Agent C (Math)
@tool
def consult_math_agent(equation: str) -> str:
    """Agent A calls this to speak to Agent C for calculations."""
    return f"[MathAgent]: Calculated '{equation}' successfully."

def main():
    print("--- LangChain Pattern: Network (Decentralized) ---")
    print("Agents operate globally. Agent A is equipped with tools representing Agent B and C.")
    
    # In a full setup, these would be bound to a create_tool_calling_agent
    tools = [consult_research_agent, consult_math_agent]
    
    print("\nSimulating Execution:")
    print("Agent A receives task -> Requires math -> peer-to-peer calls MathAgent directly.")
    print(consult_math_agent.invoke("100 * 4"))

if __name__ == "__main__":
    main()
