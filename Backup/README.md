Here’s your **full `README.md`** with everything consolidated.
You can save this file as `README.md` in your BVF Builder project folder.

---

````markdown
# 🧭 Business Value Framework (BVF) Builder — Local Ollama Edition

A **Streamlit web application** that generates a **Business Value Framework** from strategy documents, URLs, or raw text — entirely offline using your **local Ollama LLM instance**.

---

## 📌 Overview
This app takes company strategy input (PDF, DOCX, URLs, or text), processes it with a **local AI model** via [Ollama](https://ollama.ai/), and outputs a **curated, sector-specific BVF**:

- **Executive KPIs**
- **Financial / Operational KPIs**
- **Industry Strategies & Initiatives**
- **Business Processes & Functions**
- **Operating KPIs**

The BVF is visualized in an interactive **grid** and can be exported as:
- **PDF** (boardroom ready)
- **CSV** (spreadsheet format)
- **JSON** (machine-readable)

---

## ✨ Features
- Works **fully offline** — no API keys required
- Uses **Ollama** to run local LLMs (`llama3`, `mistral`, `gemma`, `qwen`)
- Accepts:
  - **Local PDF/DOCX** uploads
  - **Direct URLs** to strategy reports
  - **Raw pasted text**
- **Curated output**:
  - Deduplicated
  - Most relevant KPIs & strategies first
- Multiple export formats: **PDF**, **CSV**, **JSON**
- Interactive **BVF visual grid**

---

## 📦 Requirements
- **Python** 3.9+
- **Ollama** (installed locally)
- At least one downloaded **Ollama model** (`llama3` recommended)

---

## 🖥 Installation Instructions

### 1️⃣ Install Ollama

#### **Mac**
```bash
brew install ollama
````

#### **Windows**

1. Download the Windows installer from:
   [https://ollama.ai/download](https://ollama.ai/download)
2. Run the installer and follow the prompts.

---

### 2️⃣ Start Ollama

Once installed, start the Ollama background service:

#### **Mac & Windows**

```bash
ollama serve
```

Leave this running while you use the app.

---

### 3️⃣ Download a Model

The app defaults to `llama3`, but you can also use `mistral`, `gemma`, or `qwen`:

```bash
ollama pull llama3
```

Other models:

```bash
ollama pull mistral
ollama pull gemma
ollama pull qwen
```

---

### 4️⃣ Install Python & Dependencies

#### **Mac**

Check Python:

```bash
python3 --version
```

If missing or old, install via Homebrew:

```bash
brew install python
```

#### **Windows**

Check Python:

```powershell
python --version
```

If missing, install from:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### 5️⃣ Download the App Code

Save the main Python file (e.g., `bvf_app_ollama_full.py`) into a folder.

---

### 6️⃣ Create a Virtual Environment (recommended)

#### **Mac**

```bash
cd path/to/project
python3 -m venv .venv
source .venv/bin/activate
```

#### **Windows (PowerShell)**

```powershell
cd path\to\project
python -m venv .venv
.venv\Scripts\activate
```

---

### 7️⃣ Install Required Python Packages

```bash
pip install streamlit ollama python-dotenv requests beautifulsoup4 lxml readability-lxml pdfminer.six plotly pandas pillow python-docx reportlab
```

---

## 🚀 Running the App

With your virtual environment activated **and** Ollama running:

```bash
streamlit run bvf_app_ollama_full.py
```

The app will open in your browser at:

```
http://localhost:8501
```

---

## 🛠 Using the App

1. **Enter the company name** (e.g., `Aviva Insurance`)
2. **Choose your Ollama model** from the dropdown
3. **Provide strategy input**:

   * Upload **PDF/DOCX** files
   * Paste **URLs**
   * Paste **raw text**
4. Click **Build BVF (Local Ollama)**
5. Review:

   * **Visual grid** of your BVF
   * **Download** as PDF, CSV, or JSON

---

## 📄 Example Output

**Visual grid:**

```
+---------------------------------------------------+
| Executive KPIs  | Financial KPIs  | Strategies... |
+---------------------------------------------------+
| ... Curated lists per section ...                 |
+---------------------------------------------------+
```

**PDF Export:**

* Executive KPIs
* Financial / Operational KPIs
* Industry Strategies & Initiatives
* Business Processes & Functions
* Operating KPIs

---

## 🧠 Tips for Best Results

* Use **sector-specific strategy reports** for best accuracy
* `llama3` is good for general summaries, but `mistral` may produce sharper bullet lists
* If results seem generic, try smaller, targeted source documents

---

## ⚠ Troubleshooting

* **Model not found** → Run `ollama pull llama3` (or your chosen model)
* **Cannot connect to Ollama** → Make sure `ollama serve` is running
* **Python module not found** → Run `pip install <missing_module>`

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 🤝 Credits

* [Ollama](https://ollama.ai/) — local LLM serving
* [Streamlit](https://streamlit.io/) — interactive web interface

```

---

Do you want me to now **append a BVF data flow diagram** to this README so new users instantly understand how inputs → Ollama → BVF output works? That would make it even more visually appealing.
```
