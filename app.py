import streamlit as st
from parser_py import parse_resume
import docx2txt
import PyPDF2

st.set_page_config(page_title="Resume Parser", layout="centered")

st.title("📄 Resume Parser using NLTK")
st.write("Upload a `.pdf` or `.docx` resume file to extract information like name, email, phone, skills, and education.")

def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif uploaded_file.name.endswith(".docx"):
        return docx2txt.process(uploaded_file)
    else:
        return ""

uploaded_file = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])

if uploaded_file is not None:
    text = extract_text_from_file(uploaded_file)

    if text.strip() == "":
        st.warning("⚠️ No readable text found in the file.")
    else:
        parsed_data = parse_resume(text)

        st.subheader("📌 Extracted Details")
        st.write(f"**Name:** {parsed_data['Name']}")
        st.write(f"**Email:** {parsed_data['Email']}")
        st.write(f"**Phone:** {parsed_data['Phone']}")
        st.write(f"**Skills:** {', '.join(parsed_data['Skills']) if parsed_data['Skills'] else 'Not found'}")

        if parsed_data['Education']:
            st.write("**Education:**")
            for edu in parsed_data['Education']:
                st.write(f"- {edu}")
        else:
            st.write("**Education:** Not found")
