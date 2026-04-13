# 03 - LangChain Basics, Toolkits, and Agents

This folder contains all LangChain examples, progressing from basic pipeline construction to advanced agent execution loops.

## How It Works

LangChain is a framework for building context-aware reasoning applications by stringing together composable tools (`Components`) and executing loops (`Agents`).

---

## Part A: Core Elements and Abstractions (`03a.langchain_basics.py`)

This script demonstrates the foundational building blocks:
1. **Models:** Abstractions over language models (e.g., `ChatOpenAI`).
2. **PromptTemplates:** Dynamic text prompt definitions that cleanly inject variables instead of writing f-strings.
3. **OutputParser:** Utilities to parse raw text streams into Python objects (e.g., dictionaries or lists).
4. **LCEL Interface (LangChain Expression Language):** The syntax that pipes sequences natively using the `|` operator:
   ```python
   chain = prompt | model | output_parser
   ```

---

## Part B: Agent Execution Loop & Toolkits (`03b.agent_loop_and_toolkits.py`)

This script illustrates the "Agentic" capabilities of LangChain, specifically focusing on observation and response routing.

### 1. Toolkits
A toolkit is a collection of 3-5 tools bundled structurally for a specific domain. Instead of writing our customized python tools manually, we leverage the pre-built `FileManagementToolkit`. LangChain provides endless out-of-the-box toolkits like `SQLDatabaseToolkit` or `GitHubToolkit`.

### 2. Agent Execution Loop (`AgentExecutor`)
The underlying runtime engine for LangChain Agents performs a continuous `While Loop`.
```python
next_action = agent.get_action(question)

while next_action != AgentFinish:
    # Environment execution
    observation = run(next_action) 
    
    # Context feedback
    next_action = agent.get_action(question, previous_actions, observation)

return final_response
```

Instead of simply running `.invoke()`, we use `.iter()` in the code to slow down the classroom demonstration. Our console output allows students to explicitly monitor:
- **`AgentAction`:** When the LLM decides on a tool and input.
- **`Observation`:** The raw system output fed back to the LLM.
- **`AgentFinish`:** The condition that triggers when the request is fully satisfied.

---

## Part C: Agentless Prompt Chaining Workflows (`03a` - `03i`)
These nine scripts demonstrate how to handle multi-step reasoning natively using the LangChain Expression Language (LCEL) without relying on autonomous Agent Executors:

- `03a_information_processing.py`: Sequential transformations from raw extraction to summarization.
- `03b_complex_query_answering.py`: Breaking down questions, researching parts, and synthesizing.
- `03c_data_extraction_transformation.py`: Parsing unstructured text into strict JSON output schemas.
- `03d_content_generation.py`: Loops handling ideation, outlining, modular drafting, and review.
- `03e_conversational_state.py`: Maintaining conversational memory loops and multi-persona state manually.
- `03f_code_generation.py`: Iterative process of pseudocode, drafting, LLM static analysis, and refinement.
- `03g_multimodal_reasoning.py`: Orchestrating image OCR labeling mapping against tabular data limits.
- `03h_routing_example.py`: Dynamically routing inputs to specific processing branches based on content classification.
- `03i_parallelization_example.py`: Executing multiple independent tasks concurrently and synthesizing their results.

---

## Running the Examples

1. Navigate to the folder and install dependencies:
   ```bash
   cd 03.langchain_agents_and_toolkits
   pip install -r requirements.txt
   ```

2. Establish your API Key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. Run the scripts sequentially:
   ```bash
   python 03a.langchain_basics.py
   python 03b.agent_loop_and_toolkits.py
   ```
