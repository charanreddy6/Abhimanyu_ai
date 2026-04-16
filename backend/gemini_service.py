import os
import json
import asyncio
from google import genai
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 3
RETRY_DELAY = 4  # seconds

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)

async def generate_with_retry(prompt: str) -> str:
    """Call Gemini with up to MAX_RETRIES retries on failure, with RETRY_DELAY seconds between attempts."""
    client = get_client()
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            last_error = e
            print(f"Gemini attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY}s...")
                await asyncio.sleep(RETRY_DELAY)

    raise last_error

def clean_json(text: str) -> str:
    """Strip markdown code fences from Gemini response."""
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


async def generate_questions(skills, role, difficulty, questions_count):
    prompt = f"""
    You are an expert technical interviewer conducting an interview for the role of '{role}'.
    The desired difficulty level is '{difficulty}'.
    The candidate has the following skills: {skills}

    Generate exactly {questions_count} interview questions tailored to these skills, the role, and the difficulty.
    Focus on practical, technical questions as well as scenario-based questions suitable for the specified difficulty.
    
    IMPORTANT: Return ONLY a valid JSON array of strings containing the questions. Do not include markdown formatting like ```json or any other text.
    Example output format:
    ["Question 1?", "Question 2?", ...]
    """

    try:
        text = await generate_with_retry(prompt)
        text = clean_json(text)
        questions = json.loads(text)
        if isinstance(questions, list):
            return questions
        else:
            return [str(q) for q in questions]
    except Exception as e:
        print(f"Error parsing Gemini response after all retries: {e}")
        return ["Could not generate questions. Please try again later."]


async def suggest_skills_and_roles(extracted_skills):
    if not extracted_skills:
        return {
            "suggested_skills": ["python", "java", "javascript", "react", "machine learning", "docker", "aws"],
            "suggested_roles": ["Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Data Scientist"]
        }

    prompt = f"""
    The candidate has the following extracted skills from their resume: {extracted_skills}
    
    Based on these skills, suggest exactly 10 related technical skills they might also possess but aren't listed, and exactly 5 suitable interview roles for this candidate.
    
    Return ONLY a valid JSON object in the following format:
    {{
        "suggested_skills": ["skill1", "skill2"],
        "suggested_roles": ["Role 1", "Role 2"]
    }}
    Do not include markdown formatting or any other text.
    """

    try:
        text = await generate_with_retry(prompt)
        text = clean_json(text)
        data = json.loads(text)
        return dict(data)
    except Exception as e:
        print(f"Error generating suggestions after all retries: {e}")
        return {
            "suggested_skills": ["python", "java", "javascript", "react", "machine learning"],
            "suggested_roles": ["Software Engineer", "Full Stack Developer"]
        }


async def evaluate_answers(questions, answers, role, skills):
    prompt = f"""
    You are an expert technical interviewer evaluating a candidate for the role of '{role}'.
    The candidate has the following skills: {skills}.
    
    Please evaluate the candidate's answers to the following questions.
    Provide a strict JSON response containing an overall score, a feedback summary, and detailed analysis per question.
    Ensure your response is valid JSON that can be parsed with json.loads(). Output ONLY the JSON.
    
    Format:
    {{
      "overall_score": 0-100,
      "feedback_summary": "Brief summary",
      "detailed_analysis": [
        {{
          "question": "Question text",
          "user_answer": "User answer",
          "score": 0-10,
          "strengths": "What was good",
          "improvements": "What was missing"
        }}
      ]
    }}
    
    Questions and Answers:
    """
    for i, (q, a) in enumerate(zip(questions, answers)):
        prompt += f"\nQ{i+1}: {q}\nCandidate Answer {i+1}: {a}\n"

    try:
        text = await generate_with_retry(prompt)
        text = clean_json(text)
        parsed_json = json.loads(text.strip())
        return parsed_json
    except Exception as e:
        print(f"Error evaluating answers after all retries: {str(e)}")
        return {
            "overall_score": 0,
            "feedback_summary": "Failed to generate evaluation due to AI error.",
            "detailed_analysis": []
        }
