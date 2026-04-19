"""
04d_hierarchical_model.py

Pattern 4: Hierarchical Model
Multi-level structure with layered coordination. Director -> Manager -> Workers.
"""
from langchain_core.tools import tool

# Level 2 Tools (Managers delegating to Workers)
@tool
def software_manager(task: str) -> str:
    """Delegates technical tasks to junior devs under the software division."""
    return f"[SoftwareManager]: Coordinated and delivered technical task '{task}' via engineering team."

@tool
def sales_manager(task: str) -> str:
    """Delegates outreach tasks to sales reps under the sales division."""
    return f"[SalesManager]: Coordinated campaigns for '{task}' via sales team."

def main():
    print("--- LangChain Pattern: Hierarchical Model ---")
    print("A layered multi-agent design: CEO -> Department Managers -> Floor Workers")
    
    # Level 1 (Director) holds tools for Level 2 (Managers)
    director_tools = [software_manager, sales_manager]
    
    print("\nSimulating Execution:")
    print("Director Agent routes the grand vision.")
    print(software_manager.invoke("Build the eCommerce App"))
    print(sales_manager.invoke("Market the eCommerce App"))

if __name__ == "__main__":
    main()
