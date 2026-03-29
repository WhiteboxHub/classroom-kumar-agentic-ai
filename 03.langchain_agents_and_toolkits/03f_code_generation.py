import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        return print("Set your OPENAI_API_KEY variable.")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Code Generation Phases via Pipeline Prompts
    c_outline = ChatPromptTemplate.from_template("Generate a strictly bulleted logical pseudocode outline for fulfilling this software request: {request}") | llm | StrOutputParser()
    
    c_draft = ChatPromptTemplate.from_template("Translate the following pseudocode outline into raw functional Python code:\n\n{outline}") | llm | StrOutputParser()
    
    c_review = ChatPromptTemplate.from_template(
        "Act as a static analysis tool. Identify any potential runtime errors, edge cases, or inefficiencies in this script. "
        "Return the list of issues, or 'No issues found.'\n\nCode:\n{code}"
    ) | llm | StrOutputParser()
    
    c_refine = ChatPromptTemplate.from_template(
        "You are tasked to rewrite and fundamentally improve the following draft by fixing the identified issues mapping.\n\n"
        "Draft Code:\n{code}\n\nIdentified Issues to fix:\n{issues}\n\n"
        "Return exclusively the refined Python block."
    ) | llm | StrOutputParser()
    
    c_docs = ChatPromptTemplate.from_template("Add comprehensive Google-style docstrings and a basic pytest suite block to the bottom of this script:\n\n{code}") | llm | StrOutputParser()


    request = "A function identifying if a string acts as a palindrome, ignoring non-alphanumeric characters."
    print("--- Code Generation and Refinement Sequence ---\n")
    
    print("1. Generating decomposition outline...")
    outline = c_outline.invoke({"request": request})
    
    print("2. Writing initial functional code draft...")
    code_draft = c_draft.invoke({"outline": outline})
    
    print("3. Executing static analysis (LLM review)...")
    issues = c_review.invoke({"code": code_draft})
    print(f"   Identified Issues:\n   {issues}")
    
    print("\n4. Iteratively Refinement passed...")
    refined_code = c_refine.invoke({"code": code_draft, "issues": issues})
    
    print("5. Generating Documentation & Unit tests...")
    final_output = c_docs.invoke({"code": refined_code})
    
    print(f"\n================ PRODUCTION CODE ================\n{final_output}")

if __name__ == "__main__":
    main()
