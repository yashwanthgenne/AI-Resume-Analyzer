import streamlit as st
import PyPDF2
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

st.title("AI Resume Analyzer")

resume_file = st.file_uploader("Upload Resume", type=["pdf"])

jd_file = st.file_uploader("Upload Job Description", type=["pdf"])

skills = [
    "Java",
    "Python",
    "MySQL",
    "Spring Boot",
    "REST API",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Machine Learning",
    "NLP"
]

if st.button("Analyze Resume"):

    if resume_file and jd_file:

        resume_reader = PyPDF2.PdfReader(resume_file)
        jd_reader = PyPDF2.PdfReader(jd_file)

        resume_text = ""
        jd_text = ""

        for page in resume_reader.pages:
            resume_text += page.extract_text() or ""

        for page in jd_reader.pages:
            jd_text += page.extract_text() or ""

        resume_lower = resume_text.lower()
        jd_lower = jd_text.lower()

        resume_skills = []
        jd_skills = []

        for skill in skills:

            if skill.lower() in resume_lower:
                resume_skills.append(skill)

            if skill.lower() in jd_lower:
                jd_skills.append(skill)

        missing_skills = []

        for skill in jd_skills:
            if skill not in resume_skills:
                missing_skills.append(skill)

        if len(jd_skills) > 0:
            match_percentage = (
                (len(jd_skills) - len(missing_skills))
                / len(jd_skills)
            ) * 100
        else:
            match_percentage = 0

        st.subheader("Skills Found in Resume")
        st.write(resume_skills)

        st.subheader("Skills Required by Job")
        st.write(jd_skills)

        st.subheader("Missing Skills")
        st.write(missing_skills)

        st.subheader("Resume Match")
        st.metric("Match Score", f"{match_percentage:.0f}%")

        # Gemini AI Analysis
        model = genai.GenerativeModel("gemini-3.8-flash")

        prompt = f"""
You are an AI Resume Analyzer.

Your task is to compare the candidate's resume with the job description.

Analyze only the information provided below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Provide the result in exactly these sections:

1. MATCHING SKILLS
List the skills present in both the resume and job description.

2. MISSING SKILLS
List important skills required by the job but not clearly present in the resume.

3. RESUME IMPROVEMENTS
Give 3 practical suggestions to improve the resume for this job.

4. IMPORTANT KEYWORDS
List keywords from the job description that the candidate should consider adding if they genuinely have those skills.

Do not invent qualifications, skills, projects, or experience.
Keep the response concise and easy to understand.
"""

        response = model.generate_content(prompt)

        st.subheader("AI Analysis")
        st.markdown(response.text)

    else:
        st.warning("Please upload both Resume and Job Description.")