# app.py

import streamlit as st
import json
from core.schema import NORMALIZED_SCHEMA
from core import database
from parsers.ingestion import ingest_document
from parsers.ai_parser import parse_with_ai
from parsers.rule_engine import generate_signature, apply_rules, learn_rules_from_ai

# --- Constants for Cost Estimation ---
COST_PER_AI_PARSE = 0.01   # Estimated cost for one AI call ($)
COST_PER_RULE_PARSE = 0.0001 # Estimated cost for one rule-based extraction ($)


# --- Initialization ---
database.initialize_db()

# Initialize session state for results and stats
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'stats' not in st.session_state:
    st.session_state.stats = {"ai_count": 0, "rule_count": 0, "total_cost": 0.0}


def reset_state():
    """Clears the results and statistics."""
    st.session_state.results = {}
    st.session_state.stats = {"ai_count": 0, "rule_count": 0, "total_cost": 0.0}


# --- UI Configuration ---
st.set_page_config(layout="wide")
st.title("📄 Multi-Format Document Parser")
st.markdown("---")


# --- Sidebar ---
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF or DOCX files to parse",
        accept_multiple_files=True,
        type=['pdf', 'docx'] # <-- UPDATED THIS LINE
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Processing", type="primary", use_container_width=True, disabled=not uploaded_files):
            progress_bar = st.progress(0, text="Starting processing...")

            for i, uploaded_file in enumerate(uploaded_files):
                file_name = uploaded_file.name
                progress_bar.progress((i + 1) / len(uploaded_files), text=f"Processing {file_name}...")
                
                try:
                    # --- HYBRID PIPELINE LOGIC ---
                    full_log, final_json, status, method = [], None, "Processing", None
                    
                    # 1. Ingestion
                    file_bytes = uploaded_file.getvalue()
                    raw_text, ingest_log = ingest_document(file_name, file_bytes)
                    full_log.extend(ingest_log)

                    if raw_text:
                        # 2. Signature Generation
                        signature = generate_signature(raw_text)
                        full_log.append(f"Generated signature: {signature[:10]}...")
                        
                        # 3. Check for Existing Rules (Cheap Path)
                        saved_rules = database.find_rules_by_signature(signature)
                        
                        if saved_rules:
                            method = 'rule'
                            full_log.append("✅ Found signature. Applying saved rules.")
                            parsed_data, rule_log = apply_rules(saved_rules, raw_text)
                            full_log.extend(rule_log)
                            status = "Success (Rule)"
                        else:
                            # 4. Fallback to AI (Expensive Path)
                            method = 'ai'
                            full_log.append("⚠️ No signature found. Using AI parser.")
                            parsed_data, ai_log = parse_with_ai(raw_text)
                            full_log.extend(ai_log)
                            
                            if parsed_data:
                                # 5. Learn and Save New Rules
                                full_log.append("🧠 Learning rules from AI output...")
                                new_rules = learn_rules_from_ai(raw_text, parsed_data)
                                if new_rules:
                                    database.save_signature_and_rules(signature, new_rules)
                                    full_log.append(f"✅ Saved {len(new_rules)} new rules.")
                                status = "Success (AI & Learned)"
                            else:
                                parsed_data = {} # Ensure parsed_data is a dict for schema population
                                status = "AI Parsing Failed"

                        # Populate final JSON and update stats if processing was successful
                        if status.startswith("Success"):
                            st.session_state.stats[f"{method}_count"] += 1
                            st.session_state.stats["total_cost"] += COST_PER_AI_PARSE if method == 'ai' else COST_PER_RULE_PARSE
                            
                            final_json = NORMALIZED_SCHEMA.copy()
                            final_json['metadata'].update({'file_name': file_name, 'parsing_method': method, 'signature_used': signature})
                            final_json['data'] = parsed_data
                    else:
                        status = "Ingestion Failed"

                    st.session_state.results[file_name] = {"status": status, "log": full_log, "parsed_json": final_json}

                except Exception as e:
                    # --- ROBUST ERROR HANDLING FOR A SINGLE FILE ---
                    st.session_state.results[file_name] = {
                        "status": "Fatal Error",
                        "log": [f"A critical error occurred during processing.", f"ERROR: {str(e)}"],
                        "parsed_json": None
                    }
                    # Log the full error to the console for easier debugging
                    print(f"Error processing {file_name}: {e}")

            progress_bar.empty()
            st.success("Processing complete!")

    with col2:
        if st.button("Clear Results", use_container_width=True):
            reset_state()
            st.rerun()

    # --- Cost & Usage Summary ---
    st.divider()
    st.header("Cost & Usage Summary")
    stats = st.session_state.stats
    st.metric("Total Files Processed", value=stats['ai_count'] + stats['rule_count'])
    st.metric("Processed by AI", value=stats['ai_count'])
    st.metric("Processed by Rule", value=stats['rule_count'])
    st.metric("Estimated Total Cost", value=f"${stats['total_cost']:.4f}")


# --- Main Area for Displaying Results ---
st.header("Processing Results")

if not st.session_state.results:
    st.info("Upload documents and click 'Start Processing' to see results here.")
else:
    for file_name, result in st.session_state.results.items():
        with st.expander(f"**{file_name}** - Status: `{result['status']}`"):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Normalized JSON Output")
                if result['parsed_json']:
                    st.json(result['parsed_json'])
                    st.download_button(
                        label="⬇️ Download JSON",
                        data=json.dumps(result['parsed_json'], indent=2),
                        file_name=f"{file_name.split('.')[0]}_parsed.json",
                        mime="application/json",
                        key=f"download_{file_name}" # Unique key for each button
                    )
                else:
                    st.warning("No JSON was generated for this file.")
            with col2:
                st.subheader("Interpretation Log")
                st.code("\n".join(result['log']), language="log")
