"""
10_supervisor_model.py

Pattern 2: Supervisor Model in Google ADK
A Master Orchestrator Agent handles routing to various wrapped worker agents.
"""
from google_adk.agents import Agent
from google_adk.tools import ToolRegistry

registry = ToolRegistry()

@registry.register("worker_1_call", description="Dispatch UI tasks to Worker 1.")
def worker_1_call(task: str) -> str:
    return f"Worker 1 finalized UI: {task}"

@registry.register("worker_2_call", description="Dispatch DB tasks to Worker 2.")
def worker_2_call(task: str) -> str:
    return f"Worker 2 finalized DB schema: {task}"

def main():
    print("--- Google ADK Pattern: Supervisor Model ---")
    print("The Supervisor utilizes tool invocation exclusively to pass sub-tasks to child execution pipelines.")
    
    supervisor = Agent(
        name="HubSupervisor",
        instruction="You sit at the center of the organization. Map the UI and DB tasks appropriately.",
        tools=[registry.get_tool("worker_1_call"), registry.get_tool("worker_2_call")]
    )
    
    print("\nSupervisor Agent configured to map traffic downstream effectively.")

if __name__ == "__main__":
    main()
