# create_resumes.py
import os
from pathlib import Path

print("📝 Creating sample resume files...")

# Create resumes folder
resume_folder = Path("sample_resumes")
resume_folder.mkdir(exist_ok=True)

# Sample resumes data
resumes = [
    {
        "name": "alice_python_resume.txt",
        "content": """ALICE WONDERLAND
Software Engineer

SUMMARY:
Experienced Python developer with 5 years in web development.
Strong background in Django and FastAPI.

SKILLS:
- Python, JavaScript, SQL
- Django, Flask, FastAPI
- AWS, Docker
- Machine Learning basics

EXPERIENCE:
Senior Python Developer at TechCorp (2022-present)
- Built REST APIs using FastAPI
- Implemented authentication systems
- Optimized database queries

EDUCATION:
B.S. Computer Science, MIT"""
    },
    {
        "name": "bob_java_resume.txt", 
        "content": """BOB BUILDER
Backend Developer

SUMMARY:
Java specialist with experience in enterprise applications.
Spring Boot expert.

SKILLS:
- Java, Spring Boot
- Oracle Database
- Microservices
- Maven, Gradle

EXPERIENCE:
Java Developer at EnterpriseInc (2021-present)
- Built microservices using Spring Boot
- Integrated with legacy systems
- Wrote unit tests with JUnit

EDUCATION:
B.S. Software Engineering, Stanford"""
    },
    {
        "name": "charlie_fullstack_resume.txt",
        "content": """CHARLIE CHAPLIN
Full Stack Developer

SUMMARY:
Full stack developer comfortable with Python backend and React frontend.

SKILLS:
- Python, JavaScript, TypeScript
- React, Node.js
- Django, Express
- MongoDB, PostgreSQL
- Docker, AWS

EXPERIENCE:
Full Stack Dev at StartupXYZ (2020-present)
- Built web apps with React + Django
- Deployed to AWS
- Managed CI/CD pipelines

EDUCATION:
B.S. Computer Science, UC Berkeley"""
    },
    {
        "name": "diana_data_resume.pdf",  # We'll make it a PDF
        "content": """DIANA PRINCE
Data Scientist

SUMMARY:
Data scientist specializing in machine learning and NLP.
Python expert with TensorFlow experience.

SKILLS:
- Python, R, SQL
- TensorFlow, PyTorch
- Machine Learning, Deep Learning
- NLP, Computer Vision
- AWS SageMaker

EXPERIENCE:
Data Scientist at AI Labs (2021-present)
- Built ML models for customer prediction
- Implemented NLP pipelines
- Created data visualizations

EDUCATION:
M.S. Data Science, Carnegie Mellon"""
    }
]

# Create files
for resume in resumes:
    filepath = resume_folder / resume["name"]
    with open(filepath, 'w') as f:
        f.write(resume["content"].strip())
    print(f"  ✅ Created: {resume['name']}")

print(f"\n✨ Created {len(resumes)} resume files in '{resume_folder}/'")

# Also create a real PDF (we need to handle this differently)
print("\n📄 Note: For real PDF files, you'd need proper PDF creation.")
print("For testing, we'll use text files with .pdf extension.")