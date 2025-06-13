# import streamlit as st
# from utils import export_to_pdf, get_pdf_download_link
# from model_generate import generate_questions
# from db_utils import save_questions
# import os
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from camera_resume_scanner import scan_resume_from_camera


# st.title("\U0001F4BC Smart AI Interview Question Generator")

# # Job roles and topics
# job_roles = ["Data Scientist", "Frontend Developer", "Backend Developer", "DevOps Engineer", "Business Analyst", "AI/ML Engineer"]
# topics = {
#     "Data Scientist": ["Machine Learning", "Data Visualization", "Statistics"],
#     "Frontend Developer": ["React", "HTML/CSS", "JavaScript"],
#     "Backend Developer": ["APIs", "Databases", "Authentication", "Python/Django", "Node.js"],
#     "DevOps Engineer": ["CI/CD", "Docker", "Kubernetes"],
#     "Business Analyst": ["Requirement Gathering", "SQL", "Reporting Tools"],
#     "AI/ML Engineer": ["Model Training", "NLP", "Computer Vision"]
# }

# # Mode selection
# mode = st.radio("Choose Mode", ["Manual", "Resume-Based", "Camera CV Scanner"])

# # Common selections
# selected_job = st.selectbox("\U0001F4BC Select Job Role", job_roles)
# selected_topic = st.selectbox("\U0001F4DA Select Topic", topics[selected_job])

# keywords = []
# resume_score = None

# # Function to calculate resume match score
# def get_resume_score(resume_text, job_keywords):
#     resume_text = resume_text.lower()
#     matched_keywords = [kw for kw in job_keywords if kw.lower() in resume_text]
#     score = int((len(matched_keywords) / len(job_keywords)) * 100)
#     return score, matched_keywords

# if mode == "Resume-Based":
#     resume_file = st.file_uploader("\U0001F4C4 Upload Resume (PDF or TXT)", type=["pdf", "txt"])
#     if resume_file:
#         resume_text = resume_file.read().decode("utf-8", errors="ignore")

#         # Updated resume scoring
#         job_keywords = topics[selected_job]
#         resume_score, matched_keywords = get_resume_score(resume_text, job_keywords)

#         st.metric("\U0001F4CA Resume Relevance Score", f"{resume_score}/100")
#         st.write(f"✅ Matched Keywords: {', '.join(matched_keywords)}")

#         # Also extract top words from resume for question generation
#         keywords = [word for word in resume_text.split() if len(word) > 4][:10]
# elif mode == "Camera CV Scanner":
#     st.info("Activate camera and scan your printed resume.")
    
#     if st.button("📸 Start Camera Scan"):
#         # Capture the resume image
#         resume_image = st.camera_input("Capture your Resume")
        
#         if resume_image is not None:
#             # Save the image locally
#             image_filename = f"resume_{str(int(time.time()))}.jpg"
#             image_path = os.path.join("uploaded_resumes", image_filename)
            
#             # Save the image to the folder
#             with open(image_path, "wb") as f:
#                 f.write(resume_image.getvalue())
            
#             # Perform OCR to extract text
#             resume_text = scan_resume_from_camera(resume_image)
            
#             if resume_text:
#                 job_keywords = topics[selected_job]
#                 resume_score, matched_keywords = get_resume_score(resume_text, job_keywords)

#                 st.metric("📊 Resume Relevance Score", f"{resume_score}/100")
#                 st.write("✅ Matched Keywords:", ", ".join(matched_keywords))

#                 # Optional: Use top frequent words from scan for question generation
#                 keywords = [word for word in resume_text.split() if len(word) > 4][:10]
                
#                 # Save the image path and other relevant information in the database
#                 save_uploaded_image_info(image_filename, resume_text, resume_score)
#             else:
#                 st.warning("⚠️ No text detected or scan cancelled.")
    
# difficulty_levels = ["Medium", "Intermediate", "Advanced"]
# selected_difficulty = st.selectbox("🔥 Select Difficulty Level", difficulty_levels)

# # Question count selection (move this OUTSIDE the button)
# question_options = [5, 10, 20, 50]
# num_questions = st.selectbox("📝 Select Number of Questions", question_options, index=0)

# # Generate questions
# if st.button("\U0001F50D Generate Interview Questions"):
#     all_questions = []
#     try:
#         questions = generate_questions(selected_job, selected_topic, keywords, num_questions=num_questions, difficulty=selected_difficulty)

#         if not questions:
#             st.warning("⚠️ No questions returned from the model.")
#         else:
#             st.subheader(f"{selected_job} - {selected_topic}")
#             for i, q in enumerate(questions, 1):
#                 st.markdown(f"**Q{i}:** {q}")
#             all_questions.extend([(selected_job, selected_topic, q) for q in questions])

#     except Exception as e:
#         st.error(f"⚠️ Failed to generate questions: {e}")

#     if all_questions:
#         for role, topic, question in all_questions:
#             save_questions(role, topic, [question])

#         filename = export_to_pdf(selected_job, selected_topic, [q[2] for q in all_questions])
#         if filename:
#             st.markdown(get_pdf_download_link(filename), unsafe_allow_html=True)

import streamlit as st
from utils import export_to_pdf, get_pdf_download_link
from model_generate import generate_questions
from db_utils import save_questions
import os
import pytesseract
from PIL import Image
import time
from io import BytesIO

st.title("\U0001F4BC Smart AI Interview Question Generator")

# Job roles and topics
job_roles = ["Data Scientist", "Frontend Developer", "Backend Developer", "DevOps Engineer", "Business Analyst", "AI/ML Engineer"]
topics = {
    "Data Scientist": ["Machine Learning", "Data Visualization", "Statistics"],
    "Frontend Developer": ["React", "HTML/CSS", "JavaScript"],
    "Backend Developer": ["APIs", "Databases", "Authentication", "Python/Django", "Node.js"],
    "DevOps Engineer": ["CI/CD", "Docker", "Kubernetes"],
    "Business Analyst": ["Requirement Gathering", "SQL", "Reporting Tools"],
    "AI/ML Engineer": ["Model Training", "NLP", "Computer Vision"]
}

# Mode selection
mode = st.radio("Choose Mode", ["Manual", "Resume-Based", "Camera CV Scanner"])

# Common selections
selected_job = st.selectbox("\U0001F4BC Select Job Role", job_roles)
selected_topic = st.selectbox("\U0001F4DA Select Topic", topics[selected_job])

keywords = []
resume_score = None

# Function to calculate resume match score
def get_resume_score(resume_text, job_keywords):
    resume_text = resume_text.lower()
    matched_keywords = [kw for kw in job_keywords if kw.lower() in resume_text]
    score = int((len(matched_keywords) / len(job_keywords)) * 100)
    return score, matched_keywords

if mode == "Resume-Based":
    resume_file = st.file_uploader("\U0001F4C4 Upload Resume (PDF or TXT)", type=["pdf", "txt"])
    if resume_file:
        resume_text = resume_file.read().decode("utf-8", errors="ignore")

        # Updated resume scoring
        job_keywords = topics[selected_job]
        resume_score, matched_keywords = get_resume_score(resume_text, job_keywords)

        st.metric("\U0001F4CA Resume Relevance Score", f"{resume_score}/100")
        st.write(f"✅ Matched Keywords: {', '.join(matched_keywords)}")

        # Also extract top words from resume for question generation
        keywords = [word for word in resume_text.split() if len(word) > 4][:10]

elif mode == "Camera CV Scanner":
    st.info("Activate camera and scan your printed resume.")

    resume_image = st.camera_input("📸 Capture your Resume")
    if resume_image:
        # Display the captured resume image
        st.image(resume_image, caption="Scanned Resume Preview", use_column_width=True)

        # Read image and perform OCR
        image = Image.open(resume_image)
        resume_text = pytesseract.image_to_string(image)

        if resume_text:
            job_keywords = topics[selected_job]
            resume_score, matched_keywords = get_resume_score(resume_text, job_keywords)

            st.metric("📊 Resume Relevance Score", f"{resume_score}/100")
            st.write("✅ Matched Keywords:", ", ".join(matched_keywords))

            # Extract top words for question generation
            keywords = [word for word in resume_text.split() if len(word) > 4][:10]
        else:
            st.warning("⚠️ No text detected in the resume.")

difficulty_levels = ["Medium", "Intermediate", "Advanced"]
selected_difficulty = st.selectbox("🔥 Select Difficulty Level", difficulty_levels)

# Question count selection (move this OUTSIDE the button)
question_options = [5, 10, 20, 50]
num_questions = st.selectbox("📝 Select Number of Questions", question_options, index=0)

# Generate questions
if st.button("\U0001F50D Generate Interview Questions"):
    all_questions = []
    try:
        questions = generate_questions(selected_job, selected_topic, keywords, num_questions=num_questions, difficulty=selected_difficulty)

        if not questions:
            st.warning("⚠️ No questions returned from the model.")
        else:
            st.subheader(f"{selected_job} - {selected_topic}")
            for i, q in enumerate(questions, 1):
                st.markdown(f"**Q{i}:** {q}")
            all_questions.extend([(selected_job, selected_topic, q) for q in questions])

    except Exception as e:
        st.error(f"⚠️ Failed to generate questions: {e}")

    if all_questions:
        for role, topic, question in all_questions:
            save_questions(role, topic, [question])

        filename = export_to_pdf(selected_job, selected_topic, [q[2] for q in all_questions])
        if filename:
            st.markdown(get_pdf_download_link(filename), unsafe_allow_html=True)

