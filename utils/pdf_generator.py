from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_filled_pdf(form_type, answers, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"RBI Compliance Form - {form_type}")

    c.setFont("Helvetica", 12)
    y = height - 100

    for field, value in answers.items():
        c.drawString(50, y, f"{field}: {value}")
        y -= 25
        if y < 100:
            c.showPage()
            y = height - 100

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 40, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.save()
    return output_path
