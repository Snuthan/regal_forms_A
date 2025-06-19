def detect_form_type(text: str) -> str:
    text = text.lower()
    if "fc" in text:
        return "FC"
    elif "apr" in text:
        return "APR"
    elif "ecb" in text:
        return "ECB-2"
    return ""
