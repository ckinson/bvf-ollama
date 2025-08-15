# BVF Builder — Sector-Smart (Ollama or OpenAI)

A Streamlit app that ingests company strategy (URLs, PDFs, DOCX, or pasted text) and generates a curated **Business Value Framework (BVF)** with sector-aware labels. The visual mirrors enterprise “strategy → processes → KPIs → priorities → tech enablers”, and exports a **print-ready PDF** of the actual layout.

---

## ✨ What’s new

* **LLM provider switch:** use **Ollama (local)** *or* **OpenAI API** (paste your key in the app).
* **OpenAI SDK compatibility:** works with both **v1.x** and legacy **v0.x** clients (no more “cannot import name `OpenAI`” issues).
* **Visual upgrades:** taller rows, **rounded corners**, **spacers between layers**, and the title **“Business Value Framework” above the boxes**.
* **PDF export of the visual** (A4, **Landscape/Portrait**) via **Kaleido**.
* **Sector auto-detect** (or pick a sector manually) with sector-specific headings.
* **Curated output:** deduped, concise bullets; JSON/CSV exports too.

---

## 🧩 Features

* **Input sources:** paste URLs, upload **PDF/DOCX**, or paste raw text.
* **Industry awareness:** Retail, Insurance, Banking, Telecom, Manufacturing, Healthcare, Public Sector, Technology/SaaS, Utilities/Energy.
* **Layers:**

  * Executive KPIs
  * Financial / Operational KPIs
  * Business processes & functions + function projects
  * Operating KPIs (per function)
  * Business priorities → Technology priorities
* **Exports:** JSON, CSV, and **PDF of the visual layout** (scaled to page with margins).
* **Model options:**

  * **Ollama (local):** `llama3`, `mistral`, `gemma`, `qwen`
  * **OpenAI API:** `gpt-4o-mini`, `gpt-4.1-mini`, `gpt-4o`, `gpt-3.5-turbo`

---

## 🏗️ Installation

> Use a **Python 3.9+** virtual environment. Instructions below include **all** dependencies.

### macOS

1. **Install Ollama (optional, for local mode)**

```bash
brew install ollama
ollama pull llama3
```

2. **Create a project & virtual env**

```bash
mkdir -p ~/Documents/BVF && cd ~/Documents/BVF
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install Python packages**

```bash
pip install streamlit ollama openai python-dotenv requests beautifulsoup4 lxml readability-lxml pdfminer.six plotly pandas pillow python-docx reportlab kaleido
```

4. **Save the app**
   Create a file named **`bvf_app_ollama_utility_sectorized.py`** and paste the app code into it (from the last message).

5. **Run**

* **Ollama mode:** in a **separate terminal**:

  ```bash
  ollama serve
  ```
* **App:**

  ```bash
  streamlit run bvf_app_ollama_utility_sectorized.py
  ```

### Windows (PowerShell)

1. **Install Ollama (optional, for local mode)**
   Download from [https://ollama.ai/download](https://ollama.ai/download), then:

```powershell
ollama pull llama3
```

2. **Create project & virtual env**

```powershell
mkdir $HOME\Documents\BVF
cd $HOME\Documents\BVF
python -m venv .venv
.\.venv\Scripts\activate
```

3. **Install packages**

```powershell
pip install streamlit ollama openai python-dotenv requests beautifulsoup4 lxml readability-lxml pdfminer.six plotly pandas pillow python-docx reportlab kaleido
```

4. **Save the app** as **`bvf_app_ollama_utility_sectorized.py`** (paste in the full code).

5. **Run**

* **Ollama service (optional, local mode):**

  ```powershell
  ollama serve
  ```
* **App:**

  ```powershell
  streamlit run .\bvf_app_ollama_utility_sectorized.py
  ```

---

## 🚀 Using the App

1. **Company name** – e.g., “Aviva Insurance”.
2. **LLM provider** – choose **Ollama (local)** or **OpenAI API**.

   * If **OpenAI API**, paste your **API key** (`sk-...`) into the password field in the UI.
3. **Industry sector** – select a sector or click **Auto-detect sector** after you’ve ingested some text.
4. **Ingest content** – paste URLs, upload PDFs/DOCX, and/or paste raw text.
5. Click **Build BVF** to generate:

   * **Visual** with rounded tiles, spacers, taller rows, and title **above** the layout.
   * **Curated JSON** representation.
6. **Export** – Download **JSON**, **CSV**, or **PDF (visual)**.

   * Pick **Landscape/Portrait** for the PDF in the dropdown.
   * The PDF is rendered via **Kaleido** at high resolution and scaled to the A4 page with margins.

---

## 🔧 Configuration & Models

* **Ollama models:** The dropdown lists `llama3`, `mistral`, `gemma`, and `qwen`. Pull what you intend to use:

  ```bash
  ollama pull mistral
  ```
* **OpenAI models:** Choose from `gpt-4o-mini`, `gpt-4.1-mini`, `gpt-4o`, `gpt-3.5-turbo`.
* **Sector labels:** Headings automatically adapt per sector (e.g., Retail uses “Value Chain & Functions” and “Store / Channel KPIs”; Public Sector uses “Mission Outcomes / KPIs”, etc.).

---

## 🧠 How it Works (high level)

* **Ingestion:** Fetches web pages and PDFs (with `readability-lxml` + `pdfminer.six`); parses DOCX; or uses your pasted text.
* **Generation:** Prompts the selected LLM to emit **strict JSON** for:

  * executive\_kpis, financial\_operational\_kpis,
  * business\_functions, operating\_kpis\_by\_function,
  * function\_projects,
  * business\_priorities → technology\_priorities\_by\_business\_priority.
* **Curation:** Dedupes, caps list lengths, and standardizes ordering.
* **Visualization:** Draws a rounded-corner, layered grid with Plotly shapes and HTML annotations.
* **PDF export:** Uses **Kaleido** to render the exact visual to PNG, then builds a **ReportLab** PDF (A4, landscape/portrait) with proper scaling and margins.

---

## 🧰 Troubleshooting

* **“OpenAI error: cannot import name ‘OpenAI’”**
  The app includes a **compat layer**: it tries **OpenAI v1.x** first, then falls back to **legacy v0.x**.
  Make sure `openai` is installed:

  ```bash
  pip install --upgrade openai
  ```
* **“Image export failed” when downloading PDF**
  Kaleido missing. Install/upgrade:

  ```bash
  pip install --upgrade kaleido
  ```
* **“Cannot connect to Ollama”**
  Ensure you’re running:

  ```bash
  ollama serve
  ```

  …and you’ve pulled the model you selected:

  ```bash
  ollama pull llama3
  ```
* **“Model did not return valid JSON”**
  The app attempts to salvage JSON by trimming to the outermost braces. If it still fails:

  * Try a different model (e.g., `llama3` or `gpt-4o-mini`).
  * Reduce noisy input, or split long inputs into the most relevant sections.

---

## 🔐 Security & Privacy

* **OpenAI key** is entered **in the UI** and kept **only in memory** for the session.
* **Ollama mode** runs entirely **locally**; no data leaves your machine.

---

## 📦 Project Structure

Single-file app by default:

```
bvf_app_ollama_utility_sectorized.py
```

Outputs are generated at runtime (JSON/CSV downloaded via the UI, PDF built on demand).

---

## 🗒️ Changelog (recent)

* **Provider switch:** Ollama or OpenAI + API key field.
* **OpenAI v1/v0 compatibility** helper.
* **Visual polish:** rounded corners, increased row heights, vertical gaps, header title above grid.
* **PDF export of the visual** (A4 landscape/portrait) via Kaleido.
* **Sector auto-detect** and **sector-aware headings**.
* **Curated** list lengths + dedupe.

---

## 📄 License

Internal/demo use unless licensed otherwise. Add your preferred license here.
