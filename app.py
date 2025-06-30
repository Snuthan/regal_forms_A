import streamlit as st

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="forms.regality.ai",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS for Styling ----------
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main-header {
        text-align: center;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .main-header h1 {
        margin: 0;
        font-size: 40px;
        color: #4C5FD5;
    }
    .main-header p {
        margin: 0;
        color: #555;
        font-size: 18px;
    }
    .stButton>button {
        background-color: #4C5FD5 !important;
        color: white !important;
        border-radius: 8px;
        padding: 0.6em 1.2em;
    }
    .section-title {
        color: #4C5FD5;
        font-size: 24px;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- App Header ----------
st.markdown("""
    <div class="main-header">
        <h1>forms.regality.ai</h1>
        <p>RBI Compliance. Simplified.</p>
    </div>
""", unsafe_allow_html=True)

# ---------- Sidebar Navigation ----------
with st.sidebar:
    st.markdown("## 🗂️ Navigation")
    if st.button("FC Form"):
        st.session_state["active_form"] = "fc"
    if st.button("APR Form"):
        st.session_state["active_form"] = "apr"
    if st.button("ECB-2 Form"):
        st.session_state["active_form"] = "ecb"

# ---------- Main Content Selector ----------
form = st.session_state.get("active_form", "fc")

# ---------- FC Form Section ----------
if form == "fc":
    st.markdown("### 📝 FC Form", unsafe_allow_html=True)
    st.info("Upload Form FC and its supporting documents for validation.")

    form_fc = st.file_uploader("📄 Upload Form FC (PDF only)", type=["pdf"], key="form_fc_pdf")
    supporting_fc = st.file_uploader("📂 Upload Supporting Files (CSV, XLSX, PDF)",
                                     type=["csv", "xlsx", "pdf"], accept_multiple_files=True,
                                     key="supporting_fc_docs")

    st.markdown("### ✅ Validation Summary")
    if form_fc:
        st.success(f"✅ Form FC uploaded: `{form_fc.name}`")
    else:
        st.warning("⚠ Please upload the Form FC (PDF).")

    if supporting_fc:
        st.success(f"✅ {len(supporting_fc)} supporting document(s) uploaded.")
        for doc in supporting_fc:
            st.markdown(f"- {doc.name} → ✅ Received")
    else:
        st.warning("⚠ No supporting documents uploaded yet.")

# ---------- APR Form Section ----------
elif form == "apr":
    st.markdown("### 📄 APR Form", unsafe_allow_html=True)
    st.info("Upload the official APR form and its supporting documents.")

    form_apr = st.file_uploader("📄 Upload Form APR (PDF only)", type=["pdf"], key="form_apr_apr")
    supporting_docs = st.file_uploader("📂 Upload Supporting Documents (CSV, XLSX, PDF)",
                                       type=["csv", "xlsx", "pdf"], accept_multiple_files=True,
                                       key="supporting_docs_apr")

    st.markdown("### ✅ Validation Summary")
    if form_apr:
        st.success(f"✅ Form APR uploaded: `{form_apr.name}`")
    else:
        st.warning("⚠ Please upload the Form APR (PDF).")

    if supporting_docs:
        st.success(f"✅ {len(supporting_docs)} supporting document(s) uploaded.")
        for file in supporting_docs:
            st.markdown(f"- {file.name} → ✅ Received")
    else:
        st.warning("⚠ No supporting documents uploaded yet.")

# ---------- ECB Placeholder ----------
elif form == "ecb":
    st.markdown("### 📋 ECB-2 Form", unsafe_allow_html=True)
    st.write("This is where the ECB-2 form logic will be added.")

# ---------- Footer ----------
st.markdown("""
    <hr style="margin-top: 40px;">
    <p style='text-align: center; color: grey;'>
        © 2025 Regality AI • <a href="http://forms.regality.ai" target="_blank">forms.regality.ai</a>
    </p>
""", unsafe_allow_html=True)
