"""
12_hierarchical_model.py

Pattern 4: Hierarchical Model in Google ADK
Layered structure implemented through SequentialAgents inside other SequentialAgents, 
or by wrapping specialized Sub-Agents as routing tools in parent Agents.
"""
from google_adk.agents import Agent, SequentialAgent

def main():
    print("--- Google ADK Pattern: Hierarchical Model ---")
    print("Modeling nested delegation arrays using internal components.")
    
    # Layer 3: Individual Contributors
    dev_a = Agent(name="Dev1", instruction="Write frontend.")
    dev_b = Agent(name="Dev2", instruction="Write backend.")
    
    sales_a = Agent(name="Sales1", instruction="Contact clients.")
    
    # Layer 2: Middle Management Orchestrators
    software_team_lead = SequentialAgent(
        name="SoftwareDept",
        agents=[dev_a, dev_b]
    )
    
    sales_team_lead = SequentialAgent(
        name="SalesDept",
        agents=[sales_a]
    )
    
    # Layer 1: Director
    board_director = SequentialAgent(
        name="Director",
        agents=[software_team_lead, sales_team_lead]
    )
    
    print("\nHierarchy Built: Board Director -> [Software Dept, Sales Dept] -> [Dev1, Dev2, Sales1]")
    print("Complex multi-level nesting initialized correctly via ADK's native sub-agent ingestion schema.")

if __name__ == "__main__":
    main()
