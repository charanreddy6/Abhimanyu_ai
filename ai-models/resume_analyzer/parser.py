import pdfplumber

skills_db = ["python", "java", "machine learning", "react", "sql"]

def extract_skills(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    found = []

    for skill in skills_db:
        if skill in text.lower():
            found.append(skill)

    return found