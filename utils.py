from PyPDF2 import PdfReader
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
import base64
import pytesseract
from PIL import Image


def extract_text_from_pdf(pdf_file):
    """text from pdf
    """
    pdf_show = st.sidebar.radio("Want to see the uploaded file",('Yes','No'))
    if pdf_show == 'Yes':
        pdf_data = pdf_file.read()
        # Embed the PDF using Streamlit's markdown feature
        b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    reader = PdfReader(pdf_file)
    return " ".join(page.extract_text() for page in reader.pages)

def extract_text_from_image(image_file):
    """image to text

    Args:
        image_file (_type_): _description_
    """
    image = Image.open(image_file)
    extracted_text = pytesseract.image_to_string(image)
    image_show = st.sidebar.radio("Want to see the uploaded file",('Yes','No'))
    if image_show == 'Yes':
        st.image(image_file)
    return extracted_text
    
