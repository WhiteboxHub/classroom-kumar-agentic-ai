"""
03. Google ADK Parallelization Example
--------------------------------------
This example demonstrates how to orchestrate multiple independent agents
concurrently using Google ADK. We use a ParallelAgent to wrap three
sub-agents that perform distinct research tasks simultaneously, then feed 
their findings into a SequentialAgent to synthesize the final report.

Core Classes Highlighted:
- LlmAgent: The foundational agent capable of utilizing tools and instructions.
- ParallelAgent: Executes its list of `sub_agents` concurrently, awaiting all to finish.
- SequentialAgent: Executes a pipeline of agents strictly one after another.
- google_search: A native ADK tool provided for external search capability.
"""

from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

# Highlight: Core Model Configuration
GEMINI_MODEL = "gemini-2.0-flash"

# ====================================================================
# 1. Define Independent Sub-Agents for Parallel Execution (Fan-Out)
# ====================================================================

# Highlight: Using `output_key` securely stores the agent's final response 
# in the shared State under that specific key, passing it downstream.

researcher_agent_1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in energy.
Research the latest advancements in 'renewable energy sources'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.""",
    description="Researches renewable energy sources.",
    tools=[google_search],
    output_key="renewable_energy_result" # Stores output in state for the merger agent
)

researcher_agent_2 = LlmAgent(
    name="EVResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in transportation.
Research the latest developments in 'electric vehicle technology'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.""",
    description="Researches electric vehicle technology.",
    tools=[google_search],
    output_key="ev_technology_result" # Stores output in state for the merger agent
)

researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in climate solutions.
Research the current state of 'carbon capture methods'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.""",
    description="Researches carbon capture methods.",
    tools=[google_search],
    output_key="carbon_capture_result" # Stores output in state for the merger agent
)

# ====================================================================
# 2. Parallel Orchestrator
# ====================================================================

# Highlight: The ParallelAgent runs its `sub_agents` concurrently.
# It finishes ONLY once all enclosed researchers complete and write to state.

parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[researcher_agent_1, researcher_agent_2, researcher_agent_3],
    description="Runs multiple research agents concurrently to gather broad information."
)

# ====================================================================
# 3. Define the Synthesis Agent (Fan-In)
# ====================================================================

# Highlight: Notice the prompt variables (e.g. `{renewable_energy_result}`). 
# These will be automatically populated from the Session State!

merger_agent = LlmAgent(
    name="SynthesisAgent",
    model=GEMINI_MODEL,
    instruction="""You are an AI Assistant responsible for combining research findings into a structured report.
Your primary task is to synthesize the following research summaries. Structure your response using headings for each topic. 

**Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below.**

**Input Summaries:**
* **Renewable Energy:** {renewable_energy_result}
* **Electric Vehicles:** {ev_technology_result}
* **Carbon Capture:** {carbon_capture_result}

**Output Format:**
## Summary of Recent Sustainable Technology Advancements
### Renewable Energy Findings
[Synthesize renewable energy summary here]

### Electric Vehicle Findings
[Synthesize EV summary here]

### Carbon Capture Findings
[Synthesize carbon capture summary here]

### Overall Conclusion
[Provide a brief concluding statement]
""",
    description="Combines research findings from parallel agents into a structured report."
    # Output key is omitted because this agent's return is the direct final pipeline output.
)

# ====================================================================
# 4. Sequential Master Pipeline
# ====================================================================

# Highlight: SequentialAgent creates the full Fan-out / Fan-in lifecycle. 
# It runs `parallel_research_agent` first to populate state, then runs `merger_agent`.

root_pipeline_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    sub_agents=[
        parallel_research_agent, # Step 1: Run Researchers concurrently
        merger_agent             # Step 2: Merge the results
    ],
    description="Coordinates parallel research across sustainable tech and synthesizes results."
)

if __name__ == "__main__":
    print("\n--- Initializing Google ADK Parallel Execution ---")
    print(f"Executing: {root_pipeline_agent.name}")
    print("Parallel Sub-agents will fire concurrently utilizing: google_search filter\n")
    
    # Run the pipeline (assuming synchronous '.run()' execution framework standard)
    # Output will naturally propagate through output_keys into the merger prompt
    
    # Example invocation:
    # final_report = root_pipeline_agent.run("Start Sustainable Tech Research")
    # print(final_report)
    
    print("Code is fully configured. Enable ADK environment and call `.run()` to execute.")
