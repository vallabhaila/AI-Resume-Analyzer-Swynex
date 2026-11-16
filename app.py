import re
from pathlib import Path

import streamlit as st
from docx import Document
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

SKILLS = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "artificial intelligence", "data analysis", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "nlp", "natural language processing",
    "generative ai", "large language models", "llm", "prompt engineering",
    "flask", "django", "streamlit", "html", "css", "javascript",
    "react", "git", "github", "docker", "aws", "azure", "power bi",
    "tableau", "excel", "communication", "problem solving", "data structures",
    "algorithms", "rest api", "fastapi", "computer vision"
]

def extract_text(uploaded_file):
    """Extract text from PDF, DOCX, or TXT files."""
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        document = Document(uploaded_file)
        return "\n".join(p.text for p in document.paragraphs)
    if suffix == ".txt":
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    raise ValueError("Please upload a PDF, DOCX, or TXT file.")

def find_skills(text):
    """Find known skills using case-insensitive whole-phrase matching."""
    normalized = text.lower()
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])"
        if re.search(pattern, normalized):
            found.append(skill)
    return sorted(set(found))

def calculate_similarity(resume_text, job_text):
    """Calculate text similarity using TF-IDF vectors and cosine similarity."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([resume_text, job_text])
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100)

st.title("📄 AI-Powered Resume Analyzer")
st.write("Compare a resume with a job description and discover relevant skills and improvement areas.")
st.info("Educational prototype: the score is a text-similarity measure, not a hiring probability or an assessment of a person's ability.")

left, right = st.columns(2)
with left:
    st.subheader("1. Upload your resume")
    resume_file = st.file_uploader("Choose a resume", type=["pdf", "docx", "txt"])
with right:
    st.subheader("2. Add the job description")
    job_description = st.text_area(
        "Paste the job description here",
        height=220,
        placeholder="Example: We are looking for a Python developer with SQL, machine learning, pandas and problem-solving skills..."
    )

if st.button("Analyze Resume", type="primary", use_container_width=True):
    if resume_file is None:
        st.error("Please upload a resume first.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        try:
            resume_text = extract_text(resume_file)
            if len(resume_text.strip()) < 30:
                st.error("Could not extract enough text. If this is a scanned PDF, use a text-based PDF or DOCX file.")
            else:
                score = calculate_similarity(resume_text, job_description)
                resume_skills = set(find_skills(resume_text))
                job_skills = set(find_skills(job_description))
                matched = sorted(resume_skills & job_skills)
                missing = sorted(job_skills - resume_skills)

                st.divider()
                st.header("3. Analysis Results")
                c1, c2, c3 = st.columns(3)
                c1.metric("Resume–job similarity", f"{score:.1f}%")
                c2.metric("Matching skills", len(matched))
                c3.metric("Skills to develop", len(missing))

                st.progress(min(score / 100, 1.0), text="Text similarity score")
                st.caption("The score compares the wording of the two texts using TF-IDF and cosine similarity. It is not a probability of getting hired.")

                a, b = st.columns(2)
                with a:
                    st.subheader("✅ Matching skills")
                    if matched:
                        for skill in matched:
                            st.write(f"• {skill.title()}")
                    else:
                        st.write("No matching skills from the built-in skill list were detected.")
                with b:
                    st.subheader("📌 Skills not found in resume")
                    if missing:
                        for skill in missing:
                            st.write(f"• {skill.title()}")
                    else:
                        st.write("All detected job-description skills were found in the resume.")

                st.subheader("💡 Improvement suggestions")
                suggestions = []
                if missing:
                    suggestions.append("If you genuinely have experience with the missing skills, add clear evidence of them to your resume.")
                    suggestions.append("Consider building a small project or completing a course to develop skills you do not yet have.")
                if score < 30:
                    suggestions.append("Tailor your resume summary and project descriptions to the responsibilities in the job description, without copying claims you cannot support.")
                if not suggestions:
                    suggestions.append("Your resume contains the listed job skills. Improve it further with measurable project outcomes and specific examples.")
                for item in suggestions:
                    st.write(f"• {item}")

                st.download_button(
                    "Download extracted resume text",
                    data=resume_text,
                    file_name="extracted_resume_text.txt",
                    mime="text/plain"
                )
        except Exception as exc:
            st.error(f"Could not analyze this file: {exc}")

st.divider()
st.caption("Built with Python, Streamlit and Scikit-learn | Prototype for learning and demonstration")
