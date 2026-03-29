import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
# For Toolkit functionality
from langchain_community.agent_toolkits import FileManagementToolkit
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set your OPENAI_API_KEY environment variable. You can use a .env file.")
        return

    print("\n===========================================")
    print("1. Loading a LangChain Toolkit")
    print("===========================================")
    # A Toolkit is a modular collection of tools designed for a specific domain.
    # Instead of defining 'create_file' and 'list_directory' manually, we use the built-in Toolkit.
    
    workspace_dir = os.path.join(os.getcwd(), "agent_workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    
    toolkit = FileManagementToolkit(
        root_dir=workspace_dir,
        # We selectively extract two tools from the larger toolkit
        selected_tools=["write_file", "list_dir"]
    )
    
    # Extract the actionable tools out of the toolkit grouping
    tools = toolkit.get_tools()
    
    print(f"Loaded {len(tools)} tools dynamically from FileManagementToolkit:")
    for t in tools:
        print(f" - [Tool Name]: {t.name} -> {t.description}")

    print("\n===========================================")
    print("2. Setting up the Agent & Executor")
    print("===========================================")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Prompt MUST include `agent_scratchpad` placeholder to hold Agent Execution memory loop.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful file management assistant. Use your tools to interact with the workspace."),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"), 
    ])
    
    # 'Agent' conceptually is just the LLM configured to decide the NEXT actionable step.
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # 'AgentExecutor' is the underlying RUNTIME engine. It handles:
    #  - Calling the 'Agent' to decide an action -> (AgentAction)
    #  - Executing the defined tool code safely   -> (Observation)
    #  - Feeding Observations back to the LLM     -> (Memory Loop)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=False, # Set false so we can isolate and print the loop manually
    )

    print("\n===========================================")
    print("3. Explaining the Agent Execution Loop")
    print("===========================================\n")
    
    query = "Write 'Hello Agentic AI Class' to a file named 'hello_agent.txt', then tell me what files are currently in the directory."
    print(f"User Request: {query}\n")
    print("Initiating Execution Loop Step-by-Step...\n")
    
    # We utilize `agent_executor.iter()` to walk through the While-Loop sequentially rather than just jumping to `.invoke()`!
    step_number = 1
    for chunk in agent_executor.iter({"input": query}):
        print(f"----- Step {step_number} -----")
        
        # When the agent produces an "Action", the Executor runs the tool and returns an "Observation".
        if "intermediate_steps" in chunk:
            for action, observation in chunk["intermediate_steps"]:
                # The 'AgentAction' represents the LLM's decision (Which tool? What arguments?)
                print(f"[Agent Decides] -> AgentAction:")
                print(f"                -> Tool : '{action.tool}'")
                print(f"                -> Input: {action.tool_input}")
                
                # The 'Observation' represents the environment's response to the tool execution.
                print(f"\n[Environment]   -> Observation:\n                -> {observation}\n")
                
        # The loop terminates when the Agent interprets it has completed the user's task overarching goal.
        # This is represented by an 'AgentFinish' event which yields the final text to the user.
        elif "output" in chunk:
            print("[Agent Decides] -> AgentFinish (Condition Met)")
            print(f"Final Answer: {chunk['output']}\n")
            
        step_number += 1

    print("===========================================")
    print("Check the generated workspace directory:")
    print(f"Path: {workspace_dir}")
    print("===========================================\n")

if __name__ == "__main__":
    main()
