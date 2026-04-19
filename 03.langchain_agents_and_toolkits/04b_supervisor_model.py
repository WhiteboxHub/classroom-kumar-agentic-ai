"""
04b_supervisor_model.py

Pattern 2: Supervisor Model
Demonstrates a central agent managing task allocation and coordination in LangChain.
"""
from langchain_core.tools import tool

# Tools mimicking worker agents that the Supervisor can delegate to
@tool
def delegate_to_frontend_worker(task: str) -> str:
    """Supervisor calls this to assign UI work."""
    return f"[FrontendWorker]: Completed UI components for '{task}'."

@tool
def delegate_to_backend_worker(task: str) -> str:
    """Supervisor calls this to assign Database work."""
    return f"[BackendWorker]: Setup database schemas for '{task}'."

def main():
    print("--- LangChain Pattern: Supervisor Model ---")
    print("A central Supervisor Agent is the only entry point, holding tools to map tasks out.")
    
    # The Supervisor holds the router capabilities
    supervisor_tools = [delegate_to_frontend_worker, delegate_to_backend_worker]
    
    print("\nSimulating Execution:")
    print("User -> Supervisor.")
    print("Supervisor delegates components separately:")
    print(delegate_to_frontend_worker.invoke("Login Page"))
    print(delegate_to_backend_worker.invoke("Auth Backend"))
    print("Supervisor reviews and synthesizes the final output.")

if __name__ == "__main__":
    main()
