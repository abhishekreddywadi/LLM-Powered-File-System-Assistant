# test_all_tools.py
from fs_tools import FileSystemTools
import json

print("=" * 50)
print("TESTING FILE TOOLS")
print("=" * 50)

# Create our tools
tools = FileSystemTools()

# 1. Create a test folder with files
print("\n📁 STEP 1: Creating test files...")

# Create a test folder
import os
os.makedirs("test_resumes", exist_ok=True)

# Create some dummy resume files
resumes = [
    {"name": "john_resume.txt", "content": "John knows Python and JavaScript"},
    {"name": "jane_resume.txt", "content": "Jane is expert in Python and AWS"},
    {"name": "bob_resume.txt", "content": "Bob knows Java and C++"}
]

for resume in resumes:
    filepath = f"test_resumes/{resume['name']}"
    result = tools.write_file(filepath, resume['content'])
    print(f"  Created: {filepath}")

# 2. Test list_files
print("\n📁 STEP 2: Testing list_files...")
result = tools.list_files("test_resumes")
print(json.dumps(result, indent=2))

# 3. Test read_file
print("\n📁 STEP 3: Testing read_file...")
result = tools.read_file("test_resumes/john_resume.txt")
print(json.dumps(result, indent=2))

# 4. Test search_in_file
print("\n📁 STEP 4: Testing search_in_file...")
result = tools.search_in_file("test_resumes/jane_resume.txt", "Python")
print(json.dumps(result, indent=2))

print("\n✅ All tests complete!")