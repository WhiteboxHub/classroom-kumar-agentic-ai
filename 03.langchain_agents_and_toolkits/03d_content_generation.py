import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        return print("Set your OPENAI_API_KEY variable.")
        
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7) # Higher temp for content generation
    
    # Content Generation phases
    c_ideate = ChatPromptTemplate.from_template("Generate exactly 3 specific topic ideas based on the general interest: '{interest}'") | llm | StrOutputParser()
    c_outline = ChatPromptTemplate.from_template("Generate a structured 2-point outline for an article titled: '{topic}'") | llm | StrOutputParser()
    c_draft = ChatPromptTemplate.from_template(
        "Write a 1-paragraph draft section based strictly on this outline point: '{point}'.\n"
        "Ensure it flows logically from the prior section context (if provided): {context}"
    ) | llm | StrOutputParser()
    c_review = ChatPromptTemplate.from_template("Review and refine this compiled draft for tone, prose fluidity, and grammar:\n\n{draft}") | llm | StrOutputParser()
    
    print("--- Content Generation Workflow ---\n")
    
    print("1. Generating Ideation Topics...")
    ideas = c_ideate.invoke({"interest": "Renewable Energy storage"})
    print(f"Ideas generated:\n{ideas}\n")
    
    topic = "The Rise of Solid State Batteries in Grid Storage"
    print(f"2. Simulating User Selection: '{topic}'")
    
    print("\n3. Generating Outline...")
    outline = c_outline.invoke({"topic": topic})
    print(f"Outline:\n{outline}\n")
    
    # Mock extracting points from LLM generated outline string
    points = ["Mechanism of Solid State Batteries", "Scaling to Grid Capacity"]
    
    drafts = []
    current_context = "Introduction context (None)"
    
    print("4. Procedural Drafting (Looping through outline points)...")
    for idx, point in enumerate(points):
        print(f"   Drafting Section {idx+1}: {point}...")
        section_draft = c_draft.invoke({"point": point, "context": current_context})
        drafts.append(section_draft)
        
        # Sequentially feed the drafted section into the next cycle acting as historical context
        current_context = section_draft 
        
    full_draft = "\n\n".join(drafts)
    
    print("\n5. Deep Evaluating & Refining Complete Draft...")
    final_polished_content = c_review.invoke({"draft": full_draft})
    
    print(f"\nFINAL REFINED CONTENT:\n{final_polished_content}")


if __name__ == "__main__":
    main()
