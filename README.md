# BVF Builder — Sector-Smart (Ollama or OpenAI)

A Streamlit app that ingests company strategy (URLs, PDFs, DOCX, or pasted text) and generates a **Business Value Framework (BVF)** with sector-aware labels. The visual mirrors enterprise “strategy → processes → KPIs → priorities → tech enablers”, and exports a **print-ready PDF** of the actual layout.

---

## ✨ Highlights

- **LLM provider switch:** **Ollama (local)** *or* **OpenAI API** (paste your key in the app).
- **OpenAI SDK compatibility:** works with both **v1.x** and legacy **v0.x** clients.
- **Polished visual:** taller rows, **rounded corners**, **spacers between layers**, and the title **“Business Value Framework” above the boxes**.
- **PDF export of the actual visual** (A4 **Landscape/Portrait**) via **Kaleido**.
- **Sector auto-detect** (or pick a sector manually) with sector-specific headings.
- **Downloads:** **JSON** (no on-screen JSON view) and **CSV**.

---

## 🧩 What the app builds

Layers in the visual:

1) Executive KPIs  
2) Financial / Operational KPIs  
3) Business processes & functions (+ function projects)  
4) Operating KPIs (per function)  
5) Business priorities → Technology priorities

Supported sectors include Retail, Insurance, Banking, Telecom, Manufacturing, Healthcare, Public Sector, Technology/SaaS, Utilities/Energy.

---

## 🛠️ Requirements

- **Python 3.9+**
- Optional (for local inference): **Ollama** with a pulled model (`llama3`, `mistral`, `gemma`, or `qwen`)
- Internet (only needed if you’ll fetch URLs or use OpenAI)

**Python packages** (install inside your virtual environment):
```bash
pip install streamlit ollama openai python-dotenv requests beautifulsoup4 lxml readability-lxml pdfminer.six plotly pandas pillow python-docx reportlab kaleido
```

> **Kaleido** is required for PDF export of the visual. If you see an export error, run:
> ```bash
> pip install --upgrade kaleido
> ```

---

## 🍏 macOS — Install & Run (step-by-step)

### 1) (Optional) Install Ollama & pull a model
If you want to run locally without the cloud:
```bash
brew install ollama
ollama pull llama3
```
Keep the service running in a separate terminal:
```bash
ollama serve
```

### 2) Create project & virtual environment
```bash
mkdir -p ~/Documents/BVF && cd ~/Documents/BVF
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install all Python dependencies
```bash
pip install streamlit ollama openai python-dotenv requests beautifulsoup4 lxml readability-lxml pdfminer.six plotly pandas pillow python-docx reportlab kaleido
```

### 4) Add the app file
Save the app as **`bvf_app_ollama_utility_sectorized.py`** in this folder (paste the latest code you received).

### 5) Run the app
```bash
streamlit run bvf_app_ollama_utility_sectorized.py
```

- In the app, choose **LLM provider**:
  - **Ollama (local):** make sure `ollama serve` is running and you’ve pulled the chosen model.
  - **OpenAI API:** paste your **OpenAI API key** (`sk-...`) into the password field (kept in memory only for the session).

### Mac quick one-liner (after step 4)
```bash
cd ~/Documents/BVF && source .venv/bin/activate && streamlit run bvf_app_ollama_utility_sectorized.py
```

---

## 🪟 Windows — Install & Run (PowerShell)

1) (Optional) Install **Ollama** from https://ollama.ai/download, then:
```powershell
ollama pull llama3
ollama serve
```

2) Create project & venv
```powershell
mkdir $HOME\Documents\BVF
cd $HOME\Documents\BVF
python -m venv .venv
.\.venv\Scripts\activate
```

3) Install packages
```powershell
pip install streamlit ollama openai python-dotenv requests beautifulsoup4 lxml readability-lxml pdfminer.six plotly pandas pillow python-docx reportlab kaleido
```

4) Save the app as **`bvf_app_ollama_utility_sectorized.py`** and run:
```powershell
streamlit run .\bvf_app_ollama_utility_sectorized.py
```

---

## 🚀 Using the app

1) **Company name** (e.g., “Aviva Insurance”).  
2) **LLM provider**: **Ollama (local)** or **OpenAI API** (paste key).  
3) **Industry sector**: pick or **Auto-detect sector** (after ingesting some text).  
4) **Ingest content**: paste URLs, upload PDF/DOCX, and/or paste raw text.  
5) **Build BVF**: generates the visual only (no on-screen JSON).  
6) **Export**:
   - **Download JSON** (schema of the BVF)
   - **Download CSV**
   - **Download PDF (visual)** — choose **Landscape/Portrait** in the dropdown.

---

## 🔧 Notes & Tips

- **OpenAI SDK compatibility**: the app auto-detects **v1.x** or **legacy v0.x** and calls the right client. Just ensure `openai` is installed:
  ```bash
  pip install --upgrade openai
  ```
- **PDF export** uses **Kaleido** to render the exact Plotly visual, then scales to A4 with margins.
- If you see **“Image export failed”**, (re)install Kaleido:
  ```bash
  pip install --upgrade kaleido
  ```
- If **Ollama** connection fails, confirm:
  ```bash
  ollama serve
  ```
  and that you pulled the selected model (e.g., `ollama pull llama3`).

---

## 📦 File layout

Single-file app by default:
```
bvf_app_ollama_utility_sectorized.py
```
All outputs (JSON, CSV, PDF) are created when you export from the UI.

---

## 🔐 Privacy

- **OpenAI key** is entered in the UI and kept **only in memory** for your current session.
- **Ollama** mode is fully **local**; content doesn’t leave your machine.

---

## 🗒️ Changelog (recent)

- Visual: rounded corners, taller rows, spacing between layers, title above layout.
- Removed on-screen JSON view (downloads still available).
- Provider switch (Ollama/OpenAI) + API key field in UI.
- OpenAI v1/v0 compatibility helper.
- PDF export of the actual visual (A4 landscape/portrait).

---

## 📄 License

Internal/demo use unless licensed otherwise. Add your preferred license text here.
