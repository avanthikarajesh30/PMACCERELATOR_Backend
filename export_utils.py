
import pandas as pd
from fpdf import FPDF

def export_csv(data, filename="weather.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return filename

def export_json(data, filename="weather.json"):
    df = pd.DataFrame(data)
    df.to_json(filename, orient='records')
    return filename

def export_pdf(data, filename="weather.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Weather Data Report", ln=True)
    for item in data:
        line = ", ".join(f"{k}: {v}" for k, v in item.items())
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(filename)
    return filename