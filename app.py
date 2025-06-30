import streamlit as st
from PIL import Image

# --- Page Config ---
st.set_page_config(
    page_title="Regal Forms Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Form Type Detection Function ---
def detect_form_type(file):
    if not file:
        return None
    name = file.name.lower()
    if "fc" in name:
        return "Form FC"
    elif "apr" in name:
        return "Form APR"
    elif "ecb" in name or "ecb-2" in name:
        return "Form ECB-2"
    else:
        return "Unknown form type"

# --- Header: Logo + Title + Links Centered ---
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
    margin-right: 8px;
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
</style>

<div class="header-wrap">
    <img src="assets/Regality%20logo%20200x200.png" alt="Logo">
    <h1>📄 Regal Forms Assistant</h1>
</div>
<div class="nav-links">
    <a href="https://regality.ai" target="_blank">About</a>
    <a href="https://your-contact-link.com" target="_blank">Contact</a>
</div>
<hr style="margin-top: 0.5rem;">
""", unsafe_allow_html=True)

# --- Custom Styling ---
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

# --- Main Content: Upload + Review ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📥 Upload Documents")
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload Form FC, APR, or ECB-2 (PDF only)", type=["pdf"])
        supporting_docs = st.file_uploader("Upload Supporting Documents", type=["csv", "xlsx", "pdf"], accept_multiple_files=True)

        form_type = None
        if uploaded_file:
            form_type = detect_form_type(uploaded_file)
            if form_type == "Unknown form type":
                st.error("❌ Uploaded document does not appear to be a valid Form FC, APR, or ECB-2. Please upload the correct form.")
            else:
                st.success(f"✅ Uploaded: {uploaded_file.name} detected as {form_type}")

        if supporting_docs:
            st.success(f"✅ {len(supporting_docs)} supporting file(s) uploaded.")

        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("#### 📊 Review Results")
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        if uploaded_file and form_type != "Unknown form type":
            st.success(f"✅ Detected form type: **{form_type}**")

            st.markdown("---")
            st.markdown("#### 📝 Field Validation")
            required_fields = ["Applicant Name", "Form Date", "Amount", "Signature"]
            st.write("Validating fields in your document... (placeholder)")
            for field in required_fields:
                st.write(f"- {field}: ⏳ Pending validation")

        elif uploaded_file and form_type == "Unknown form type":
            st.error("❌ Cannot analyze an invalid form. Please upload a correct Form FC, APR, or ECB-2 document.")
        else:
            st.info("🟣 Ready for Analysis - upload a valid form document to detect its type.")
            st.info("Upload a form document to see field validation status.")

        st.caption("Once your documents are uploaded, smart validation and guidance will appear here.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<hr style="margin-top: 2rem;">
<p style='text-align: center; font-size: 0.85rem; color: grey;'>
© 2025 Regality AI – Powered by Streamlit
</p>
""", unsafe_allow_html=True)
