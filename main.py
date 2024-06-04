import streamlit as st
import pandas as pd
import PyPDF2
import openai
import os
from io import BytesIO
import pathway as pw  # Importing the Pathway library

# Set your OpenAI API key here
openai.api_key = 'your-api-key'

# Initialize Pathway
pathway_client = pw.Client()

def compare_pdfs(pdf1, pdf2):
    # Read the PDF files
    pdf1_reader = PyPDF2.PdfReader(BytesIO(pdf1.getvalue()))
    pdf2_reader = PyPDF2.PdfReader(BytesIO(pdf2.getvalue()))

    # Initialize a list to store differences
    differences = []

    # Compare the number of pages in both PDFs
    num_pages = min(len(pdf1_reader.pages), len(pdf2_reader.pages))

    # Iterate through each page and compare text
    for i in range(num_pages):
        page1_text = pdf1_reader.pages[i].extract_text()
        page2_text = pdf2_reader.pages[i].extract_text()

        # Use OpenAI API to compare text from both pages
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Find differences between these two texts:\n\nText 1: {page1_text}\n\nText 2: {page2_text}",
            max_tokens=150
        )

        # Add the response to the differences list
        differences.append(response.choices[0].text.strip())

    return differences

def compare_excel(excel1, excel2):
    # Read the Excel files
    df1 = pd.read_excel(excel1)
    df2 = pd.read_excel(excel2)

    # Find differences
    comparison = df1.compare(df2)

    return comparison

st.title('File Comparator using AI')

file_type = st.selectbox('Select file type to compare', ['PDF', 'Excel'])

if file_type == 'PDF':
    pdf1 = st.file_uploader('Upload first PDF', type=['pdf'])
    pdf2 = st.file_uploader('Upload second PDF', type=['pdf'])
    if pdf1 and pdf2:
        differences = compare_pdfs(pdf1, pdf2)
        for i, difference in enumerate(differences):
            st.write(f'Differences in page {i+1}:')
            st.write(difference)

elif file_type == 'Excel':
    excel1 = st.file_uploader('Upload first Excel sheet', type=['xlsx'])
    excel2 = st.file_uploader('Upload second Excel sheet', type=['xlsx'])
    if excel1 and excel2:
        comparison = compare_excel(excel1, excel2)
        st.write('Differences:')
        st.dataframe(comparison)

