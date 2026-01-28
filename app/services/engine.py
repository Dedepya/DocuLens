import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_resume_content(resume_text: str, jd_text: str):
    """Uses OpenAI to compare resume vs JD and generate embeddings."""
    
    system_prompt = (
        "You are an AI Resume Analyzer. Compare the Resume against the Job Description (JD). "
        "Provide a structured analysis in JSON format. Be critical and specific."
    )

    user_prompt = f"""
    JOB DESCRIPTION:
    {jd_text}

    RESUME:
    {resume_text}

    Return a JSON object with:
    {{
        "match_score": (int 0-100),
        "technical_skills_gap": (list of strings),
        "soft_skills_gap": (list of strings),
        "section_feedback": {{
            "summary": "...",
            "experience": "...",
            "education": "..."
        }},
        "rewrite_suggestions": (list of 3 bullet point suggestions)
    }}
    """

    # 1. Get Analysis
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    analysis_data = json.loads(response.choices[0].message.content)

    # 2. Get Embedding for the Resume text
    emb_response = client.embeddings.create(
        input=resume_text[:8000], # OpenAI limit safety
        model="text-embedding-3-small"
    )
    embedding = emb_response.data[0].embedding

    return analysis_data, embedding