import re
from PyPDF2 import PdfReader
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_skills(text):
    skills_keywords = [
        'python', 'java', 'sql', 'machine learning', 'deep learning', 'nlp',
        'excel', 'power bi', 'tableau', 'communication', 'teamwork', 'cloud',
        'aws', 'azure', 'gcp', 'data analysis', 'data science', 'statistics'
    ]
    doc = nlp(text.lower())
    extracted = set()
    for token in doc:
        if token.text in skills_keywords:
            extracted.add(token.text)
    return list(extracted)
