# bvf_app_ollama_utility_sectorized.py
# Streamlit BVF Builder (Sector-Smart Utility Layout) using local Ollama
#
# Features:
# - Strict JSON-only prompt with salvage parsing
# - Curated output (deduped, concise)
# - Sector-aware headings (auto-detect or manual)
# - Layered, color-coded layout (utility-style)
# - Local PDF/DOCX upload, URL fetch, raw text
# - Exports: PDF, CSV, JSON
#
# Requirements (install in your venv):
#   pip install streamlit ollama python-dotenv requests beautifulsoup4 lxml readability-lxml pdfminer.six plotly pandas pillow python-docx reportlab
#
# Run:
#   1) ollama serve                 # in another terminal
#   2) ollama pull llama3           # (or mistral / gemma / qwen)
#   3) streamlit run bvf_app_ollama_utility_sectorized.py

import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

import streamlit as st
import requests
from bs4 import BeautifulSoup
from readability import Document as ReadabilityDocument
from pdfminer.high_level import extract_text as pdf_extract_text
import pandas as pd
import plotly.graph_objects as go
from ollama import chat
from docx import Document as DocxDocument
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# ---------------------------
# Streamlit & Colors
# ---------------------------
st.set_page_config(page_title="BVF Builder (Sector Smart • Ollama)", layout="wide")

PALETTE = {
    "bg": "#FFFFFF",
    "exec_band": "#F2F2F2",
    "fin_band": "#F7F7F7",
    "functions_band_label": "#1F4E79",
    "function_tile": "#2E75B6",
    "function_body": "#EAF2FB",
    "kpi_band": "#DDEBF7",
    "priorities_band_label": "#833C99",
    "priority_tile": "#9E57B3",
    "priority_body": "#F3E9F8",
    "text_dark": "#0F172A",
}

# ---------------------------
# Sector labels mapping
# ---------------------------
SECTORS = [
    "Auto-detect from content",
    "Utilities / Energy",
    "Retail",
    "Insurance",
    "Banking",
    "Telecom",
    "Manufacturing",
    "Healthcare",
    "Public Sector",
    "Technology / SaaS",
]

def get_sector_labels(sector: str) -> Dict[str, str]:
    dflt = {
        "exec_label": "Executive KPIs",
        "fin_label": "Financial / Operational KPIs",
        "functions_label": "Business Processes & Functions",
        "op_kpis_label": "Operating KPIs",
        "priorities_label": "Business Priorities",
        "tech_priorities_label": "Technology Priorities",
    }
    mapping = {
        "Utilities / Energy": dflt,
        "Retail": {
            "exec_label": "Executive KPIs",
            "fin_label": "Financial / Operational KPIs",
            "functions_label": "Value Chain & Functions",
            "op_kpis_label": "Store / Channel KPIs",
            "priorities_label": "Growth & Customer Priorities",
            "tech_priorities_label": "Digital & Technology Enablers",
        },
        "Insurance": {
            "exec_label": "Executive KPIs",
            "fin_label": "Financial / Operational KPIs",
            "functions_label": "Value Chain & Functions",
            "op_kpis_label": "Operational KPIs",
            "priorities_label": "Strategic Priorities",
            "tech_priorities_label": "Technology Enablers",
        },
        "Banking": {
            "exec_label": "Executive KPIs",
            "fin_label": "Financial / Operational KPIs",
            "functions_label": "Value Chain & Functions",
            "op_kpis_label": "Operational KPIs",
            "priorities_label": "Transformation Priorities",
            "tech_priorities_label": "Technology Enablers",
        },
        "Telecom": {
            "exec_label": "Executive KPIs",
            "fin_label": "Financial / Operational KPIs",
            "functions_label": "Network & Customer Functions",
            "op_kpis_label": "Operational KPIs",
            "priorities_label": "Growth & Network Priorities",
            "tech_priorities_label": "Technology Enablers",
        },
        "Manufacturing": {
            "exec_label": "Executive KPIs",
            "fin_label": "Financial / Operational KPIs",
            "functions_label": "Operations & Supply Chain Functions",
            "op_kpis_label": "Operational KPIs",
            "priorities_label": "Manufacturing Priorities",
            "tech_priorities_label": "Industry 4.0 Enablers",
        },
        "Healthcare": {
            "exec_label": "Executive KPIs",
            "fin_label": "Financial / Operational KPIs",
            "functions_label": "Clinical & Operational Functions",
            "op_kpis_label": "Clinical / Operational KPIs",
            "priorities_label": "Clinical & Transformation Priorities",
            "tech_priorities_label": "Digital Health Enablers",
        },
        "Public Sector": {
            "exec_label": "Mission Outcomes / KPIs",
            "fin_label": "Financial / Operational KPIs",
            "functions_label": "Programs & Service Functions",
            "op_kpis_label": "Performance KPIs",
            "priorities_label": "Policy & Service Priorities",
            "tech_priorities_label": "GovTech Enablers",
        },
        "Technology / SaaS": {
            "exec_label": "Executive KPIs",
            "fin_label": "Financial / Product KPIs",
            "functions_label": "Product & GTM Functions",
            "op_kpis_label": "Product / Ops KPIs",
            "priorities_label": "Growth & Platform Priorities",
            "tech_priorities_label": "Platform & Engineering Enablers",
        },
    }
    return mapping.get(sector, dflt)

# ---------------------------
# Data Model
# ---------------------------
@dataclass
class BVF:
    company: str
    executive_kpis: List[str] = field(default_factory=list)
    financial_operational_kpis: List[str] = field(default_factory=list)
    business_functions: List[str] = field(default_factory=list)
    operating_kpis_by_function: Dict[str, List[str]] = field(default_factory=dict)
    function_projects: Dict[str, List[str]] = field(default_factory=dict)
    business_priorities: List[str] = field(default_factory=list)
    technology_priorities_by_business_priority: Dict[str, List[str]] = field(default_factory=dict)
    sources: List[str] = field(default_factory=list)

    def curate(self):
        self.executive_kpis = sorted(set([s for s in self.executive_kpis if s.strip()]))[:8]
        self.financial_operational_kpis = sorted(set([s for s in self.financial_operational_kpis if s.strip()]))[:10]
        seen = set(); ordered = []
        for f in self.business_functions:
            if f and f not in seen:
                ordered.append(f); seen.add(f)
        self.business_functions = ordered[:10] if ordered else list(self.operating_kpis_by_function.keys())[:10]
        self.operating_kpis_by_function = {k: sorted(set([x for x in v if x.strip()]))[:8] for k, v in self.operating_kpis_by_function.items()}
        self.function_projects = {k: sorted(set([x for x in v if x.strip()]))[:6] for k, v in self.function_projects.items()}
        self.business_priorities = [*dict.fromkeys([s for s in self.business_priorities if s.strip()])][:8]
        self.technology_priorities_by_business_priority = {k: sorted(set([x for x in v if x.strip()]))[:8] for k, v in self.technology_priorities_by_business_priority.items()}

    def to_frame(self) -> pd.DataFrame:
        rows = []
        for f in self.business_functions:
            rows.append({"Section": "Function Projects", "Lane": f, "Items": "\n".join(self.function_projects.get(f, []))})
        for f, items in self.operating_kpis_by_function.items():
            rows.append({"Section": "Operating KPIs", "Lane": f, "Items": "\n".join(items)})
        for p in self.business_priorities:
            rows.append({"Section": "Business Priority", "Lane": p, "Items": "\n".join(self.technology_priorities_by_business_priority.get(p, []))})
        return pd.DataFrame(rows)

# ---------------------------
# Helpers: ingest
# ---------------------------
def fetch_text(url: str) -> str:
    try:
        if url.lower().endswith(".pdf"):
            return pdf_extract_text(url)
        resp = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        if "application/pdf" in resp.headers.get("Content-Type", ""):
            with open("temp.pdf", "wb") as fh:
                fh.write(resp.content)
            return pdf_extract_text("temp.pdf")
        doc = ReadabilityDocument(resp.text)
        soup = BeautifulSoup(doc.summary(), "lxml")
        return soup.get_text(separator=" ", strip=True)
    except Exception:
        return ""

def read_uploaded_file(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded_file.read())
        return pdf_extract_text("temp_uploaded.pdf")
    elif name.endswith(".docx"):
        doc = DocxDocument(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    else:
        return uploaded_file.read().decode("utf-8", errors="ignore")

# ---------------------------
# LLM: Ollama call + parsing + sector detect
# ---------------------------
def call_ollama(prompt: str, model: str) -> str:
    response = chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def parse_json_safely(output: str) -> Optional[dict]:
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        start = output.find("{"); end = output.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(output[start:end+1])
            except json.JSONDecodeError:
                return None
        return None

def detect_sector(corp_text: str, model: str) -> str:
    options = [s for s in SECTORS if s != "Auto-detect from content"]
    prompt = f"""You are an industry classifier. Choose the single best-fitting sector label from this list:
{options}
Return ONLY the label string, nothing else.

Text:
{corp_text[:6000]}
"""
    out = call_ollama(prompt, model)
    choice = out.strip()
    return choice if choice in options else "Utilities / Energy"

# ---------------------------
# Extraction (sector-agnostic schema)
# ---------------------------
def extract_bvf(company: str, corp_text: str, model: str) -> BVF:
    schema_hint = json.dumps({
        "executive_kpis": ["string"],
        "financial_operational_kpis": ["string"],
        "business_functions": ["string"],
        "operating_kpis_by_function": {"FunctionName": ["KPI1", "KPI2"]},
        "function_projects": {"FunctionName": ["Project1", "Project2"]},
        "business_priorities": ["string"],
        "technology_priorities_by_business_priority": {"BusinessPriorityName": ["Tech priority 1", "Tech priority 2"]},
        "sources": ["string"]
    }, indent=2)

    prompt = f"""You are a senior business strategist.
Company: {company}

GOAL
Produce a curated Business Value Framework (BVF) using the layers below.
Use concise, sector-specific, non-generic language. Remove duplicates and prioritize impact.

LAYOUT & FIELDS (STRICT JSON ONLY):
{schema_hint}

GUIDANCE
- business_functions should reflect end-to-end operations for the client's sector.
- operating_kpis_by_function: include 3–8 crisp, quantifiable KPIs per function.
- function_projects (optional): 3–6 short bullets reflecting realistic initiatives.
- business_priorities: 5–8 transformation themes.
- technology_priorities_by_business_priority: 4–8 technology levers per priority.

RULES
- Return ONLY valid JSON. No explanations, code fences, or extra text.

TEXT TO ANALYZE
{corp_text[:100000]}
"""

    output = call_ollama(prompt, model)
    data = parse_json_safely(output)
    if not data:
        st.error("❌ Model did not return valid JSON after salvage.")
        return BVF(company=company)
    bvf = BVF(company=company, **data)
    bvf.curate()
    return bvf

# ---------------------------
# Visualization helpers
# ---------------------------
def bulletify(items: List[str]) -> str:
    if not items:
        return "—"
    return "<br>".join([f"• {x}" for x in items])

def render_bvf_figure_utility_layout(bvf: BVF, sector_labels: Dict[str, str]) -> go.Figure:
    functions = bvf.business_functions or list(bvf.operating_kpis_by_function.keys())
    functions = functions[:10] if functions else ["Function"]
    n_cols = max(6, len(functions))

    # Row heights
    ROW_EXEC = 1.1
    ROW_FIN = 1.1
    ROW_LABEL = 0.6
    ROW_FUNCTIONS = 2.2
    ROW_OP_KPIS = 2.2
    ROW_PRIORITIES_LABEL = 0.6
    ROW_PRIORITIES = 2.6
    total_rows = ROW_EXEC + ROW_FIN + ROW_LABEL + ROW_FUNCTIONS + ROW_OP_KPIS + ROW_PRIORITIES_LABEL + ROW_PRIORITIES

    fig = go.Figure()
    fig.update_xaxes(visible=False, range=[0, n_cols])
    fig.update_yaxes(visible=False, range=[0, total_rows])
    fig.update_layout(
        height=1080,
        margin=dict(l=30, r=30, t=40, b=30),
        plot_bgcolor=PALETTE["bg"],
        paper_bgcolor=PALETTE["bg"],
        showlegend=False,
    )

    def rect(x0, y0, x1, y1, fill, line=PALETTE["text_dark"], width=1):
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color=line, width=width), fillcolor=fill, layer="below")

    def text_center(x, y, html, size=14, color=PALETTE["text_dark"]):
        fig.add_annotation(x=x, y=y, text=html, showarrow=False, yanchor="middle",
                           font=dict(size=size, color=color))

    # Title
    y = total_rows
    fig.add_annotation(x=n_cols/2, y=y-0.2, text=f"<b>Business Value Framework — {bvf.company}</b>",
                       showarrow=False, yanchor="top", font=dict(size=20, color=PALETTE["text_dark"]))

    # Exec KPIs
    y -= ROW_EXEC
    rect(0, y, n_cols, y+ROW_EXEC, PALETTE["exec_band"])
    exec_text = f"<b>{sector_labels['exec_label']}</b><br><br>" + bulletify(bvf.executive_kpis)
    text_center(n_cols/2, y + ROW_EXEC/2, exec_text)

    # Fin/Op KPIs
    y -= ROW_FIN
    rect(0, y, n_cols, y+ROW_FIN, PALETTE["fin_band"])
    fin_text = f"<b>{sector_labels['fin_label']}</b><br><br>" + bulletify(bvf.financial_operational_kpis)
    text_center(n_cols/2, y + ROW_FIN/2, fin_text)

    # Functions label
    y -= ROW_LABEL
    rect(0, y, n_cols, y+ROW_LABEL, PALETTE["functions_band_label"], line=PALETTE["functions_band_label"], width=0)
    text_center(0.6, y + ROW_LABEL/2, f"<b style='color:white'>{sector_labels['functions_label']}</b>", color="white")

    # Function tiles (with projects)
    y -= ROW_FUNCTIONS
    colw = n_cols / len(functions)
    for i, f in enumerate(functions):
        x0 = i*colw; x1 = (i+1)*colw
        rect(x0, y+ROW_FUNCTIONS*0.75, x1, y+ROW_FUNCTIONS, PALETTE["function_tile"], line=PALETTE["function_tile"], width=0)
        text_center((x0+x1)/2, y+ROW_FUNCTIONS*0.875, f"<b style='color:white'>{f}</b>", size=13, color="white")
        rect(x0, y, x1, y+ROW_FUNCTIONS*0.75, PALETTE["function_body"])
        bullets = bvf.function_projects.get(f, [])
        body = bulletify(bullets)
        text_center((x0+x1)/2, y+ROW_FUNCTIONS*0.375, body, size=12)

    # Operating KPIs per function
    y -= ROW_OP_KPIS
    rect(0, y, n_cols, y+ROW_OP_KPIS, PALETTE["kpi_band"])
    for i, f in enumerate(functions):
        x0 = i*colw; x1 = (i+1)*colw
        kp = bvf.operating_kpis_by_function.get(f, [])
        rect(x0+0.05, y+0.05, x1-0.05, y+ROW_OP_KPIS-0.05, "#FFFFFF")
        text = f"<b>{f} — {sector_labels['op_kpis_label']}</b><br><br>" + bulletify(kp)
        text_center((x0+x1)/2, y+ROW_OP_KPIS/2, text, size=12)

    # Priorities label
    y -= ROW_PRIORITIES_LABEL
    rect(0, y, n_cols, y+ROW_PRIORITIES_LABEL, PALETTE["priorities_band_label"], line=PALETTE["priorities_band_label"], width=0)
    text_center(0.65, y + ROW_PRIORITIES_LABEL/2, f"<b style='color:white'>{sector_labels['priorities_label']}</b>", color="white")

    # Priority tiles with tech
    y -= ROW_PRIORITIES
    priorities = bvf.business_priorities or list(bvf.technology_priorities_by_business_priority.keys())
    if not priorities:
        priorities = ["Priority"]
    if len(priorities) > len(functions):
        priorities = priorities[:len(functions)]
    colw = n_cols / len(priorities)

    for i, p in enumerate(priorities):
        x0 = i*colw; x1 = (i+1)*colw
        rect(x0, y, x1, y+ROW_PRIORITIES, PALETTE["priority_body"])
        rect(x0, y+ROW_PRIORITIES*0.75, x1, y+ROW_PRIORITIES, PALETTE["priority_tile"], line=PALETTE["priority_tile"], width=0)
        hdr = f"<b style='color:white'>{p}</b>"
        text_center((x0+x1)/2, y+ROW_PRIORITIES*0.875, hdr, size=13, color="white")
        techs = bvf.technology_priorities_by_business_priority.get(p, [])
        body = f"<b>{sector_labels['tech_priorities_label']}</b><br><br>" + bulletify(techs)
        text_center((x0+x1)/2, y+ROW_PRIORITIES*0.375, body, size=12)

    return fig

# ---------------------------
# PDF Export
# ---------------------------
def export_bvf_to_pdf(bvf: BVF, filename: str, labels: Dict[str, str]):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []

    def bullets(lst: List[str]):
        return [Paragraph(f"• {x}", styles["Normal"]) for x in lst]

    story.append(Paragraph(f"Business Value Framework — {bvf.company}", styles["Title"]))
    story.append(Spacer(1, 12))

    # Exec KPIs
    story.append(Paragraph(labels["exec_label"], styles["Heading2"]))
    story.append(Spacer(1, 6))
    for p in bullets(bvf.executive_kpis): story.append(p)
    story.append(Spacer(1, 10))

    # Fin/Op KPIs
    story.append(Paragraph(labels["fin_label"], styles["Heading2"]))
    story.append(Spacer(1, 6))
    for p in bullets(bvf.financial_operational_kpis): story.append(p)
    story.append(Spacer(1, 10))

    # Functions & projects
    story.append(Paragraph(labels["functions_label"], styles["Heading2"]))
    story.append(Spacer(1, 6))
    for f in bvf.business_functions:
        story.append(Paragraph(f, styles["Heading3"]))
        story.append(Spacer(1, 4))
        for p in bullets(bvf.function_projects.get(f, [])): story.append(p)
    story.append(Spacer(1, 10))

    # Operating KPIs by function
    story.append(Paragraph(f"{labels['op_kpis_label']} (by function)", styles["Heading2"]))
    story.append(Spacer(1, 6))
    for f, items in bvf.operating_kpis_by_function.items():
        story.append(Paragraph(f, styles["Heading3"]))
        story.append(Spacer(1, 4))
        for p in bullets(items): story.append(p)
    story.append(Spacer(1, 10))

    # Priorities + tech
    story.append(Paragraph(labels["priorities_label"], styles["Heading2"]))
    story.append(Spacer(1, 6))
    for p in bvf.business_priorities:
        story.append(Paragraph(p, styles["Heading3"]))
        story.append(Spacer(1, 4))
        for t in bullets(bvf.technology_priorities_by_business_priority.get(p, [])): story.append(t)

    doc.build(story)

# ---------------------------
# UI
# ---------------------------
st.title("🧭 BVF Builder — Sector Smart (Ollama, Offline)")

company = st.text_input("Company name", placeholder="e.g., Aviva Insurance")
selected_sector = st.selectbox("Industry sector", SECTORS, index=0)
model_name = st.selectbox("Ollama model to use", ["llama3", "mistral", "gemma", "qwen"], index=0)

manual_urls = st.text_area("Optional: paste specific URLs (one per line)", height=100, placeholder="https://example.com/strategy.pdf\nhttps://investors.example.com/annual-report")
manual_text = st.text_area("Paste raw strategy text here", height=200)

uploaded_files = st.file_uploader("Upload local PDF or DOCX strategy files", type=["pdf", "docx"], accept_multiple_files=True)

colA, colB, colC, colD = st.columns(4)
with colA:
    if st.button("Load Uploaded Files"):
        file_text = ""
        for file in uploaded_files or []:
            file_text += "\n\nSOURCE: " + file.name + "\n" + read_uploaded_file(file)
        manual_text += ("\n" + file_text) if file_text else ""
        st.session_state["ingested_text"] = manual_text

with colB:
    if st.button("Fetch from URLs"):
        all_text = ""
        for u in manual_urls.splitlines():
            u = u.strip()
            if u:
                all_text += f"\n\nSOURCE: {u}\n{fetch_text(u)}"
        manual_text += ("\n" + all_text) if all_text else ""
        st.session_state["ingested_text"] = manual_text

with colC:
    if st.button("Auto-detect sector (Ollama)"):
        full_text = st.session_state.get("ingested_text", "") or manual_text
        if not full_text.strip():
            st.warning("Add some text or URLs/files first so I can detect the sector.")
        else:
            sector = detect_sector(full_text, model=model_name)
            st.success(f"Detected sector: {sector}")
            st.session_state["sector"] = sector

with colD:
    build_disabled = not company or not (manual_text.strip() or st.session_state.get("ingested_text", "").strip())
    if st.button("Build BVF (Local Ollama)", disabled=build_disabled):
        full_text = st.session_state.get("ingested_text", "") or manual_text
        with st.spinner("Generating BVF using local Ollama..."):
            bvf = extract_bvf(company, full_text, model=model_name)
            st.session_state["bvf"] = bvf
            if st.session_state.get("sector"):
                st.session_state["sector_locked"] = st.session_state["sector"]

# Results
bvf: Optional[BVF] = st.session_state.get("bvf")
effective_sector = (
    st.session_state.get("sector_locked")
    or (st.session_state.get("sector") if selected_sector == "Auto-detect from content" else selected_sector)
)
if selected_sector != "Auto-detect from content":
    effective_sector = selected_sector
labels = get_sector_labels(effective_sector or "Utilities / Energy")

if bvf and (bvf.executive_kpis or bvf.business_functions):
    st.subheader("Curated BVF (JSON)")
    st.json(asdict(bvf))

    st.subheader("Visual")
    fig = render_bvf_figure_utility_layout(bvf, labels)
    st.plotly_chart(fig, use_container_width=True)

    # Exports
    st.subheader("Export")
    df = bvf.to_frame()
    st.download_button("Download JSON", json.dumps(asdict(bvf), indent=2), file_name=f"{bvf.company}_BVF.json")
    st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), file_name=f"{bvf.company}_BVF.csv", mime="text/csv")

    pdf_filename = f"{bvf.company}_BVF.pdf"
    export_bvf_to_pdf(bvf, pdf_filename, labels)
    with open(pdf_filename, "rb") as pdf_file:
        st.download_button("Download PDF", pdf_file, file_name=pdf_filename, mime="application/pdf")
