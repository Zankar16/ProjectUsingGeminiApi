import streamlit as st
import os
import google.generativeai as genai
genai.configure(api_key='**************************')
model=genai.GenerativeModel("gemini-pro")
def get_gemini_respond(question):
    response=model.generate_content(question)
    return response.text
st.set_page_config(page_title="QUESTION ME")
st.header("QUESTION ME FROM GEMINI")
input=st.text_input("Input: ",key="input")
submit=st.button("i dare you to solve")
if submit:
    response=get_gemini_respond(input)
    st.header("the response is ")
    st.write(response)
