import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        return print("Set your OPENAI_API_KEY variable.")

    # Using text LLM (Since passing Base64 encoded images requires gpt-4-vision APIs and varies slightly).
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # In a full multimodal pipeline, Prompt 1 would accept {image_base64_payload}
    print("--- Multimodal & Multi-step Logic Sequence ---\n")
    print("1. [Simulated Modality Hook] Extracting physical bounding box text from Image Bytes...")
    
    extracted_OCR_text = "Label A points to 'Gross Revenue'. Label B points to 'Operating Costs'."
    
    # Prompt 2: Conceptual Linking 
    p_link = ChatPromptTemplate.from_template(
        "Analyze the following raw OCR text extracted from an image diagram. "
        "Create a clean linking dictionary showing what each label points to.\n\n"
        "OCR Text: {text}"
    )
    c_link = p_link | llm | StrOutputParser()
    
    # Prompt 3: Intersect modalities (Labels linked to Tabular data execution)
    p_interpret = ChatPromptTemplate.from_template(
        "You have visual contextual labels and distinct tabular spreadsheet data. "
        "Using both, calculate the overall profit explicitly mapped to Label A minus Label B.\n\n"
        "Visual Context Labels: {labels}\n"
        "Spreadsheet Tabular Data: [Gross Revenue=$500,000], [Operating Costs=$320,000]\n"
    )
    c_interpret = p_interpret | llm | StrOutputParser()
    
    
    print("2. Mapping contextual Image text to relational labels...")
    linked_labels = c_link.invoke({"text": extracted_OCR_text})
    print(linked_labels)
    
    print("\n3. Injecting interpretation using cross-modal spreadsheet tabular matrices...")
    final_derived_answer = c_interpret.invoke({"labels": linked_labels})
    
    print(f"\nFINAL MULTIMODAL SYNTHESIS:\n{final_derived_answer}")

if __name__ == "__main__":
    main()
