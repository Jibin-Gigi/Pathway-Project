import streamlit as st
import os
import pandas as pd
import openai
import pathway as pw
from pathway.xpacks.llm.llms import OpenAIChat, prompt_chat_single_qa

# Set your OpenAI API key here
openai.api_key = 'your-api-key'

# Initialize the Pathway LLM
llm = OpenAIChat(api_key=openai.api_key)

def compare_files(file1, file2, file_type):
    # Use the AI model to compare the contents of the files
    response = prompt_chat_single_qa(llm, f"Compare two {file_type} files and provide the differences.")
    # Process the response to extract the comparison
    # This is a placeholder, actual implementation will depend on the AI model's response
    differences = response['choices'][0]['message']['content']
    return differences

st.title('File Comparator using AI')

file_type = st.selectbox('Select file type to compare', ['PDF', 'Excel'])

if file_type == 'PDF':
    pdf1 = st.file_uploader('Upload first PDF', type=['pdf'])
    pdf2 = st.file_uploader('Upload second PDF', type=['pdf'])
    if pdf1 and pdf2:
        # Call the compare function
        differences = compare_files(pdf1, pdf2, 'PDF')
        st.write(differences)

elif file_type == 'Excel':
    excel1 = st.file_uploader('Upload first Excel sheet', type=['xlsx'])
    excel2 = st.file_uploader('Upload second Excel sheet', type=['xlsx'])
    if excel1 and excel2:
        # Call the compare function
        differences = compare_files(excel1, excel2, 'Excel')
        st.write(differences)

