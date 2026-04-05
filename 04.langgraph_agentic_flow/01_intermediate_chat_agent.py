"""
Intermediate LangGraph Example: Chatbot Agent with Tool Execution
This example demonstrates:
- A loop between an LLM node and a Tool node
- Conditional edges using `tools_condition` router
- Checkpointer (MemorySaver) for conversation history

Flow:
1. User provides a message.
2. The Agent (LLM) decides whether to answer directly or use a tool.
3a. If a tool is needed, it routes to the Tool Execution node, then loops back to the Agent.
3b. If no tool is needed, it routes to END.
"""

from typing import Annotated, Literal, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# 1. State Definition
# We use `add_messages` to ensure messages are appended rather than overwritten
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 2. Nodes

def chatbot_node(state: AgentState):
    """The main LLM node."""
    print("--- Node: Chatbot (LLM) ---")
    messages = state["messages"]
    
    # In a real scenario, this would be an LLM invocation:
    # response = llm.bind_tools(tools).invoke(messages)
    
    # Mocking LLM behavior:
    last_message = messages[-1].content
    
    if "weather" in last_message.lower():
        print("Agent decides to use the weather tool.")
        # Mocking a tool call structure
        response = AIMessage(
            content="",
            tool_calls=[{"name": "get_weather", "args": {"location": "San Francisco"}, "id": "call_123"}]
        )
    elif isinstance(messages[-1], ToolMessage):
        print("Agent is reading tool result and generating final answer.")
        response = AIMessage(content="The weather in San Francisco is sunny and 72°F.")
    else:
        print("Agent responds directly.")
        response = AIMessage(content="Hello! I am a helpful agent. How can I assist you?")
    
    return {"messages": [response]}


def tools_node(state: AgentState):
    """Executes tools based on LLM output."""
    print("--- Node: Tool Execution ---")
    last_message = state["messages"][-1]
    
    # Mocking tool execution
    tool_messages = []
    if hasattr(last_message, "tool_calls"):
        for tool_call in last_message.tool_calls:
            print(f"Executing tool: {tool_call['name']}({tool_call['args']})")
            # Simulate tool returning data
            tool_result = "Sunny, 72°F" 
            tool_messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))
            
    return {"messages": tool_messages}

# 3. Router logic
def route_after_chatbot(state: AgentState) -> Literal["tools", "__end__"]:
    """Conditional routing based on whether the LLM produced tool calls."""
    last_message = state["messages"][-1]
    
    # If there is a tool call, route to tools node
    if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
        print("Router Decision: LLM requested a tool -> Route to 'tools'")
        return "tools"
    
    # Otherwise, finish
    print("Router Decision: LLM provided final answer -> Route to END")
    return "__end__"

# 4. Build the Graph
def build_intermediate_graph():
    print("Initializing Intermediate StateGraph...")
    workflow = StateGraph(AgentState)
    
    workflow.add_node("chatbot", chatbot_node)
    workflow.add_node("tools", tools_node)
    
    workflow.add_edge(START, "chatbot")
    
    # Add conditional edge from chatbot
    workflow.add_conditional_edges(
        "chatbot",
        route_after_chatbot,  # Router logic
        {
            "tools": "tools",  # If router returns "tools", go to tools_node
            "__end__": END     # If router returns "__end__", stop
        }
    )
    
    # Loop back to chatbot after tools are done executing
    workflow.add_edge("tools", "chatbot")
    
    # 5. Compile with Checkpointer
    memory_saver = MemorySaver()
    app = workflow.compile(checkpointer=memory_saver)
    return app

if __name__ == "__main__":
    app = build_intermediate_graph()
    
    config = {"configurable": {"thread_id": "session-1"}}
    
    print("\n=== User: Hello! ===")
    initial_input = {"messages": [HumanMessage(content="Hello!")]}
    
    for event in app.stream(initial_input, config=config):
        pass
        
    print("\n--- Final State ---")
    state = app.get_state(config)
    for m in state.values["messages"]:
        print(f"{m.__class__.__name__}: {m.content}")
        
    print("\n=== User: What's the weather in San Francisco? ===")
    next_input = {"messages": [HumanMessage(content="What's the weather like in San Francisco?")]}
    
    for event in app.stream(next_input, config=config):
        pass
        
    print("\n--- Final State ---")
    state = app.get_state(config)
    for m in state.values["messages"]:
         m_type = m.__class__.__name__
         content = m.content
         if hasattr(m, 'tool_calls') and m.tool_calls:
             content = f"Tool Calls: {m.tool_calls}"
         print(f"{m_type}: {content}")
