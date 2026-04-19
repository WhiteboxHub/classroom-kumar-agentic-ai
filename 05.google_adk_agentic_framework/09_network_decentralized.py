"""
09_network_decentralized.py

Pattern 1: Network (Decentralized) in Google ADK
Agents are exposed as tools to one another organically enabling cross-communication.
"""
from google_adk.agents import Agent
from google_adk.tools import ToolRegistry

registry = ToolRegistry()

# To securely pass a peer agent in ADK, wrap its invocation.
@registry.register("consult_research", description="Talk to the Peer Research Agent.")
def consult_research(query: str) -> str:
    return f"[ResearchAgent] Addressed your inquiry: {query}"

@registry.register("consult_math", description="Talk to the Peer Math Agent.")
def consult_math(query: str) -> str:
    return f"[MathAgent] Addressed your inquiry: {query}"

def main():
    print("--- Google ADK Pattern: Network (Decentralized) ---")
    print("A general agent is granted tool access to manually bridge with sister agents.")
    
    # Initialize Agent A with Peer capabilities
    agent_a = Agent(
        name="GeneralAgent",
        instruction="Route to the appropriate peer agent natively.",
        tools=[registry.get_tool("consult_research"), registry.get_tool("consult_math")]
    )
    
    print("\nAgent A successfully mapped with peer-to-peer delegation vectors.")

if __name__ == "__main__":
    main()
