import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def generate_questions(skills):

    prompt = f"""
    Generate 5 interview questions for these skills:

    {skills}
    """

    response = model.generate_content(prompt)

    return response.text