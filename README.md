# 🧠 Smart AI Interview Question Generator

A powerful AI-powered tool built with **Python**, **Streamlit**, and **Groq’s LLaMA3 API** that generates intelligent interview questions based on **job role**, **topic**, or **resume content**.

> ✨ Ideal for freshers or professionals to prepare for technical interviews effectively.

---

## 📌 Features

- ✅ **Manual Mode** – Select job role and topic manually to get relevant questions
- 📄 **Resume Upload Mode** – Upload PDF/TXT resume and get personalized questions
- 📷 **Camera CV Scan Mode** – Take photo of printed resume, scan text using OCR (Tesseract), and generate interview questions
- 📊 **Resume Score Analyzer** – Shows match score between resume and job role/topic
- 📝 **Difficulty Levels** – Choose from Medium, Intermediate, or Advanced
- 📤 **Export to PDF** – Save generated questions for offline practice
- 💾 **Question Storage** – Stores questions in SQLite DB for history or tracking

---
## 🔧 Technologies Used

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web App UI |
| Groq (LLaMA 3) | LLM for generating questions |
| Tesseract OCR | Resume text extraction |
| OpenCV | Camera image processing |
| SQLite | Lightweight database |
| PDFKit / ReportLab | Export questions to PDF |

Set Up Virtual Environment
python -m venv venv
venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt


Create .env File
Add your Groq API Key in .env file
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama3-8b-8192

Run App
streamlit run app.py
