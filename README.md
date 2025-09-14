<pre class="p-0 m-0 rounded-xl"><div class="rt-Box relative"><pre><code class="language-markdown"><span class="token">#</span><span class="token"> Multi-Format Document Parser</span><span>
</span>
This project is a Streamlit application designed to ingest documents in various formats (PDFs, scans), parse their content, and produce a single, normalized JSON output.

<span>It features a hybrid, cost-effective pipeline that learns document layouts. It uses an expensive AI model (Ollama </span><span class="token code">`phi3:mini`</span><span>) only for the first encounter with a new layout, then generates and saves cheaper, rule-based methods for all subsequent documents with the same structure.
</span>
<span></span><span class="token">##</span><span class="token"> Key Features</span><span>
</span>
<span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">Normalized Output</span><span class="token">**</span><span>: A single, stable JSON schema for all inputs.
</span><span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">Cost & Scale</span><span class="token">**</span><span>: Avoids using AI on every document by learning and reusing layout "signatures" and rules.
</span><span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">Interpretability</span><span class="token">**</span><span>: Provides a human-readable interpretation log for each file, showing the processing path (AI vs. Rule).
</span><span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">Layout Learning</span><span class="token">**</span><span>: Treats new layouts as unique signatures and learns extraction rules from the initial AI parse, storing them for future use.
</span><span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">Web Interface</span><span class="token">**</span><span>: A Streamlit app for multi-file uploads, status tracking, JSON preview/download, and a cost/usage summary.
</span>
<span></span><span class="token">##</span><span class="token"> Tech Stack</span><span>
</span>
<span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">Language</span><span class="token">**</span><span>: Python 3.11+
</span><span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">Web Framework</span><span class="token">**</span><span>: Streamlit
</span><span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">LLM</span><span class="token">**</span><span>: Ollama with </span><span class="token code">`phi3:mini`</span><span> (local)
</span><span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">Document Parsing</span><span class="token">**</span><span>: PyMuPDF, Tesseract (for OCR)
</span><span></span><span class="token">-</span><span></span><span class="token">**</span><span class="token">Rule Storage</span><span class="token">**</span><span>: SQLite
</span>
<span></span><span class="token">##</span><span class="token"> Setup and Installation</span><span>
</span>
These instructions are for macOS with Homebrew.

<span></span><span class="token">###</span><span class="token"> 1. Prerequisites</span><span>
</span>
Ensure you have Python 3.11+, Homebrew, and Xcode Command Line Tools installed.

<span></span><span class="token">###</span><span class="token"> 2. Install System Dependencies</span><span>
</span>
Install Tesseract (for OCR) and Ollama (for the local LLM).

```bash
brew install tesseract
brew install ollama</code></pre></div></pre>

### 3. Set Up Python Environment

Clone this repository, create a virtual environment, and install the required Python packages.

<pre class="p-0 m-0 rounded-xl"><div class="rt-Box relative"><div class="rt-Flex rt-r-fd-column rt-r-py-1 rt-r-w absolute top-2 z-10 px-[14px]"><div class="rt-Flex rt-r-fd-row rt-r-ai-center rt-r-jc-space-between"><span data-accent-color="gray" class="rt-Text">bash</span></div></div><pre><code class="language-bash"><span class="token"># Navigate to your project directory</span><span>
</span><span></span><span class="token"># cd multi_format_parser</span><span>
</span>
<span></span><span class="token"># Create and activate a virtual environment</span><span>
</span>python3 -m venv venv
<span></span><span class="token">source</span><span> venv/bin/activate
</span>
<span></span><span class="token"># Install Python dependencies</span><span>
</span><span>pip </span><span class="token">install</span><span> -r requirements.txt</span></code></pre></div></pre>

### 4. Download the LLM Model

Pull the phi3:mini model using Ollama.

<pre class="p-0 m-0 rounded-xl"><div class="rt-Box relative"><div class="rt-Flex rt-r-fd-column rt-r-py-1 rt-r-w absolute top-2 z-10 px-[14px]"><div class="rt-Flex rt-r-fd-row rt-r-ai-center rt-r-jc-space-between"><span data-accent-color="gray" class="rt-Text">bash</span></div></div><pre><code class="language-bash"><span>ollama pull phi3:mini</span></code></pre></div></pre>

## How to Run the Application

1. **Start the Ollama service** (it usually runs as a background service, but you can ensure it's running in a separate terminal):
   <pre class="p-0 m-0 rounded-xl"><div class="rt-Box relative"><div class="rt-Flex rt-r-fd-column rt-r-py-1 rt-r-w absolute top-2 z-10 px-[14px]"><div class="rt-Flex rt-r-fd-row rt-r-ai-center rt-r-jc-space-between"><span data-accent-color="gray" class="rt-Text">bash</span></div></div><pre><code class="language-bash"><span>ollama serve</span></code></pre></div></pre>
2. **Run the Streamlit application** from the project's root directory:
   <pre class="p-0 m-0 rounded-xl"><div class="rt-Box relative"><div class="rt-Flex rt-r-fd-column rt-r-py-1 rt-r-w absolute top-2 z-10 px-[14px]"><div class="rt-Flex rt-r-fd-row rt-r-ai-center rt-r-jc-space-between"><span data-accent-color="gray" class="rt-Text">bash</span></div></div><pre><code class="language-bash"><span>streamlit run app.py</span></code></pre></div></pre>

Your web browser will open with the application running at http://localhost:8501.

## Project Structure

<pre class="p-0 m-0 rounded-xl"><div class="rt-Box relative"><div class="rt-Flex rt-r-fd-column rt-r-py-1 rt-r-w absolute top-2 z-10 px-[14px]"><div class="rt-Flex rt-r-fd-row rt-r-ai-center rt-r-jc-space-between"><span data-accent-color="gray" class="rt-Text">text</span></div></div><pre><code class="language-text"><span>multi_format_parser/
</span>├── venv/                 # Python virtual environment
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
└── requirements.txt      # Python dependencies</code></pre></div></pre>
