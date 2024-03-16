from dotenv import load_dotenv

import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

load_dotenv()  ## load our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#use of gemini vision pro 
def get_gemini_response(pdf_content_1,pdf_content_2,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([pdf_content_1[0],pdf_content_2[0],prompt])
    return response.text

def input_call_transcript_pdf(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def input_financial_pdf(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

#Prompt Template

input_prompt="""

Generate a prompt to analyze the correlation between revenue from operations and sentiments expressed 
in a transcript. Identify positive or negative sentiment in statements made by speakers and validate it 
with corresponding financial data for the quarter. Generate all this based on the text provided below from
two PDFs of earning call transcripts and financial data of one quarter.

I want a response in one single string having the structure{{'Prompt':'','Speaker Name':'','Sentiment by speaker':''}}
"""    

def display_results(output_dict):
    # Display Prompt
    st.subheader("The Prompt:")
    st.write(output_dict['Prompt'])
    # Display Speaker Name
    st.subheader("Speaker Name:")
    st.write(output_dict['Speaker Name'])
    # Display sentiment
    st.subheader("The Sentiment by speaker's statement is:")
    st.write(output_dict['Sentiment by speaker'])

# Streamlit app
st.title("LLM Platform")
st.text("Platform for generating prompt and sentiment regarding Financial statement data")
uploaded_file_1=st.file_uploader("Upload Call Transcript...",type=["pdf"])
uploaded_file_2=st.file_uploader("Upload Financial Data...",type=["pdf"])
submit=st.button("Submit")

if submit:
    if uploaded_file_1 and uploaded_file_2 is not None:
        text_1=input_call_transcript_pdf(uploaded_file_1)
        text_2=input_financial_pdf(uploaded_file_2)
        response= get_gemini_response(text_1,text_2,input_prompt)
        response=response.replace('{{', '{').replace('}}', '}')
        output_dict = eval(response)
        display_results(output_dict)
        #st.subheader(response)