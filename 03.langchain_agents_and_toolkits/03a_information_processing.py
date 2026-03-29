import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OPENAI_API_KEY environment variable.")
        return

    # Information Processing Workflow: sequential transformation of raw data
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Prompt 1 & 2: Summarization step (Extract/Clean skipped for brevity)
    p_summarize = ChatPromptTemplate.from_template("Summarize the following text:\n\n{text}")
    c_summarize = p_summarize | llm | StrOutputParser()
    
    # Prompt 3: Extract entities
    p_entities = ChatPromptTemplate.from_template("Extract specific entities (names, dates, locations) from this summary:\n\n{summary}")
    c_entities = p_entities | llm | StrOutputParser()
    
    # Prompt 4: Mocked Knowledge Base Search (usually involves VectorDB/Retriever)
    def mock_internal_search(entities_str: str) -> str:
        return f"[MOCKED SEARCH] Found strategic priority alignment for: {entities_str[:50]}..."
        
    # Prompt 5: Generate Final Report
    p_report = ChatPromptTemplate.from_template(
        "Generate a final executive report incorporating the timeline summary, extracted entities, and internal search results.\n\n"
        "Summary: {summary}\nEntities: {entities}\nSearch Results: {search_results}"
    )
    c_report = p_report | llm | StrOutputParser()
    
    raw_text = "On January 15th, 2023, Dr. Emily Chen announced an entirely new AI-driven healthcare initiative at the Global Summit in Geneva. It aims to reduce administrative load by 40%."
    print("--- Information Processing Workflow ---")
    
    print("\n1. Generating Summary...")
    summary = c_summarize.invoke({"text": raw_text})
    print(summary)
    
    print("\n2. Extracting Entities...")
    entities = c_entities.invoke({"summary": summary})
    print(entities)
    
    print("\n3. Querying Internal Knowledge Base...")
    search_results = mock_internal_search(entities)
    print(search_results)
    
    print("\n4. Synthesizing Final Report...")
    report = c_report.invoke({
        "summary": summary, 
        "entities": entities, 
        "search_results": search_results
    })
    print(f"\nFINAL REPORT:\n{report}")

if __name__ == "__main__":
    main()
