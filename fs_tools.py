"""
fs_tools.py - Core File System Tools for LLM Function Calling
==============================================================
This module provides structured tools that an LLM can call to work with files.
Each function returns a structured response that the LLM can understand.

Assignment Part A: Core File System Tools (60%)
"""

import os
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional, Union

# Import libraries for reading different file formats
import PyPDF2
import docx


def read_file(filepath: str) -> Dict:
    """
    Read resume files (PDF, TXT, DOCX) and extract text content.

    Args:
        filepath (str): Path to the file to read

    Returns:
        dict: Structured response containing:
            - success (bool): Whether the operation succeeded
            - content (str): The extracted text content
            - metadata (dict): File information (name, size, modified_date, extension)
            - error (str, optional): Error message if failed

    Example:
        >>> result = read_file("resumes/john_doe.pdf")
        >>> print(result["content"])
    """
    # Convert to Path object for easier manipulation
    file_path = Path(filepath)

    try:
        # Check if file exists before attempting to read
        if not file_path.exists():
            return {
                "success": False,
                "content": None,
                "metadata": None,
                "error": f"File not found: {filepath}"
            }

        # Extract file metadata (information about the file)
        stats = file_path.stat()
        metadata = {
            "name": file_path.name,
            "size_bytes": stats.st_size,
            "size_human": _format_size(stats.st_size),
            "modified_date": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "extension": file_path.suffix.lower(),
            "full_path": str(file_path.absolute())
        }

        # Extract content based on file type
        content = _extract_text_by_file_type(file_path)

        return {
            "success": True,
            "content": content,
            "metadata": metadata,
            "error": None
        }

    except Exception as e:
        # Handle any errors gracefully and return structured error response
        return {
            "success": False,
            "content": None,
            "metadata": None,
            "error": f"Error reading file: {str(e)}"
        }


def _extract_text_by_file_type(file_path: Path) -> str:
    """
    Helper function to extract text from different file formats.
    This is an internal function used by read_file.

    Args:
        file_path (Path): Path object pointing to the file

    Returns:
        str: Extracted text content
    """
    extension = file_path.suffix.lower()

    # Handle plain text files
    if extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    # Handle PDF files using PyPDF2
    elif extension == '.pdf':
        text_content = []
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            # Iterate through each page and extract text
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text.strip():  # Only add non-empty pages
                    text_content.append(page_text)
        return '\n\n'.join(text_content)

    # Handle Word documents (.docx) using python-docx
    elif extension == '.docx':
        doc = docx.Document(file_path)
        # Extract text from all paragraphs
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return '\n'.join(paragraphs)

    # Unsupported file type
    else:
        return f"Unsupported file type: {extension}"


def _format_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format (KB, MB, etc.)

    Args:
        size_bytes (int): Size in bytes

    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def list_files(directory: str, extension: Optional[str] = None) -> List[Dict]:
    """
    List all files in a directory, optionally filtered by extension.

    Args:
        directory (str): Path to the directory to list
        extension (str, optional): Filter by file extension (e.g., '.pdf', '.txt')

    Returns:
        list: List of dictionaries containing file metadata:
            - name (str): Filename
            - size (str): Human-readable file size
            - modified_date (str): Last modification timestamp
            - extension (str): File extension
            - path (str): Relative path to the file

    Example:
        >>> files = list_files("resumes", extension=".pdf")
        >>> for file in files:
        ...     print(file["name"])
    """
    dir_path = Path(directory)

    # Check if directory exists
    if not dir_path.exists():
        return [{
            "error": f"Directory not found: {directory}"
        }]

    if not dir_path.is_dir():
        return [{
            "error": f"Path is not a directory: {directory}"
        }]

    files_list = []

    # Iterate through all items in the directory
    for item in dir_path.iterdir():
        # Only process files, not subdirectories
        if item.is_file():
            # Apply extension filter if provided
            if extension:
                # Normalize extension comparison (both should start with dot)
                file_ext = item.suffix.lower()
                filter_ext = extension.lower() if extension.startswith('.') else f'.{extension.lower()}'
                if file_ext != filter_ext:
                    continue

            # Get file statistics
            stats = item.stat()

            file_info = {
                "name": item.name,
                "size": _format_size(stats.st_size),
                "modified_date": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "extension": item.suffix.lower(),
                "path": str(item)
            }
            files_list.append(file_info)

    return files_list


def write_file(filepath: str, content: str) -> Dict:
    """
    Write content to a file, creating directories if needed.

    Args:
        filepath (str): Path where the file should be written
        content (str): Content to write to the file

    Returns:
        dict: Response containing:
            - success (bool): Whether the operation succeeded
            - filepath (str): Path to the written file
            - bytes_written (int): Number of bytes written
            - message (str): Success message
            - error (str, optional): Error message if failed

    Example:
        >>> result = write_file("output/summary.txt", "This is a summary")
        >>> print(result["message"])
    """
    file_path = Path(filepath)

    try:
        # Create parent directories if they don't exist
        # parents=True creates all parent directories
        # exist_ok=True doesn't error if directory already exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content to file with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Get file stats after writing
        stats = file_path.stat()

        return {
            "success": True,
            "filepath": str(file_path),
            "bytes_written": len(content.encode('utf-8')),
            "message": f"Successfully wrote {len(content)} characters to {filepath}",
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "filepath": str(file_path),
            "bytes_written": 0,
            "message": None,
            "error": f"Error writing file: {str(e)}"
        }


def search_in_file(filepath: str, keyword: str) -> Dict:
    """
    Search for keywords in file content, returning matches with context.

    This function performs a case-insensitive search and returns
    matching lines along with surrounding context.

    Args:
        filepath (str): Path to the file to search
        keyword (str): Keyword to search for (case-insensitive)

    Returns:
        dict: Response containing:
            - success (bool): Whether the operation succeeded
            - filepath (str): Path to the searched file
            - keyword (str): The keyword that was searched
            - total_matches (int): Total number of matches found
            - matches (list): List of match dictionaries with:
                - line_number (int): Line number where match was found
                - line_content (str): The full line content
                - context (str): Surrounding lines (2 before, 2 after)
            - error (str, optional): Error message if failed

    Example:
        >>> result = search_in_file("resume.txt", "Python")
        >>> print(f"Found {result['total_matches']} matches")
    """
    # First, read the file using our read_file function
    read_result = read_file(filepath)

    # Check if file read was successful
    if not read_result["success"]:
        return {
            "success": False,
            "filepath": filepath,
            "keyword": keyword,
            "total_matches": 0,
            "matches": [],
            "error": read_result.get("error", "Unknown error reading file")
        }

    content = read_result["content"]
    keyword_lower = keyword.lower()

    # Split content into lines for line-by-line search
    lines = content.split('\n')

    matches = []

    # Search through each line
    for line_number, line_content in enumerate(lines, start=1):
        # Case-insensitive search
        if keyword_lower in line_content.lower():
            # Calculate context range (2 lines before, 2 after)
            context_start = max(0, line_number - 3)  # -3 because enumerate starts at 1
            context_end = min(len(lines), line_number + 2)

            # Extract context lines
            context_lines = lines[context_start:context_end]
            context_with_line_nums = []
            for i, ctx_line in enumerate(context_lines, start=context_start + 1):
                marker = ">>> " if i == line_number else "    "
                context_with_line_nums.append(f"{marker}{ctx_line}")

            matches.append({
                "line_number": line_number,
                "line_content": line_content.strip(),
                "context": '\n'.join(context_with_line_nums)
            })

    return {
        "success": True,
        "filepath": filepath,
        "keyword": keyword,
        "total_matches": len(matches),
        "matches": matches,
        "error": None
    }


# Tool schema definitions for LLM function calling
# These describe the tools to an LLM in a structured format
TOOL_SCHEMAS = {
    "read_file": {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file and extract its text content. Supports PDF, TXT, and DOCX formats.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file to read (e.g., 'resumes/john_doe.pdf')"
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    "list_files": {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in a directory, optionally filtered by extension",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Path to the directory to list"
                    },
                    "extension": {
                        "type": "string",
                        "description": "Optional file extension filter (e.g., '.pdf', '.txt')"
                    }
                },
                "required": ["directory"]
            }
        }
    },
    "write_file": {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file, creating directories if needed",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path where the file should be written"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["filepath", "content"]
            }
        }
    },
    "search_in_file": {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Search for a keyword in a file and return matches with surrounding context",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file to search"
                    },
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for (case-insensitive)"
                    }
                },
                "required": ["filepath", "keyword"]
            }
        }
    }
}


if __name__ == "__main__":
    # Simple test when running the module directly
    print("File System Tools Module")
    print("=" * 50)
    print("Available functions:")
    print("  - read_file(filepath)")
    print("  - list_files(directory, extension=None)")
    print("  - write_file(filepath, content)")
    print("  - search_in_file(filepath, keyword)")
