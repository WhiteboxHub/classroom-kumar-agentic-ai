"""
Intermediate Google ADK Example: Advanced Orchestrators

This example demonstrates parallel and looping orchestration patterns 
imported directly from the Google ADK framework:
- ParallelAgent: Executes multiple sub-agents simultaneously.
- LoopAgent: Repeats a task until a specific condition is met.
"""

from google_adk.agents import Agent, ParallelAgent, LoopAgent
from google_adk.memory import SessionService
from google_adk.llms import GoogleGenAIModel

def run_intermediate_examples():
    session = SessionService(session_id="intermediate-demo")
    model = GoogleGenAIModel(model_name="gemini-1.5-pro")
    
    # ----------------------------------------------------
    # 1. Parallel Execution Demo
    # ----------------------------------------------------
    print("\n--- 1. Parallel Orchestrator Demo ---")
    seo_agent = Agent(
        name="SEO_Agent", 
        instruction="Optimize meta tags for homepage.",
        model=model
    )
    ui_agent = Agent(
        name="UI_Agent", 
        instruction="Create responsive CSS for homepage.",
        model=model
    )
    db_agent = Agent(
        name="DB_Agent", 
        instruction="Index product tables in database.",
        model=model
    )
    
    # The ParallelAgent encapsulates these sub-agents to trigger their 
    # tasks concurrently rather than blocking sequentially.
    parallel_orchestrator = ParallelAgent(
        name="FrontPage Launch Squad",
        agents=[seo_agent, ui_agent, db_agent],
        model=model
    )
    
    print("Executing FrontPage Squad concurrently...")
    parallel_result = parallel_orchestrator.run(
        task="Prepare the frontpage for launch", 
        session=session
    )
    print("Parallel Result:", parallel_result)
    
    # ----------------------------------------------------
    # 2. Loop Execution Demo
    # ----------------------------------------------------
    print("\n--- 2. Loop Orchestrator Demo ---")
    
    qa_agent = Agent(
        name="QA_Agent", 
        instruction="Run automated integration tests and report issues.",
        model=model
    )
    
    # The LoopAgent evaluates the outcome of the sub-agent and decides whether
    # to repeat based on a defined condition and max bounds.
    loop_orchestrator = LoopAgent(
        name="QA Testing Loop",
        agent=qa_agent,
        condition="Stop when all automated integration tests pass",
        max_iterations=5,
        model=model
    )
    
    print("Executing QA loop until success or configured max iteration limit...")
    loop_result = loop_orchestrator.run(
        task="Test the final application build", 
        session=session
    )
    print("Loop Result:", loop_result)
    
if __name__ == "__main__":
    # Note: Requires google-adk installed and GOOGLE_API_KEY exported
    run_intermediate_examples()
