# LLM File Assistant

A Python application that provides file system operations through natural language queries with LLM integration. Designed for processing documents like resumes, this tool combines powerful file operations with an intuitive natural language interface.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **Multi-Format Support**: Read PDF, TXT, and DOCX files with automatic text extraction
- **Two Operating Modes**:
  - **Mock Mode**: Pattern-based processing without any LLM dependencies
  - **OpenRouter Mode**: Cloud API with multiple free models for intelligent processing
- **Function Calling**: Reliable file operations through structured tool definitions
- **Natural Language Interface**: Query files using everyday language
- **Comprehensive Error Handling**: Graceful handling of missing files and invalid operations

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Available Tools](#available-tools)
- [Project Structure](#project-structure)
- [API Key Setup](#api-key-setup)
- [Running the Demo](#running-the-demo)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Python 3.7 or higher** - The project uses modern Python features including type hints and pathlib
- **OpenRouter API Key** (optional) - Only required for cloud LLM mode

---

## Installation

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd llm-file-assistant

# Or simply download and extract the ZIP file
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `PyPDF2>=3.0.0` - For reading PDF files
- `python-docx>=1.0.0` - For reading Word documents (.docx)
- `requests>=2.31.0` - For OpenRouter API calls

---

## Configuration

### Setting Up OpenRouter API Key (Optional)

OpenRouter provides access to multiple free LLM models. To use cloud LLM features:

1. Get your free API key at https://openrouter.ai/keys
2. Set the environment variable:

**Windows (Command Prompt):**
```cmd
set OPENROUTER_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY="your-api-key-here"
```

**Linux/macOS:**
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

### Available Free Models on OpenRouter

- `google/gemma-2-9b-it:free` - Google's efficient 9B model
- `google/gemma-3-27b-it:free` - Google's larger 27B model
- `mistralai/mistral-7b-instruct:free` - Mistral's 7B instruction model
- `openai/gpt-4o-mini` - OpenAI's efficient mini model (may have costs)

---

## Quick Start

### Mock Mode (No API Key Required)

The simplest way to get started - uses pattern matching without any LLM:

```python
# Import the LLMFileAssistant class
from llm_file_assistant import LLMFileAssistant

# Create assistant in mock mode (default)
assistant = LLMFileAssistant()

# Process your first query
response = assistant.process_query("List all files")
print(response)

# Search for specific content
response = assistant.process_query("Find Python developers")
print(response)

# Read a specific file
response = assistant.process_query("Read resume.txt")
print(response)
```

### OpenRouter Mode (API Key Required)

For intelligent processing with cloud LLMs:

```python
import os
from llm_file_assistant import LLMFileAssistant

# Make sure OPENROUTER_API_KEY is set in your environment
# Or pass it directly:
api_key = "sk-or-v1-your-actual-api-key"

# Create assistant with OpenRouter
assistant = LLMFileAssistant(
    use_openrouter=True,
    api_key=api_key,
    model="google/gemma-2-9b-it:free"  # Free model
)

# Now use natural language queries
response = assistant.process_query("Which candidates have React experience?")
print(response)
```

---

## Usage Examples

### 1. Interactive Mode

Run the assistant interactively from the command line:

```bash
# Using mock mode (default)
python llm_file_assistant.py

# The assistant will guide you through available commands
```

**Example Session:**
```
==========================================================
         LLM File Assistant - Help
==========================================================

[DIR] LIST FILES:
   - "List all files in sample_resumes"
   - "Show me all TXT files"
   - "What files are in test_resumes?"

[FILE] READ FILES:
   - "Read alice_frontend.txt"
   - "Show me the content of charlie_full.txt"

[SEARCH] SEARCH:
   - "Find Python developers"
   - "Search for JavaScript skills"
   - "Look for data analysts"

[USER] You: List all files in sample_resumes
[AI] Assistant:
[DIR] Found 3 files in 'sample_resumes':
  - alice_frontend.txt (2.1 KB) - Modified: 2024-01-15 10:30:00
  - bob_backend.txt (1.8 KB) - Modified: 2024-01-15 10:30:00
  - charlie_full.txt (3.2 KB) - Modified: 2024-01-15 10:30:00
```

### 2. Running the Demo Script

The demo script shows all features automatically:

```bash
python demo.py
```

This will demonstrate:
- Listing files in directories
- Reading file contents
- Searching for specific skills
- Direct tool execution

### 3. Direct Tool Usage

You can also use the file system tools directly:

```python
from fs_tools import read_file, list_files, search_in_file, write_file

# List all PDF files in a directory
pdf_files = list_files("sample_resumes", extension=".pdf")
for file in pdf_files:
    print(f"{file['name']} - {file['size']}")

# Read a resume file
result = read_file("sample_resumes/alice_frontend.txt")
if result["success"]:
    print(result["content"])

# Search for a keyword in a file
search_result = search_in_file("sample_resumes/alice_frontend.txt", "Python")
print(f"Found {search_result['total_matches']} matches")

# Write content to a new file
write_result = write_file("output/summary.txt", "This is a summary")
```

### 4. Common Queries

Here are some example queries you can use:

**Listing Files:**
- "List all files in sample_resumes"
- "Show me all TXT files"
- "What files are in test_resumes?"
- "List all PDF files"

**Reading Files:**
- "Read alice_frontend.txt"
- "Show me the content of charlie_full.txt"
- "Display bob_backend.txt"

**Searching:**
- "Find Python developers"
- "Search for JavaScript skills"
- "Look for data analysts"
- "Find candidates with React experience"
- "Search for 'machine learning' in sample_resumes"

**Writing Files:**
- "Write a summary to output.txt"
- "Create a file named results.txt with the findings"

---

## Available Tools

The LLM File Assistant provides four core tools for file operations:

### 1. read_file(filepath)

Read and extract text from PDF, TXT, or DOCX files.

**Parameters:**
- `filepath` (str): Path to the file to read

**Returns:**
```python
{
    "success": True,
    "content": "File text content here...",
    "metadata": {
        "name": "resume.txt",
        "size_bytes": 2048,
        "size_human": "2.0 KB",
        "modified_date": "2024-01-15 10:30:00",
        "extension": ".txt",
        "full_path": "/path/to/resume.txt"
    },
    "error": None
}
```

### 2. list_files(directory, extension=None)

List all files in a directory, optionally filtered by extension.

**Parameters:**
- `directory` (str): Path to the directory to list
- `extension` (str, optional): Filter by file extension (e.g., '.pdf', '.txt')

**Returns:**
```python
[
    {
        "name": "resume1.pdf",
        "size": "1.5 MB",
        "modified_date": "2024-01-15 10:30:00",
        "extension": ".pdf",
        "path": "sample_resumes/resume1.pdf"
    },
    # ... more files
]
```

### 3. write_file(filepath, content)

Write content to a file, creating directories if needed.

**Parameters:**
- `filepath` (str): Path where the file should be written
- `content` (str): Content to write to the file

**Returns:**
```python
{
    "success": True,
    "filepath": "output/summary.txt",
    "bytes_written": 150,
    "message": "Successfully wrote 150 characters to output/summary.txt",
    "error": None
}
```

### 4. search_in_file(filepath, keyword)

Search for a keyword in a file with surrounding context.

**Parameters:**
- `filepath` (str): Path to the file to search
- `keyword` (str): Keyword to search for (case-insensitive)

**Returns:**
```python
{
    "success": True,
    "filepath": "sample_resumes/resume.txt",
    "keyword": "Python",
    "total_matches": 3,
    "matches": [
        {
            "line_number": 15,
            "line_content": "Skills: Python, Django, PostgreSQL",
            "context": "    13: Education\n    14: -------\n>>> 15: Skills: Python, Django, PostgreSQL\n    16: \n    17: Experience"
        },
        # ... more matches
    ],
    "error": None
}
```

---

## Project Structure

```
llm-file-assistant/
├── fs_tools.py              # Part A: Core file system operations
│                            # - read_file(), list_files(), write_file(), search_in_file()
│                            # - Multi-format file reading (PDF, TXT, DOCX)
│
├── llm_file_assistant.py    # Part B: LLM integration layer
│                            # - LLMFileAssistant class
│                            # - Mock mode (pattern matching)
│                            # - OpenRouter mode (cloud API)
│
├── demo.py                  # Quick demonstration script
│                            # - Shows all features without interactive input
│
├── setup_simple.py          # Script to create test data
│                            # - Generates sample resume files
│
├── test_assignment.py       # Test suite for validation
│                            # - Comprehensive tests for all tools
│
├── requirements.txt         # Python dependencies
│                            # - PyPDF2, python-docx, requests
│
├── sample_resumes/          # Sample resume files for testing
│   ├── alice_frontend.txt
│   ├── bob_backend.txt
│   └── charlie_full.txt
│
├── test_resumes/            # Additional test resume files
│   ├── jane_resume.txt
│   ├── john_resume.txt
│   └── bob_resume.txt
│
└── README.md                # This file
```

---

## API Key Setup (OpenRouter)

OpenRouter provides access to multiple free LLM models through a single API.

### Getting Your Free API Key

1. Visit https://openrouter.ai/keys
2. Sign up for a free account
3. Generate your API key
4. Copy the key (starts with `sk-or-v1-`)

### Setting the Environment Variable

**Windows (Command Prompt):**
```cmd
set OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

**Linux/macOS:**
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

**To make it permanent**, add to your shell profile:
- Linux/macOS: Add to `~/.bashrc` or `~/.zshrc`
- Windows: Add to System Environment Variables

### Free Models Available

| Model | Description |
|-------|-------------|
| `google/gemma-2-9b-it:free` | Google's efficient 9B parameter model |
| `google/gemma-3-27b-it:free` | Google's larger 27B parameter model |
| `mistralai/mistral-7b-instruct:free` | Mistral's 7B instruction-tuned model |

---

## Running the Demo

The demo script showcases all features without requiring interactive input:

```bash
python demo.py
```

**Expected Output:**
```
============================================================
   LLM FILE ASSISTANT - DEMO
============================================================

[DEMO 1] Listing files in sample_resumes:
----------------------------------------
[DIR] Found 3 files in 'sample_resumes':
  - alice_frontend.txt (2.1 KB) - Modified: 2024-01-15 10:30:00
  - bob_backend.txt (1.8 KB) - Modified: 2024-01-15 10:30:00
  - charlie_full.txt (3.2 KB) - Modified: 2024-01-15 10:30:00

[DEMO 2] Reading alice_frontend.txt:
----------------------------------------
[FILE] File: alice_frontend.txt
[SIZE] Size: 2.1 KB
[DATE] Modified: 2024-01-15 10:30:00

[CONTENT] Content:
--------------------------------------------------
ALICE JOHNSON
Frontend Developer
...

[DEMO 3] Searching for 'frontend' skills:
----------------------------------------
[SEARCH] Found 'frontend' in 1 file(s):

[FILE] alice_frontend.txt (3 match(es))
   Line 8: Frontend Developer
   Line 22: React, Vue.js, Angular
...

============================================================
   DEMO COMPLETE!
============================================================
```

---

## Troubleshooting

### Issue: "Module not found" Error

**Problem:** Import errors for PyPDF2, python-docx, or requests.

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "File not found" Error

**Problem:** The specified file or directory doesn't exist.

**Solution:**
- Verify the file path is correct
- Use `list_files()` to see available files
- Check that you're in the correct directory

### Issue: OpenRouter API Error

**Problem:** "OpenRouter API error: 401 Unauthorized"

**Solution:**
- Verify your API key is correct
- Check that `OPENROUTER_API_KEY` environment variable is set
- Ensure you haven't exceeded free tier limits

### Issue: "Unsupported file type"

**Problem:** Trying to read a file format that's not supported.

**Solution:**
- Supported formats: PDF (.pdf), TXT (.txt), DOCX (.docx)
- Convert other formats to TXT or DOCX first

### Issue: Pattern matching not recognizing queries (Mock Mode)

**Problem:** Mock mode doesn't understand your query.

**Solution:**
- Use keywords like "list", "read", "search", "find"
- Be specific about file names (include extension)
- Try rephrasing your query
- Consider using OpenRouter mode for more natural language understanding

---

## Architecture Overview

### How It Works

The LLM File Assistant consists of two main parts:

**Part A: File System Tools (`fs_tools.py`)**
- Core Python functions for file operations
- No LLM dependency
- Structured return formats for easy parsing
- Support for PDF, TXT, and DOCX files

**Part B: LLM Integration (`llm_file_assistant.py`)**
- Wrapper around file system tools
- Two modes: Mock (pattern matching) and OpenRouter (cloud LLM)
- Function calling for reliable tool execution
- Conversation history support

### Why This Architecture?

1. **Separation of Concerns**: File operations are separate from LLM logic
2. **Flexibility**: Can use tools with or without an LLM
3. **Testability**: Each tool can be tested independently
4. **Extensibility**: Easy to add new tools or LLM providers

---

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

## License

This project is open source and available under the MIT License.

---

## Acknowledgments

- Built with Python 3.7+
- Uses PyPDF2 for PDF parsing
- Uses python-docx for Word document parsing
- OpenRouter for cloud LLM access
