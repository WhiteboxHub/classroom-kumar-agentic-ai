import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        return print("Set your OPENAI_API_KEY variable.")
        
    # JSON mapped output model ensures format compliance natively
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0).bind(response_format={"type": "json_object"})
    
    # Prompt 1: Initial extraction attempt
    p_extract = ChatPromptTemplate.from_template(
        "Extract the recipient name, billing address, and total amount from this unstructured text. "
        "Return EXCLUSIVELY a JSON object with keys 'name', 'address', 'amount'.\n\nText: {text}"
    )
    c_extract = p_extract | llm | JsonOutputParser()
    
    # Prompt 2: Conditional conditional correction based on Processing validation
    p_recover = ChatPromptTemplate.from_template(
        "The previous extraction failed to parse the following missing or corrupted fields: {missing_fields}. "
        "Here is the original text context: {text}. Please find the missing information and return it EXCLUSIVELY as JSON."
    )
    c_recover = p_recover | llm | JsonOutputParser()
    
    unstructured_invoice = "INVOICE #99824 - To: Global Tech Inc. Route all physical mail to Suite 400, 1 Market St, SF CA. Grand Total: $14,200.00"
    
    print("--- Data Extraction & Transformation Loop ---\n")
    print("1. Initial Extraction pass...")
    
    extracted_data = c_extract.invoke({"text": unstructured_invoice})
    print(f"Raw Output: {extracted_data}")
    
    # Validation Processing Step
    required_keys = ["name", "address", "amount"]
    missing_keys = [k for k in required_keys if k not in extracted_data or extracted_data[k] is None]
    
    # If missing fields exist, trigger conditional error prompt routing
    if missing_keys:
        print(f"\n2. [Processing] Missing/Malformed fields detected: {missing_keys}")
        print("   Routing to conditional recovery prompt...")
        
        recovery_data = c_recover.invoke({
            "missing_fields": ", ".join(missing_keys), 
            "text": unstructured_invoice
        })
        
        # Merge recovery attempt map
        extracted_data.update(recovery_data)
        print(f"   Recovered Output: {recovery_data}")
        
    print("\n3. Validation Successful. Structured Output Finalized:")
    print(json.dumps(extracted_data, indent=2))

if __name__ == "__main__":
    main()
