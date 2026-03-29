import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        return print("Set your OPENAI_API_KEY variable.")

    # We use a dual-model execution pattern. JSON for state parsing, Text for conversational reply.
    llm_json = ChatOpenAI(model="gpt-3.5-turbo", temperature=0).bind(response_format={"type": "json_object"})
    llm_text = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    # Prompt 1: Turn Utterance -> State Updates
    p_state = ChatPromptTemplate.from_template(
        "Analyze the user's latest dialogue utterance: '{utterance}'.\n"
        "Extract intent and any defined parameters (like destination, date, item).\n"
        "Respond simply with a flat JSON mapping identifying 'intent', and relevant 'entities'."
    )
    c_state = p_state | llm_json | JsonOutputParser()
    
    # Prompt 2: State Context -> Dialogue turn text 
    p_dialogue = ChatPromptTemplate.from_template(
        "You are an AI Assistant maintaining conversational continuity."
        "The conversation's accumulated state memory holds: {state_json}\n"
        "The user's latest utterance is: '{utterance}'\n"
        "Craft a natural response progressing the conversation. If the user's intent requires more specific "
        "information not present in the state memory, request it gently."
    )
    c_dialogue = p_dialogue | llm_text | StrOutputParser()
    
    
    print("--- Conversational Agents with State (No Framework Memories!) ---\n")
    # Represent the accumulating conversation state manually
    persistent_session_state = {} 
    
    user_conversation_flow = [
        "I'd like to book a table for dinner tonight.",
        "Yes, we will have 4 guests.",
        "Preferably at an Italian restaurant downtown."
    ]
    
    for turn_number, user_utterance in enumerate(user_conversation_flow, 1):
        print(f"\n[Turn {turn_number}] User: {user_utterance}")
        
        # 1. Processing State Mapping
        state_updates = c_state.invoke({"utterance": user_utterance})
        print(f"   [System] Extracted state updates: {state_updates}")
        
        # Merge changes structurally into persistent layer
        persistent_session_state.update(state_updates.get("entities", {}))
        if "intent" in state_updates: 
            persistent_session_state["intent"] = state_updates["intent"]
            
        print(f"   [System] Memory Pool: {persistent_session_state}")
        
        # 2. Sequential Response via memory injection
        reply = c_dialogue.invoke({
            "state_json": json.dumps(persistent_session_state),
            "utterance": user_utterance
        })
        print(f"   Agent: {reply}")

if __name__ == "__main__":
    main()
