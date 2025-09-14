# parsers/ai_parser.py

import ollama
import json
from core.schema import NORMALIZED_SCHEMA

def parse_with_ai(raw_text: str) -> tuple[dict | None, list[str]]:
    """
    Parses raw text into a structured JSON using a local LLM.

    Args:
        raw_text (str): The raw text extracted from a document.

    Returns:
        A tuple containing:
        - dict | None: The parsed JSON data, or None on failure.
        - list[str]: An interpretation log for this step.
    """
    log = ["Attempting to parse with AI (phi3:mini)..."]
    
    # We create a clean copy of the data schema to guide the LLM
    target_schema = json.dumps(NORMALIZED_SCHEMA['data'], indent=2)

    prompt = f"""
    You are an expert data extraction tool.
    Your task is to analyze the following document text and extract the required information.
    Return the information as a valid JSON object that strictly follows this schema.
    Do not include any explanations, comments, or markdown formatting around the JSON.
    Only output the final JSON object.

    SCHEMA:
    {target_schema}

    DOCUMENT TEXT:
    ---
    {raw_text[:4000]} 
    ---

    JSON OUTPUT:
    """

    try:
        response = ollama.chat(
            model='phi3:mini',
            messages=[{'role': 'user', 'content': prompt}],
            format='json', # This is a powerful feature of Ollama
        )
        
        content = response['message']['content']
        log.append("AI model responded successfully.")
        
        # The 'json' format flag should ensure this is valid, but we double-check
        parsed_json = json.loads(content)
        log.append("Successfully parsed AI response into JSON.")
        
        return parsed_json, log

    except json.JSONDecodeError:
        log.append("Error: AI returned a non-JSON response.")
        log.append(f"Received: {content}")
        return None, log
    except Exception as e:
        log.append(f"An unexpected error occurred with Ollama: {e}")
        return None, log
