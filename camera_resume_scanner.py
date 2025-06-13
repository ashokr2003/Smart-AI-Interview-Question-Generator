import pytesseract
import cv2
from PIL import Image
import io
import streamlit as st  # <-- Add this import

# Path to the Tesseract executable (adjust the path based on your installation)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows path example

def scan_resume_from_camera():
    """
    This function captures an image from the camera, performs OCR to extract text,
    and returns the extracted text.
    """
    # Capture image from Streamlit camera input
    image_file = st.camera_input("Capture your Resume")
    
    if image_file is not None:
        # Convert the uploaded image to a format suitable for OCR
        image = Image.open(image_file)
        
        # Convert the image to OpenCV format for OCR processing
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Perform OCR (optical character recognition)
        resume_text = pytesseract.image_to_string(image_cv)

        # Return the extracted resume text
        return resume_text
    return None
