from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

load_dotenv() #load all environment variables from .env

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-pro-vision")

# Input : role played by model
# Image : Invoice uploaded
# Prompt : Task to be performed on the invoice

def input_image_details(uploaded_image):
    if uploaded_image is not None:
        #read the file into bytes
        bytes_data=uploaded_image.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_image.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
  

def get_response(input,image,prompt): 
    response=model.generate_content([input,image[0],prompt])  # Gemini takes inputs in the form of list
    return response.text

st.set_page_config(page_icon="INVOICE EXTRACTOR")
st.header("MULTILANGUAGE INVOICE EXTRACTOR")

input=st.text_input("Input Prompt :" ,key="input")
uploaded_image=st.file_uploader("Choose an invoice:", type=["png","jpg","jpeg"   ])
image=" " 
if uploaded_image is not None:
    image=Image.open(uploaded_image)
    st.image(image,caption="Uploaded Invoice.", use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an  expert in understanding invoices.We will upload a image as invoice
and you will have to answer any questions based on the uploaded invoice image """

if submit:
    image_data=input_image_details(uploaded_image)
    response=get_response(input_prompt,image_data,input)
    st.subheader("The response is:")
    st.write(response)