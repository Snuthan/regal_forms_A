import streamlit as st
import json
import os
from PIL import Image
import base64
from chains.form_selector import detect_form_type
from utils.file_utils import extract_from_csv, extract_from_excel, extract_from_pdf
from utils.pdf_generator import generate_filled_pdf

st.set_page_config(page_title="Regal Forms Assistant", layout="centered")

# === Shared keywords ===
GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
FORM_KEYWORDS = ["fc", "apr", "ecb", "fill", "form", "start"]

# === Greeting + relevance helpers ===
def is_greeting(text):
    return text.strip().lower() in GREETINGS

def is_irrelevant(text):
    text = text.lower()
    return not any(keyword in text for keyword in FORM_KEYWORDS + GREETINGS)

# === Load form schemas ===
with open("data/form_schemas.json") as f:
    form_schemas = json.load(f)

# === Session State Initialization ===
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_form" not in st.session_state:
    st.session_state.selected_form = None

if "current_field_index" not in st.session_state:
    st.session_state.current_field_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = {}

if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False

# === Logo + Title (Inline) ===
def get_base64_image(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("assets/logo.png")
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 12px;">
        <img src="data:image/png;base64,{logo_base64}" width="40" height="40">
        <h1 style="margin: 0;">Regal Forms Assistant</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# === Welcome Message ===
st.markdown(
    """
    <div style="margin-top: -10px; margin-bottom: 20px;">
        👋 <b>Welcome to the Regal Forms Assistant!</b><br>
        This AI assistant will help you fill RBI compliance forms (FC, APR, ECB-2) step-by-step.<br>
        You can upload a file, and I’ll auto-fill most of the details for you.
    </div>
    """,
    unsafe_allow_html=True
)

# === File Upload ===
uploaded_file = st.file_uploader("📁 Upload a supporting file (CSV, Excel, or PDF):", type=["csv", "xlsx", "pdf"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]
    if file_type == "csv":
        st.session_state.extracted_data = extract_from_csv(uploaded_file)
    elif file_type == "xlsx":
        st.session_state.extracted_data = extract_from_excel(uploaded_file)
    elif file_type == "pdf":
        raw_text = extract_from_pdf(uploaded_file)
        st.session_state.extracted_data = {"raw_text": raw_text}
    st.success("✅ File processed! I’ll auto-fill whatever I can.")

# === Chat Input ===
user_input = st.chat_input("Type something like 'Fill Form FC'...")

# === Step 1: Greeting, Irrelevant, or Form Selection ===
if user_input and not st.session_state.selected_form:
    st.session_state.messages.append(("user", user_input))

    if is_greeting(user_input):
        reply = "👋 Hello! I'm here to help you fill RBI forms like FC, APR, and ECB-2. Just type 'Fill Form FC' to get started."

    elif is_irrelevant(user_input):
        reply = "🤖 I'm designed to assist with RBI compliance forms like FC, APR, and ECB-2. Try saying 'Fill Form FC' to begin."

    else:
        form_type = detect_form_type(user_input)
        if form_type:
            st.session_state.selected_form = form_type
            st.session_state.answers = {}
            st.session_state.current_field_index = 0
            reply = f"✅ You selected **Form {form_type}**.\n\nLet me fill in what I can from the uploaded file."
        else:
            reply = "❌ I couldn't detect the form. Try 'Fill Form FC', 'Start APR', or 'Open ECB-2'."

    st.session_state.messages.append(("assistant", reply))

# === Step 2: Field Handling ===
elif user_input and st.session_state.selected_form:
    st.session_state.messages.append(("user", user_input))

    fields = form_schemas.get(st.session_state.selected_form, [])
    idx = st.session_state.current_field_index
    if idx < len(fields):
        prev_field = fields[idx]
        st.session_state.answers[prev_field] = user_input
        st.session_state.current_field_index += 1

    while st.session_state.current_field_index < len(fields):
        current_field = fields[st.session_state.current_field_index]
        if current_field in st.session_state.extracted_data:
            st.session_state.answers[current_field] = st.session_state.extracted_data[current_field]
            st.session_state.current_field_index += 1
        else:
            reply = f"Please enter **{current_field}**:"
            st.session_state.messages.append(("assistant", reply))
            break
    else:
        reply = "✅ All fields filled!\n\n### Your Responses:"
        for k, v in st.session_state.answers.items():
            reply += f"\n- **{k}**: {v}"
        reply += "\n\n(To reset, refresh the page.)"
        st.session_state.messages.append(("assistant", reply))

        # === Generate PDF ===
        pdf_path = os.path.join("state", f"{st.session_state.selected_form}_filled.pdf")
        generate_filled_pdf(
            st.session_state.selected_form,
            st.session_state.answers,
            pdf_path
        )
        st.session_state.pdf_ready = True
        st.session_state.pdf_path = pdf_path

# === Display Chat ===
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)

# === PDF Download Button ===
if st.session_state.get("pdf_ready", False):
    try:
        with open(st.session_state.pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Filled PDF",
                data=f,
                file_name=f"{st.session_state.selected_form}_filled.pdf",
                mime="application/pdf"
            )
    except FileNotFoundError:
        st.error("⚠ PDF file not found. Please try again.")
