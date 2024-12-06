from PyPDF2 import PdfReader
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
import base64
import requests
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes



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


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_openai_response_img(image_file, api_key, text_prompt, model_name, max_tokens):
#   base64_image = encode_image(image_path)
  base64_image = base64.b64encode(image_file.read()).decode('utf-8')
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }
  payload = {
    "model": model_name,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": text_prompt
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": max_tokens
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  return response.json()


import base64
import requests
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from io import BytesIO

def pdf_pages_to_base64_images(pdf_file):
    """
    Converts PDF pages to Base64-encoded image strings.
    Returns a list of Base64-encoded images (JPEG format).
    """
    # Convert PDF to images using pdf2image
    images = convert_from_bytes(pdf_file.read())  # Assuming pdf_file is a file-like object
    base64_images = []

    for image in images:
        # Save image to a BytesIO buffer in JPEG format
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        # Encode the image in Base64
        encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
        base64_images.append(encoded_image)

    return base64_images

def get_openai_response_pdf(pdf_file, api_key, text_prompt, model_name, max_tokens=150):
    """
    Sends images extracted from a PDF file and a text prompt to the OpenAI API for a response.
    """
    # Prepare headers for the OpenAI API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Prepare the payload with the initial text prompt
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text_prompt
                    }
                ]
            }
        ],
        "max_tokens": max_tokens
    }

    # Convert PDF pages to Base64 images and append them to the payload
    base64_images = pdf_pages_to_base64_images(pdf_file)
    for base64_image in base64_images:
        image_data = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }
        payload['messages'][0]['content'].append(image_data)

    # Send the request to the OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Return the API response
    return response.json()
