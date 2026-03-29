import os
from dotenv import load_dotenv

load_dotenv()

def demonstrate_models():
    print("===========================================")
    print("1. Models (Abstractions over LLM APIs)")
    print("===========================================")
    # Notice we use modern langchain_openai instead of deprecated langchain.chat_models
    from langchain_openai import ChatOpenAI
    
    chat_model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo", temperature=0)
    
    print("Invoking ChatOpenAI with 'hi!'...")
    response = chat_model.invoke("hi!")
    print(f"Model Output: {response.content}\n")

def demonstrate_prompt_templates():
    print("===========================================")
    print("2. PromptTemplates (Abstractions over text)")
    print("===========================================")
    from langchain_core.prompts import ChatPromptTemplate
    
    prompt = ChatPromptTemplate.from_template("Show me 5 examples of this concept: {concept}")
    
    print("Defining PromptTemplate with variable '{concept}' = 'animal'")
    formatted_prompt = prompt.format(concept="animal")
    print(f"Formatted Prompt: '{formatted_prompt}'\n")

def demonstrate_output_parser():
    print("===========================================")
    print("3. OutputParser (Abstractions for parsing)")
    print("===========================================")
    from langchain_core.output_parsers import BaseOutputParser
    
    class CommaSeparatedListOutputParser(BaseOutputParser):
        """Parse the output of an LLM call to a comma-separated list."""
        def parse(self, text: str):
            """Parse the output of an LLM call."""
            return text.strip().split(", ")
            
    parser = CommaSeparatedListOutputParser()
    print("Parsing string 'hi, bye, hello'...")
    parsed_output = parser.parse("hi, bye, hello")
    print(f"Parsed Output (List): {parsed_output}\n")

def demonstrate_lcel_interface():
    print("===========================================")
    print("4. LCEL Interface (LangChain Expression Language)")
    print("===========================================")
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_template("Name 5 concepts related to this: {concept}")
    output_parser = StrOutputParser()
    
    # Leverages the | pipe symbol to compose LangChain components
    print("Composing Chain: chain = prompt | model | output_parser")
    chain = prompt | model | output_parser
    
    print("Invoking chain with concept='probability distribution'...")
    # Because this takes a few seconds, we'll stream or just print immediately.
    # To keep it quick, we'll run it synchronously.
    response = chain.invoke({"concept": "probability distribution"})
    print(f"Output:\n{response}\n")

def demonstrate_agent():
    print("===========================================")
    print("5. AgentExecutor & Tools (The Runtime Runtime)")
    print("===========================================")
    from langchain_openai import ChatOpenAI
    from langchain.agents import create_tool_calling_agent, AgentExecutor, tool
    from langchain_core.prompts import ChatPromptTemplate
    
    # Define a custom tool for the agent
    @tool
    def get_word_length(word: str) -> int:
        """Returns the length of a word in characters."""
        print(f"    [TOOL CALLED: get_word_length for '{word}']")
        return len(word)
        
    tools = [get_word_length]
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Prompt requires 'agent_scratchpad' which maps intermediate_steps natively
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Utilize your available tools when possible."),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"), 
    ])
    
    print("Initializing Agent and AgentExecutor...")
    # Agent: Chain responsible for deciding the next step
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # AgentExecutor: Handles complexities like tool errors and logging
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    
    query = "How many letters are in the word supercalifragilisticexpialidocious?"
    print(f"Agent Query: {query}")
    
    print("Agent running...")
    # agent_executor natively iterates: next_action -> observation -> next_action -> AgentFinish
    response = agent_executor.invoke({"input": query})
    print(f"\nFinal Agent Output: {response['output']}")
    print("===========================================\n")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OPENAI_API_KEY environment variable. You can use a .env file.")
        print("Example: export OPENAI_API_KEY='sk-...'")
    else:
        print("\n--- Starting LangChain Basics Demonstration ---\n")
        demonstrate_models()
        demonstrate_prompt_templates()
        demonstrate_output_parser()
        demonstrate_lcel_interface()
        demonstrate_agent()
        print("--- Demonstration Complete ---")
