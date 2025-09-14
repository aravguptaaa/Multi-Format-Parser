# Multi-Format Document Parser

This project is a Streamlit application designed to ingest documents in various formats (PDFs, scans), parse their content, and produce a single, normalized JSON output.

It features a hybrid, cost-effective pipeline that learns document layouts. It uses an expensive AI model (Ollama `phi3:mini`) only for the first encounter with a new layout, then generates and saves cheaper, rule-based methods for all subsequent documents with the same structure.
Project Demo: https://www.loom.com/share/e575a3eb60fa4d6ebe1f5e36117162da

## Key Features

- **Normalized Output**: A single, stable JSON schema for all inputs.
- **Cost & Scale**: Avoids using AI on every document by learning and reusing layout "signatures" and rules.
- **Interpretability**: Provides a human-readable interpretation log for each file, showing the processing path (AI vs. Rule).
- **Layout Learning**: Treats new layouts as unique signatures and learns extraction rules from the initial AI parse, storing them for future use.
- **Web Interface**: A Streamlit app for multi-file uploads, status tracking, JSON preview/download, and a cost/usage summary.

## Tech Stack

- **Language**: Python 3.11+
- **Web Framework**: Streamlit
- **LLM**: Ollama with `phi3:mini` (local)
- **Document Parsing**: PyMuPDF, Tesseract (for OCR)
- **Rule Storage**: SQLite

## Setup and Installation

These instructions are for macOS with Homebrew.

### 1. Prerequisites

Ensure you have Python 3.11+, Homebrew, and Xcode Command Line Tools installed.

### 2. Install System Dependencies

Install Tesseract (for OCR) and Ollama (for the local LLM).

```bash
brew install tesseract
brew install ollama
3. Set Up Python Environment
Clone this repository, create a virtual environment, and install the required Python packages.

bash
Copy code
# Navigate to your project directory
cd multi_format_parser

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
4. Download the LLM Model
Pull the phi3:mini model using Ollama:

bash
Copy code
ollama pull phi3:mini
How to Run the Application
Start the Ollama service (it usually runs as a background service, but you can ensure it's running in a separate terminal):

bash
Copy code
ollama serve
Run the Streamlit application from the project's root directory:

bash
Copy code
streamlit run app.py
Your web browser will open with the application running at http://localhost:8501.

Project Structure
text
Copy code
multi_format_parser/
├── venv/                 # Python virtual environment
├── app.py                # Main Streamlit application file
├── core/
│   ├── database.py       # SQLite database logic
│   └── schema.py         # The normalized JSON schema
├── data/
│   └── parser_memory.db  # SQLite database file (created on first run)
├── parsers/
│   ├── ingestion.py      # Raw text extraction and OCR logic
│   ├── ai_parser.py      # LLM interaction logic
│   └── rule_engine.py    # Signature generation and rule learning/application
├── README.md             # This file
└── requirements.txt      # Python dependencies
