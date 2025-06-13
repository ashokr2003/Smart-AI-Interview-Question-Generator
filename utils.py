#utils.py
from fpdf import FPDF
import textwrap
import base64

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Interview Questions", ln=True, align="C")
        self.ln(5)

    def add_question(self, number, question, explanation=None):
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 10, f"Q{number}: {question}", align="L")
        if explanation:
            self.set_font("Arial", "", 11)
            wrapped = textwrap.wrap(explanation, 100)
            for line in wrapped:
                self.cell(10)  # indent
                self.multi_cell(0, 8, f"- {line}", align="L")

def get_pdf_download_link(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="questions.pdf">📄 Download PDF</a>'

def export_to_pdf(job_role, topic, questions, filename="questions.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Interview Questions for {job_role} - {topic}", ln=True, align="C")
    pdf.ln(5)

    if not questions:
        pdf.multi_cell(0, 10, "No questions were generated.")
    else:
        for i, question in enumerate(questions, 1):
            if isinstance(question, tuple):
                q_text, explanation = question
            else:
                q_text, explanation = question, None
            pdf.add_question(i, q_text, explanation)

    try:
        pdf.output(filename)
        return filename
    except Exception as e:
        print(f"❌ PDF generation error: {e}")
        return None
