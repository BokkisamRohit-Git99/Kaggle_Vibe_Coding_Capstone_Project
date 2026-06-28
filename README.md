# Antigravity Unified Agri-Health-Finance Network

This repository implements a decentralized Multi-Agent Workspace powered by the Google ADK (Agent Development Kit), Model Context Protocol (MCP), Streamlit, and local safety pipelines. It features agentic diagnostics for crop pathology and automated agricultural financial planning, all wrapped in a robust, multi-layer security guardrail.

---

## ⚙️ Core Architecture & Components

The application is structured into modular, decoupled layers to maintain clean separation of concerns:

### 1. 🛡️ Safety & Guardrail Engine
* **File:** `guardrails.py`
* **Implementation:** Implements input validation using `Llama-Guard-3-1B` (via the `project-free-llama/Llama-Guard-3-1B` Hugging Face model).
* **Execution:** Raw user inputs (text + image presence flag) are run through the safety pipeline on a local PyTorch device (CUDA or CPU) before they are sent to the diagnostic models.

### 2. 📡 MCP Geo-Location Telemetry
* **Files:** `location.py` and `geo_server.py`
* **Implementation:** Uses a custom FastMCP server (`ThinAir-Geo-Server`) executing over standard Input/Output (`stdio`) transport.
* **Execution:** Obtains the external network IP and queries IP-based geolocation data autonomously to establish the target region profile without direct user intervention.

### 3. 🔬 Multi-Agent Engine (Google ADK)
* **Pathologist Agent:** `pathologist.py` uses the Google ADK and Gemini models (`gemini-2.5-flash`) to diagnose plant anomalies from text descriptions and uploaded images.
* **Financial Agent:** `finance.py` performs real-time commodities futures analysis and customized micro-insurance suggestions based on the pathology results and detected region.
* **Routing Gateway:** `gateway.py` handles Google Cloud ADK generation. If the Gemini API key is missing or fails, it falls back to a locally hosted Ollama instance (`gemma4` model at `http://localhost:11434`).
* **Prompts:** `templates.py` defines the structured visual layout instructions for the agent outputs.

---

## 📂 Project Structure & Files

Below is the directory map of the project along with a one-liner description of each file:

* `.env.example` — Template configuration file for setting up required API keys.
* `.gitignore` — Specifies files and directories that Git should ignore.
* `README.md` — Project documentation and architectural overview.
* `requirements.txt` — List of required Python packages and dependencies.
* `app.py` — Streamlit user interface serving as the main system dashboard and execution controller.
* `run.py` — Wrapper script that launches the Streamlit application on port 8080 via subprocess.
* `antigravity/__init__.py` — Package initialization file.
* `antigravity/agents/__init__.py` — Subpackage initialization for agents.
* `antigravity/agents/finance.py` — Financial risk analyzer agent using Gemini and Google Search tool.
* `antigravity/agents/gateway.py` — Routing manager that handles fallback logic between Cloud ADK and local Ollama.
* `antigravity/agents/pathologist.py` — Crop anomaly diagnostic agent with Brave Search and multimodal image processing.
* `antigravity/mcp_server/__init__.py` — Subpackage initialization for MCP servers.
* `antigravity/mcp_server/geo_server.py` — FastMCP server providing geo-spatial location details via IP resolution.
* `antigravity/prompts/__init__.py` — Subpackage initialization for prompt configurations.
* `antigravity/prompts/templates.py` — Prompt instructions and output layouts for pathology and financial agents.
* `antigravity/security/__init__.py` — Subpackage initialization for safety security guards.
* `antigravity/security/guardrails.py` — Safety guardrail engine performing local Llama Guard 3 text validation.
* `antigravity/services/__init__.py` — Subpackage initialization for external services.
* `antigravity/services/location.py` — Telemetry module wrapper communicating with the geo-location MCP server over stdio.

---

## 🚀 Setup & Execution Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/BokkisamRohit-Git99/Kaggle_Vibe_Coding_Capstone_Project.git
cd Kaggle_Vibe_Coding_Capstone_Project
```

### 2. Configure a Virtual Environment
Initialize a clean Python environment to avoid dependency conflicts:
* **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
Install all package requirements:
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
1. Copy the example configuration file:
   * **Windows (PowerShell):**
     ```powershell
     Copy-Item .env.example .env
     ```
   * **macOS / Linux:**
     ```bash
     cp .env.example .env
     ```
2. Open `.env` and fill in your authentication credentials:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   *(Note: The system supports fallback to a local Ollama server running `gemma4` if no key is supplied).*

### 5. Launch the Workspace Engine
Execute the Streamlit application using the wrapper launcher script:
```bash
python run.py
```
This runs the web application server on port `8080`. Open your browser and navigate to `http://localhost:8080`.
Alternatively, run the app using:
```bash
streamlit run app.py
```
