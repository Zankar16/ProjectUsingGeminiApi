import streamlit as st
import os
import pathlib
import textwrap
import google.generativeai as genai
from PIL import Image

genai.configure(api_key='AIzaSyCvkJXn0ynov8qyxLyIxDu1nmBk95dBrrY')
model=genai.GenerativeModel("gemini-pro-vision")
def get_gemini_respond(input,image):
    if input!="":
        response=model.generate_content([input,image])
    else:
        response=model.generate_content(image)
    return response.text

st.set_page_config(page_title="QUESTION ME")

st.header("QUESTION ME FROM GEMINI")
input=st.text_input("Input: ",key="input")
uploaded_file=st.file_uploader("choose an image",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="uploaded image")

submit=st.button("i dare you to solve")
if submit:
    response=get_gemini_respond(input,image)
    st.header("the response is ")
    st.write(response)