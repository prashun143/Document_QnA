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
os.environ["LANGCHAIN_API_KEY"] = os.getenv["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant. Please provide response to user queries"),
        ("user", "Question:{Question}"),
        ("user"," document:{document}")
    ]
)

st.title("Document QnA")
file_type = st.sidebar.radio("Uploading Image or Pdf file", ('Image', 'Pdf'))

uploaded_file = st.sidebar.file_uploader(label="Upload your Document to start query")
if uploaded_file:
    text_content = ''
    if file_type is 'Pdf':
        text_content = extract_text_from_pdf(uploaded_file)
    if file_type is 'Image':
        text_content = extract_text_from_image(uploaded_file)
    input_text = st.text_input("Please enter your Query here")
    llm = ChatOpenAI(model = "gpt-4o")
    output_parser = StrOutputParser()
    #chain
    chain = prompt | llm | output_parser
    if input_text:
        st.write(chain.invoke({'Question': input_text,'document': text_content}))
else :
    st.error("Please re-upload the file with correct selection of filters in left side")




