from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv
import base64
from utils import *


load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant. Please provide response to user queries"),
        ("user", "Question:{Question}"),
        ("user"," document:{document}")
    ]
)

st.title("Document QnA")
file_type = st.sidebar.radio("Uploading Image or Pdf file", ('Image', 'Pdf','ProcessedText'))
select_model = st.sidebar.radio("Please select the model to proceed", ('gpt-4o',  'gpt-4o-mini',  'gpt-4',  'gpt-3.5-turbo','chatgpt-4o-latest'))
output_token = st.sidebar.number_input("Please enter the response token limit", min_value= 5, max_value= 500)
uploaded_file = st.sidebar.file_uploader(label="Upload your Document to start query")
if uploaded_file:
    # text_content = ''
    # if file_type is 'Pdf':
    #     text_content = extract_text_from_pdf(uploaded_file)
    # if file_type is 'Image':
    #     text_content = extract_text_from_image(uploaded_file)
    input_text = st.text_input("Please enter your Query here")
    # llm = ChatOpenAI(model = "gpt-4o")
    # output_parser = StrOutputParser()
    # #chain
    # chain = prompt | llm | output_parser
    # if input_text:
    #     st.write(chain.invoke({'Question': input_text,'document': text_content}))
    if file_type == 'Image':
        response = get_openai_response_img(uploaded_file,OPENAI_API_KEY , input_text ,select_model, output_token)
        st.write(response['choices'][0]['message']['content'])
    if file_type == 'Pdf':
        response = get_openai_response_pdf(uploaded_file,OPENAI_API_KEY , input_text ,select_model, output_token)
        st.write(response['choices'][0]['message']['content'])
    
    if file_type == 'ProcessedText':
        text = ''
        image_data = uploaded_file.read()  # Read the image data into memory
        image = Image.open(BytesIO(image_data))
        text = text + [pytesseract.image_to_string(image, lang="tel")]
        st.write(text)
else :
    st.error("Please re-upload the file with correct selection of filters in left side")




