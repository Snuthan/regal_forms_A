# app.py
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import os
import re
import io
import pytesseract
from PIL import Image

# --- Page Config ---
st.set_page_config(
    page_title="Regal Forms Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Custom CSS ---
st.markdown("""
<style>
.header-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
    margin-bottom: 5px;
}
.header-wrap img {
    height: 50px;
    margin-right: 5px;
}
.header-wrap h1 {
    font-size: 2rem;
    color: #4B0082;
    margin: 0;
}
.nav-links {
    position: absolute;
    top: 20px;
    right: 30px;
}
.nav-links a {
    margin-left: 20px;
    font-weight: 500;
    color: #4B0082;
    text-decoration: none;
}
.section-card {
    background-color: #F9F7FC;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.upload-box {
    border: 2px dashed #4B0082;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    color: #4B0082;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header-wrap">
    <img src="https://raw.githubusercontent.com/Snuthan/regal_forms_A/main/assets/Regality%20logo%20200x200.png" alt="Logo">
    <h1> Regal Forms Assistant</h1>
</div>
<div class="nav-links">
    <a href="https://regality.ai" target="_blank">About</a>
    <a href="https://your-contact-link.com" target="_blank">Contact</a>
</div>
<hr style="margin-top: 0.5rem;">
""", unsafe_allow_html=True)

# --- OCR fallback ---
def ocr_pdf_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img)
        full_text += text + "\n"
    return full_text.lower().replace('–', '-')

# --- Strict Form Type Detection ---
def detect_form_type_from_pdf(pdf_file):
    try:
        file_bytes = pdf_file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        text = full_text.lower().replace('–', '-')

        st.info("🧪 Extracted text length: " + str(len(text)))
        st.code(text[:1000])

        if len(text.strip()) < 20:
            st.warning("📸 Using OCR fallback!")
            pdf_file.seek(0)
            text = ocr_pdf_text(pdf_file)
            st.code(text[:500])

        apr_indicators = [
            "annual performance report", "form apr", "odi - apr", "odi/apr", "odi annual return",
            "overseas direct investment apr", "odi part ii", "apr submission", "apr filing",
            "return on investment abroad", "apr compliance", "apr details",
            "annual filing of overseas investment", "odi compliance report"
        ]

        fc_indicators = [
            "form fc", "financial commitment", "odi part i", "overseas direct investment",
            "fc-gpr", "investment proposal"
        ]

        matched_apr = [kw for kw in apr_indicators if kw in text]
        matched_fc = [kw for kw in fc_indicators if kw in text]

        st.write("✅ Matched APR indicators:", matched_apr)
        st.write("✅ Matched FC indicators:", matched_fc)

        apr_score = len(matched_apr)
        fc_score = len(matched_fc)

        if apr_score >= 2 and apr_score > fc_score:
            return "APR", text
        elif fc_score >= 2 and fc_score > apr_score:
            return "FC", text
        elif apr_score >= 2 and fc_score >= 2:
            return "APR", text
        else:
            return "Unknown", text
    except Exception:
        return "Unknown", ""

# --- Extract Fields from Form Text ---
def extract_fields_from_form(text):
    uin_match = re.search(r'uin[:\s\-]+([A-Z0-9-]+)', text, re.IGNORECASE)
    entity_match = re.search(r'entity name[:\s\-]+([\w\s&.]+)', text, re.IGNORECASE)
    amount_match = re.search(r'(amount|investment)[:\s\-]+([0-9,.]+)', text, re.IGNORECASE)
    fields = {
        "uin": uin_match.group(1).strip() if uin_match else None,
        "entity": entity_match.group(1).strip() if entity_match else None,
        "amount": amount_match.group(2).strip() if amount_match else None
    }
    st.write("🧾 Extracted from Form:", fields)
    return fields

# --- Extract Fields from Supporting Docs ---
def extract_fields_from_support(docs):
    results = {"uin": None, "entity": None, "amount": None}
    for file in docs:
        try:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
            else:
                continue
            for col in df.columns:
                col_lc = col.lower()
                if "uin" in col_lc and results["uin"] is None:
                    results["uin"] = str(df[col].iloc[0])
                elif "entity" in col_lc and results["entity"] is None:
                    results["entity"] = str(df[col].iloc[0])
                elif "amount" in col_lc or "investment" in col_lc:
                    if results["amount"] is None:
                        results["amount"] = str(df[col].iloc[0])
        except Exception:
            pass
    st.write("📎 Extracted from Supporting Docs:", results)
    return results

# --- Main Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📥 Upload Documents")
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        uploaded_form = st.file_uploader("Upload RBI Form (APR or FC) [PDF only]", type=["pdf"], key="form")
        supporting_files = st.file_uploader("Upload Supporting Documents (CSV, Excel, PDF)", type=["csv", "xlsx", "pdf"], accept_multiple_files=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("#### ✅ Validation Results")
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        if uploaded_form:
            form_type, form_text = detect_form_type_from_pdf(uploaded_form)

            if form_type == "Unknown":
                st.error("❌ Unable to confirm the form type based on document content. Please check and re-upload the correct file.")
            else:
                st.success(f"📄 Detected Form Type: {form_type}")

                if supporting_files:
                    form_fields = extract_fields_from_form(form_text)
                    support_fields = extract_fields_from_support(supporting_files)
                    errors = []
                    for field in ["uin", "entity", "amount"]:
                        f_val = form_fields[field].lower().strip() if form_fields[field] else None
                        s_val = support_fields[field].lower().strip() if support_fields[field] else None
                        if f_val and s_val:
                            if f_val != s_val:
                                errors.append(f"❌ Mismatch in {field.upper()}: '{form_fields[field]}' vs '{support_fields[field]}'")

                    if errors:
                        for err in errors:
                            st.error(err)
                    else:
                        st.success("✅ All key fields match between form and supporting documents.")

                else:
                    st.info("ℹ️ Upload supporting documents to validate form consistency.")

        else:
            st.info("📝 Please upload a document for validation.")

        st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<hr style="margin-top: 2rem;">
<p style='text-align: center; font-size: 0.85rem; color: grey;'>
© 2025 Regality AI – Powered by Streamlit
</p>
""", unsafe_allow_html=True)
