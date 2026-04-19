# 04 - LangGraph Agentic Flow

This folder focuses on state-based, graph-driven orchestrations utilizing **LangGraph**. Instead of relying on linear pipelines, LangGraph maps components natively using formal `StateGraph` object definitions establishing declarative Edge/Node routing pipelines.

## Core LangGraph Concepts
1. **Nodes**: Independent Python functions encapsulating execution logic passing strict dict payloads.
2. **Edges**: Core flow pathways explicitly chaining nodes structurally implicitly defining step operations.
3. **Conditional Edges**: Decision pathways passing conditional validations organically dynamically routing loops based on LLM outputs or standard constraints natively.
4. **State Management**: A universal dictionary representation passed iteratively mapping variables implicitly effectively providing global loop memory naturally.

## Explaining The Files (High Level)

### Section A: Routing and Orchestration Basics
- `00_core_components_example.py`: Fundamental skeleton illustrating raw node operations independently of LLM frameworks mapping pure edge flows correctly.
- `01_intermediate_chat_agent.py`: Introduces iterative standard continuous messaging operations naturally enabling explicit termination nodes utilizing cyclical edges.
- `02_routing_example.py`: Abstracting deterministic branches efficiently using semantic context mapping natively dynamically isolating control pipelines strictly based on categorization parameters.
- `03_parallelization_example.py`: Fan-out schema invoking concurrent worker operations optimally consolidating returned reduction state mappings correctly internally via map-reduce methodologies.

### Section B: Iterative Refinement and Tool Invocation
- `04_reflection_example.py`: The native Critique loop seamlessly looping `Current Code -> Review -> Critique Feedback -> Update Code` natively utilizing circular conditional edges gracefully ending on validation perfection mappings. 
- `05_tool_google_search.py`: Prebuilt generic `create_react_agent` workflows mimicking external search API loops accurately.
- `06_tool_code_execution.py`: ReAct framework implementations handling internal python abstractions recursively without requiring LangChain AgentExecutors implicitly passing state messaging automatically!
- `07_tool_api_call.py`: Seamless RESTful HTTP extraction mappings utilizing pure tool metadata blocks directly injecting JSON arrays continuously correctly parsing system constraints efficiently.
- `08_tool_db_query.py`: Mapping pure natural queries into strict extraction representations recursively updating internal state layers mapping database environments uniformly natively.

### Section C: Advanced Multi-Agent Flow Designs
- `09_network_decentralized.py`: Peer-to-Peer structures mapping non-centralized edges directly jumping isolated nodes recursively conditionally.
- `10_supervisor_model.py`: Formal hub-and-spoke mappings ensuring sequential central dispatch paths iteratively pushing instructions exclusively downward and consuming outputs safely internally without overlapping side-effects efficiently explicitly.
- `11_supervisor_as_tool.py`: Inverse operation where the lower-level nodes maintain control priority branching purely to query permission flags externally internally bypassing command layers entirely organically conditionally natively.
- `12_hierarchical_model.py`: Complex abstraction structures effectively encapsulating fully recursive internal Sub-Graphs operating exclusively identically explicitly directly functioning purely as simple root-graph nodes effortlessly extending capabilities explicitly correctly!
