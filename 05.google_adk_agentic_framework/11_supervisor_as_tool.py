"""
11_supervisor_as_tool.py

Pattern 3: Supervisor as Tool in Google ADK
Worker executes its primary framework logic but leverages a Supervisor-wrapped tool for support.
"""
from google_adk.agents import Agent
from google_adk.tools import ToolRegistry

registry = ToolRegistry()

@registry.register("ask_supervisor", description="Use this to escalate blockers or request proprietary permissions.")
def ask_supervisor(issue: str) -> str:
    return f"[Supervisor Override]: Issue '{issue}' evaluated and resolved. Resume operations."

def main():
    print("--- Google ADK Pattern: Supervisor as a Tool ---")
    print("Rather than being the orchestrator, the Supervisor functions strictly as an Oracle tool for the worker.")
    
    floor_worker = Agent(
        name="PrimaryWorker",
        instruction="Execute long-running tasks. Invoke the supervisor ONLY if stuck.",
        tools=[registry.get_tool("ask_supervisor")]
    )
    
    print("\nWorker securely initialized with Supervisor-escalation bypass abilities.")

if __name__ == "__main__":
    main()
