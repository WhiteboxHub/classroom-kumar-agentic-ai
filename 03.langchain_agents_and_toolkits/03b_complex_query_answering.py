import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OPENAI_API_KEY variable.")
        return

    # Complex Query Answering Workflow
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Prompt 1: Identify sub-questions
    p_sub = ChatPromptTemplate.from_template(
        "Identify the core sub-questions required to answer this user query: '{query}'\nList them clearly."
    )
    c_sub = p_sub | llm | StrOutputParser()
    
    # Prompt 2 & 3: Research each distinct sub-question
    p_research = ChatPromptTemplate.from_template(
        "Provide a factual historical summary specifically about this sub-topic: {topic}"
    )
    c_research = p_research | llm | StrOutputParser()
    
    # Prompt 4: Synthesize final answer
    p_synthesize = ChatPromptTemplate.from_template(
        "Synthesize the following distinct pieces of information into a single coherent answer to the original query: '{query}'\n\n"
        "Info 1: {info1}\n"
        "Info 2: {info2}"
    )
    c_synthesize = p_synthesize | llm | StrOutputParser()
    
    original_query = "What were the main causes of the stock market crash in 1929, and how did government policy respond?"
    print(f"--- Complex Query Answering ---\nQuery: {original_query}")
    
    print("\n1. Extracting Sub-questions...")
    sub_questions = c_sub.invoke({"query": original_query})
    print(sub_questions)
    
    print("\n2. Researching Topic 1 (Causes)...")
    info1 = c_research.invoke({"topic": "Causes of the stock market crash in 1929"})
    
    print("\n3. Researching Topic 2 (Government Response)...")
    info2 = c_research.invoke({"topic": "Government policy response to the 1929 stock market crash"})
    
    print("\n4. Synthesizing Final Answer...")
    final_answer = c_synthesize.invoke({
        "query": original_query, 
        "info1": info1, 
        "info2": info2
    })
    print(f"\nSYNTHESIZED ANSWER:\n{final_answer}")

if __name__ == "__main__":
    main()
