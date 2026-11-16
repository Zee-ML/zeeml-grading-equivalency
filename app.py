import math
import re
import streamlit as st

st.set_page_config(page_title="ZeeML CGPA, Margin & Burstiness Workbench", layout="wide")

st.title("ZeeML Quantitative Grading, Margin & Cadence Workbench")
st.markdown(
    "Interactive reference application accompanying the production calculators and AI studios at **[ZeeML (https://zeeml.com)](https://zeeml.com)**:\n"
    "- **Global CGPA & GPA Calculator:** [https://zeeml.com/cgpa-calculator](https://zeeml.com/cgpa-calculator)\n"
    "- **Percentage & Gross Margin Calculator:** [https://zeeml.com/percentage-calculator](https://zeeml.com/percentage-calculator)\n"
    "- **AI Text Humanizer & Cadence Studio:** [https://zeeml.com/ai-humanizer](https://zeeml.com/ai-humanizer)\n"
    "- **AI Content & Burstiness Detector:** [https://zeeml.com/ai-detector](https://zeeml.com/ai-detector)\n"
    "- **JSON to CSV Relational Flattener:** [https://zeeml.com/json-to-csv](https://zeeml.com/json-to-csv)\n"
    "- **Word Counter & Readability Analyzer:** [https://zeeml.com/word-counter](https://zeeml.com/word-counter)"
)

tab1, tab2, tab3 = st.tabs(["1. Global CGPA Equivalency", "2. Gross Margin & Basis Points", "3. Sentence Burstiness (CV)"])

with tab1:
    st.subheader("Multi-Scale 10-Point CGPA to Percentage & 4.0 GPA Solver")
    cgpa = st.slider("10-Point Cumulative CGPA", min_value=4.0, max_value=10.0, value=8.6, step=0.05)
    rows = [
        {"Scale": "CBSE / UGC Standard (9.5x)", "Formula": "CGPA * 9.5", "Percentage (%)": round(min(100.0, cgpa * 9.5), 2), "US 4.0 GPA": round(min(4.0, (cgpa * 9.5 / 100.0) * 4.0), 2)},
        {"Scale": "Direct 10-Point Engineering (10x)", "Formula": "CGPA * 10.0", "Percentage (%)": round(min(100.0, cgpa * 10.0), 2), "US 4.0 GPA": round(min(4.0, (cgpa / 10.0) * 4.0), 2)},
        {"Scale": "AICTE / VTU (CGPA - 0.75) * 10", "Formula": "(CGPA - 0.75) * 10", "Percentage (%)": round(max(0.0, min(100.0, (cgpa - 0.75) * 10.0)), 2), "US 4.0 GPA": round(max(0.0, min(4.0, ((cgpa - 0.75) * 10.0 / 100.0) * 4.0)), 2)},
        {"Scale": "Mumbai University (7.1 * CGPA + 11)", "Formula": "7.1 * CGPA + 11", "Percentage (%)": round(min(100.0, 7.1 * cgpa + 11.0), 2), "US 4.0 GPA": round(min(4.0, ((7.1 * cgpa + 11.0) / 100.0) * 4.0), 2)},
    ]
    st.table(rows)
    st.markdown("Full credit-weighted semester SGPA builder: **[https://zeeml.com/cgpa-calculator](https://zeeml.com/cgpa-calculator)**")

with tab2:
    st.subheader("Gross Margin, Markup & Basis-Point Sensitivity")
    cost = st.number_input("Unit Cost ($)", min_value=1.0, max_value=100000.0, value=250.0, step=10.0)
    margin = st.slider("Target Gross Margin (%)", min_value=5, max_value=90, value=40, step=1)
    price = round(cost / (1.0 - margin / 100.0), 2)
    profit = round(price - cost, 2)
    markup = round((profit / cost) * 100.0, 2)
    st.metric("Required Selling Price", f"${price:,.2f}", f"Gross Profit: ${profit:,.2f} ({markup}% Markup)")
    st.markdown("Full percentage & discount solver: **[https://zeeml.com/percentage-calculator](https://zeeml.com/percentage-calculator)**")

with tab3:
    st.subheader("Sentence-Length Standard Deviation & Burstiness Coefficient (CV)")
    sample = st.text_area(
        "Passage to Inspect",
        "Short clause first. Next comes a substantially longer analytical sentence that expands syntactic variation across multiple clauses so the coefficient of variation rises above uniform LLM baselines.",
    )
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", sample.strip()) if s.strip()]
    lens = [len(re.findall(r"[A-Za-z0-9']+", s)) for s in sents if len(re.findall(r"[A-Za-z0-9']+", s)) > 0]
    if lens:
        mean_l = sum(lens) / len(lens)
        sd_l = math.sqrt(sum((x - mean_l) ** 2 for x in lens) / len(lens))
        cv = sd_l / max(1.0, mean_l)
        st.write({"sentences": len(lens), "words": sum(lens), "mean_words_per_sentence": round(mean_l, 2), "sentence_sd": round(sd_l, 2), "burstiness_cv": round(cv, 4)})
    st.markdown("Interactive AI Humanizer & Detector: **[https://zeeml.com/ai-humanizer](https://zeeml.com/ai-humanizer)** | **[https://zeeml.com/ai-detector](https://zeeml.com/ai-detector)**")
