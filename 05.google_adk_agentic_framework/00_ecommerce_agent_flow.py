"""
Google ADK Intro: Internal Components and Flow using Google ADK Framework

Core Modules Used:
- Agent: The base unit containing a name, instruction, and tools.
- SequentialAgent: Orchestrator running sub-agents in a fixed order.
- SessionService: Manages lifecycle and rewinds.

Simple Example: E-commerce Agent
Goal: "Launch a trending product store"
"""

import os
# Importing directly from the Google ADK framework
from google_adk.agents import Agent, SequentialAgent
from google_adk.memory import SessionService
from google_adk.tools import ToolRegistry
from google_adk.llms import GoogleGenAIModel  

def setup_ecommerce_flow():
    # 1. Integration Layer & Tool Registry
    registry = ToolRegistry()
    
    @registry.register("fetch_trends", description="Fetch trending products from Search APIs")
    def fetch_trends(query: str) -> str:
        # Mocking Vertex Search or Trends API
        return f"Top trending item for '{query}': Smart Home Gadgets"
        
    print("--- Setting up E-commerce Multi-Agent Setup using Google ADK ---")
    
    # 2. Session Management (Memory Layer)
    session = SessionService(session_id="ecommerce-launch-123")
    print(f"Initialized Session: {session.session_id}")
    
    # Configure Model
    model = GoogleGenAIModel(model_name="gemini-1.5-pro")

    # 3. Define Specialized Roles (Agents base units)
    research_agent = Agent(
        name="ResearchAgent", 
        instruction="Use search APIs to identify trending products. Only return the trend data.", 
        tools=[registry.get_tool("fetch_trends")],
        model=model
    )
    
    marketing_agent = Agent(
        name="MarketingAgent",
        instruction="Generate high-converting product descriptions based on the research provided.",
        model=model
    )
    
    pricing_agent = Agent(
        name="PricingAgent",
        instruction="Manage product listings and dynamic pricing updates in DB.",
        model=model
    )
    
    # 4. Multi-Agent Manager via Sequential Orchestrator
    ecommerce_orchestrator = SequentialAgent(
        name="E-Commerce Launch Pipeline",
        agents=[research_agent, marketing_agent, pricing_agent],
        model=model
    )
    
    # 5. Execution Flow
    goal = "Launch a trending product store"
    
    # Demonstrate Rewind Capability via Session Service recording
    session.record_state("pre-launch")
    print("State 'pre-launch' recorded in Session Service.")
    
    print(f"\nExecuting Sequential Pipeline with Goal: '{goal}'")
    
    # Pass the session to the orchestrator to maintain the memory layer
    result = ecommerce_orchestrator.run(task=goal, session=session)
    
    session.record_state("post-launch")
    print("\nState 'post-launch' recorded in Session Service.")
    
    print("--- Final Result ---")
    print(result)

if __name__ == "__main__":
    # Note: Requires google-adk installed and GOOGLE_API_KEY exported
    setup_ecommerce_flow()
