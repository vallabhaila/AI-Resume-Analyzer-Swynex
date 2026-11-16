# AI-Powered Resume Analyzer

### Swynex AI Internship – Task 2

## Project Overview
AI-Powered Resume Analyzer is a Python-based application developed using Streamlit. It compares a candidate's resume with a job description and identifies matching skills, missing skills and areas for improvement.

## Features
- Supports PDF, DOCX and TXT resumes.
- Extracts text from uploaded documents.
- Calculates resume-job similarity.
- Identifies matching skills.
- Detects skills not found in the resume.
- Provides improvement suggestions.
- Allows users to download extracted resume text.

## Technologies Used
- Python
- Streamlit
- Scikit-learn
- TF-IDF
- Cosine Similarity
- pypdf
- python-docx

## Project Workflow
1. Upload a resume.
2. Enter a job description.
3. Extract resume text.
4. Calculate similarity using TF-IDF and cosine similarity.
5. Detect matching and missing skills.
6. Display analysis results and suggestions.

## First Sample Test Result
- Similarity score: 20.9%
- Matching skills: 7
- Skills to develop: 2
- Missing skills: Deep Learning and Natural Language Processing.

These results are from one sample test and do not represent general model accuracy or hiring probability.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Project Screenshots
The repository includes screenshots of:
- Application interface
- Python source code
- First sample analysis result

## Limitations
- Skill detection is keyword-based.
- Similarity is not hiring probability.
- Scanned PDFs may require OCR.
- Results require human review.

## Conclusion
This project demonstrates the practical use of Python, NLP techniques and machine learning libraries to compare resumes with job descriptions.

Developed as part of the Swynex AI Internship – Task 2.

**Developer:** Vallabh Aila
