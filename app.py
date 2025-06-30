import streamlit as st
from PIL import Image
import PyPDF2

# --- Page Config ---
st.set_page_config(
    page_title="Regal Forms Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Form Type Detection from Filename ---
def detect_form_type(file):
    name = file.name.lower()
    if "fc" in name:
        return "Form FC"
    elif "apr" in name:
        return "Form APR"
    elif "ecb" in name or "ecb-2" in name:
        return "Form ECB-2"
    return "Unknown form type"

# --- Strict Content Checker ---
def is_valid_form_content(file, expected_type):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages[:3]:  # Check first 3 pages
            text += page.extract_text() or ""
        text = text.lower()

        # Define strict keywords for each form type
        keywords = {
            "Form FC": ["foreign contribution", "form fc", "fcr act", "utilization", "donor", "fund"],
            "Form APR": ["annual performance report", "apr", "borrower", "loan", "outstanding amount", "drawdown"]
        }

        # Compare content with expected keywords
        if expected_type in keywords:
            matches = [kw for kw in keywords[expected_type] if kw in text]
            return len(matches) >= 2  # At least 2 keywords must match
        return False
    except Exception as e:
        return False

# --- Header: Logo + Title + Links ---
st.markdown("""
<style>
.header-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 4px;
    margin-top: 10px;
    margin-bottom: 5px;
}
.header-wrap img {
    height: 50px;
}
.header-wrap h1 {
    font-size: 2rem;
    color: #4B0082;
    margin: 0;
    padding: 0;
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
</style>

<div class="header-wrap">
    <img src="assets/Regality%20logo%20200x200.png" alt="Logo">
    <h1> Regal Forms Assistant</h1>
</div>
<div class="nav-links">
    <a href="https://regality.ai" target="_blank">About</a>
    <a href="https://your-contact-link.com" target="_blank">Contact</a>
</div>
<hr style="margin-top: 0.5rem;">
""", unsafe_allow_html=True)

# --- Section Styling ---
st.markdown("""
<style>
body {
    background-color: #ffffff;
    color: #222222;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.section-card {
    background-color: #F9F7FC;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# --- Main Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📥 Upload Documents")
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload Form FC or APR (PDF only)", type=["pdf"])
        supporting_docs = st.file_uploader("Upload Supporting Documents", type=["csv", "xlsx", "pdf"], accept_multiple_files=True)

        form_type = None
        valid_content = False

        if uploaded_file:
            form_type = detect_form_type(uploaded_file)
            valid_content = is_valid_form_content(uploaded_file, form_type)

            if form_type == "Unknown form type":
                st.error("❌ File name doesn't match any supported form (FC/APR). Please rename and try again.")
            elif not valid_content:
                st.error("❌ File name looks like a valid form but its content doesn't match. Please check the document.")
            else:
                st.success(f"✅ Uploaded: {uploaded_file.name} detected as {form_type} and passed validation.")

        if supporting_docs:
            st.success(f"✅ {len(supporting_docs)} supporting file(s) uploaded.")

        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("#### 📊 Review Results")
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        if uploaded_file and form_type != "Unknown form type" and valid_content:
            st.success(f"✅ Detected form type: **{form_type}**")
            st.markdown("---")
            st.markdown("#### 📝 Field Validation")
            required_fields = ["Applicant Name", "Form Date", "Amount", "Signature"]
            for field in required_fields:
                st.write(f"- {field}: ⏳ Pending validation")
        elif uploaded_file:
            st.warning("🟡 Please upload a valid document with correct content to continue.")
        else:
            st.info("🟣 Upload a form to begin analysis.")

        st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<hr style="margin-top: 2rem;">
<p style='text-align: center; font-size: 0.85rem; color: grey;'>
© 2025 Regality AI – Powered by Streamlit
</p>
""", unsafe_allow_html=True)
