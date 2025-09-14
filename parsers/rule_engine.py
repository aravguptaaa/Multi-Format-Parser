# parsers/rule_engine.py

import hashlib
import re

def generate_signature(raw_text: str) -> str:
    """
    Creates a unique and stable signature for a document layout.
    It hashes the first few non-whitespace tokens to identify structure.
    """
    # Normalize by lowercasing and splitting into tokens
    tokens = raw_text.lower().split()
    
    # Use the first 50 tokens as a representative sample of the layout
    signature_tokens = tokens[:50]
    
    # Join them and create a hash
    signature_string = "".join(signature_tokens)
    return hashlib.sha256(signature_string.encode()).hexdigest()

def apply_rules(rules: dict, raw_text: str) -> tuple[dict, list[str]]:
    """
    Applies a set of regex rules to the raw text to extract data.
    """
    extracted_data = {}
    log = ["Applying saved rules to extract data."]
    
    for field, rule_details in rules.items():
        pattern = rule_details.get('pattern')
        try:
            match = re.search(pattern, raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                # Use the first capturing group if it exists, otherwise the whole match
                value = match.group(1) if match.groups() else match.group(0)
                extracted_data[field] = value.strip()
                log.append(f"  - SUCCESS: Found '{field}' with value '{value[:30].strip()}...'")
            else:
                extracted_data[field] = None
                log.append(f"  - FAILED: Could not find '{field}' using pattern.")
        except Exception as e:
            log.append(f"  - ERROR: Rule for '{field}' failed with error: {e}")
            extracted_data[field] = None
            
    return extracted_data, log

def learn_rules_from_ai(raw_text: str, ai_parsed_data: dict) -> dict:
    """
    Generates simple regex rules based on the AI's successful parse.
    """
    learned_rules = {}
    for key, value in ai_parsed_data.items():
        if value is None or not isinstance(value, str):
            continue
        
        # Escape special regex characters in the value
        value_escaped = re.escape(value.strip())
        
        # Create a simple pattern: find this value and capture it.
        # This is a basic approach; more complex logic could find surrounding text.
        pattern = f"({value_escaped})"
        
        # Test the pattern to make sure it works
        if re.search(pattern, raw_text, re.IGNORECASE | re.DOTALL):
            learned_rules[key] = {"pattern": pattern, "method": "regex"}
            
    return learned_rules