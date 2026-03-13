# setup_simple.py
import os
from pathlib import Path

print("📁 Setting up test folders and files...")

# Create test_resumes folder
test_folder = Path("test_resumes")
test_folder.mkdir(exist_ok=True)

# Create sample_resumes folder  
sample_folder = Path("sample_resumes")
sample_folder.mkdir(exist_ok=True)

# Create test resumes
resumes = [
    {
        "folder": "test_resumes",
        "name": "john_dev.txt",
        "content": """John Developer
Skills: Python, JavaScript, React
Email: john@email.com
Experience: 5 years Python development"""
    },
    {
        "folder": "test_resumes",
        "name": "jane_data.txt", 
        "content": """Jane Data
Skills: Python, SQL, Machine Learning
Email: jane@email.com
Experience: 3 years data science"""
    },
    {
        "folder": "test_resumes",
        "name": "bob_java.txt",
        "content": """Bob Java
Skills: Java, Spring Boot, SQL
Email: bob@email.com
Experience: 7 years Java development"""
    },
    {
        "folder": "sample_resumes",
        "name": "alice_frontend.txt",
        "content": """Alice Frontend
Skills: JavaScript, React, HTML/CSS
Email: alice@email.com
Experience: 4 years frontend dev"""
    },
    {
        "folder": "sample_resumes", 
        "name": "charlie_full.txt",
        "content": """Charlie Fullstack
Skills: Python, JavaScript, Django, React
Email: charlie@email.com
Experience: 6 years fullstack"""
    }
]

# Create files
for resume in resumes:
    filepath = Path(resume["folder"]) / resume["name"]
    with open(filepath, 'w') as f:
        f.write(resume["content"])
    print(f"✅ Created: {resume['folder']}/{resume['name']}")

print(f"\n✨ Created {len(resumes)} resume files!")
print("\n📋 Ready to test! Run: python llm_file_assistant_free.py")