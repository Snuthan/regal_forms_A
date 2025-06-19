import pandas as pd
import pdfplumber

def extract_from_csv(file) -> dict:
    df = pd.read_csv(file)
    return df.to_dict(orient="records")[0]

def extract_from_excel(file) -> dict:
    df = pd.read_excel(file)
    return df.to_dict(orient="records")[0]

def extract_from_pdf(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text
