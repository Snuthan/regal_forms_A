
import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="Regal Forms Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Custom CSS for Layout & Styling ---
st.markdown("""
<style>
body {
    background-color: #ffffff;
    color: #222222;
}
section.main > div {
    background-color: #ffffff;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 1rem 0.5rem 1rem;
    background-color: #ffffff;
    border-bottom: 1px solid #ddd;
    margin-bottom: 1.5rem;
}
.navbar-title {
    font-size: 1.8rem;
    font-weight: 600;
    color: #4B0082;
    margin: 0 auto;
}
.navbar-links {
    font-size: 1rem;
    display: flex;
    gap: 1.5rem;
    align-items: center;
}
.navbar-links a {
    color: #4B0082;
    text-decoration: none;
    font-weight: 500;
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



# --- Custom Navbar ---
st.markdown("""
<div class="navbar">
    <div></div>
    <div class="navbar-title">📄 Regal Forms Assistant</div>
    <div class="navbar-links">
        <a href="https://regality.ai" target="_blank">About</a>
        <a href="https://your-contact-link.com" target="_blank">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Main Content: Split into Upload and Results Section ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📥 Upload Documents")
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Form FC or APR (PDF only)", type=["pdf"])
        supporting_docs = st.file_uploader("Upload Supporting Documents", type=["csv", "xlsx", "pdf"], accept_multiple_files=True)
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
        if supporting_docs:
            st.success(f"✅ {len(supporting_docs)} supporting files uploaded.")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("#### 📊 Review Results")
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write("🟣 Ready for Analysis")
        st.caption("Once your documents are uploaded, smart validation and guidance will appear here.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Footer (Optional) ---
st.markdown("""
<hr style="margin-top: 2rem;">
<p style='text-align: center; font-size: 0.85rem; color: grey;'>
© 2025 Regality AI – Powered by Streamlit
</p>
""", unsafe_allow_html=True)
