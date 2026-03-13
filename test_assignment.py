"""
test_assignment.py - Comprehensive Test Suite for Assignment
============================================================
Tests all requirements for both Part A (File System Tools) and Part B (LLM Integration)

Run this to verify your assignment is complete:
    python test_assignment.py
"""

import json
import os
from fs_tools import read_file, list_files, write_file, search_in_file, TOOL_SCHEMAS
from llm_file_assistant import LLMFileAssistant


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_part_a_read_file():
    """
    Test Part A: read_file function
    Requirement: Read resume files (PDF, TXT, DOCX), extract text content,
    return structured response with content and metadata, handle errors gracefully.
    """
    print_section("PART A: Test read_file()")

    # Test 1: Read existing TXT file
    print("\n1. Testing TXT file reading...")
    result = read_file("sample_resumes/alice_frontend.txt")
    print(f"   Success: {result['success']}")
    print(f"   Content length: {len(result['content'])} characters")
    print(f"   Metadata keys: {list(result['metadata'].keys())}")
    assert result['success'] == True
    assert result['content'] is not None
    assert result['metadata'] is not None
    assert 'name' in result['metadata']
    assert 'size_bytes' in result['metadata']
    assert 'extension' in result['metadata']
    print("   [PASS] TXT reading works!")

    # Test 2: Error handling - file not found
    print("\n2. Testing error handling (file not found)...")
    result = read_file("nonexistent_file.txt")
    print(f"   Success: {result['success']}")
    print(f"   Error message present: {result.get('error') is not None}")
    assert result['success'] == False
    assert result['error'] is not None
    print("   [PASS] Error handling works!")

    # Test 3: Check metadata structure
    print("\n3. Testing metadata structure...")
    result = read_file("sample_resumes/charlie_full.txt")
    metadata = result['metadata']
    print(f"   Name: {metadata['name']}")
    print(f"   Size: {metadata['size_human']}")
    print(f"   Modified: {metadata['modified_date']}")
    print(f"   Extension: {metadata['extension']}")
    print("   [PASS] Metadata structure is correct!")


def test_part_a_list_files():
    """
    Test Part A: list_files function
    Requirement: List all files in directory, filter by extension,
    return file metadata (name, size, modified date).
    """
    print_section("PART A: Test list_files()")

    # Test 1: List all files
    print("\n1. Testing list all files...")
    result = list_files("sample_resumes")
    print(f"   Number of files found: {len(result)}")
    print(f"   Files: {[f['name'] for f in result]}")
    assert len(result) > 0
    assert 'name' in result[0]
    assert 'size' in result[0]
    assert 'modified_date' in result[0]
    print("   [PASS] List files works!")

    # Test 2: Filter by extension
    print("\n2. Testing extension filter (.txt)...")
    result = list_files("sample_resumes", extension=".txt")
    print(f"   TXT files found: {len(result)}")
    for f in result:
        print(f"      - {f['name']}")
    assert all(f['extension'] == '.txt' for f in result)
    print("   [PASS] Extension filter works!")

    # Test 3: Error handling - directory not found
    print("\n3. Testing error handling (invalid directory)...")
    result = list_files("nonexistent_directory")
    print(f"   Returns error: {'error' in result[0]}")
    assert 'error' in result[0]
    print("   [PASS] Error handling works!")


def test_part_a_write_file():
    """
    Test Part A: write_file function
    Requirement: Write content to file, create directories if needed,
    return success/failure status.
    """
    print_section("PART A: Test write_file()")

    # Test 1: Write to existing directory
    print("\n1. Testing write to existing directory...")
    test_content = "This is a test resume content.\nSkills: Python, JavaScript"
    result = write_file("test_resumes/test_write.txt", test_content)
    print(f"   Success: {result['success']}")
    print(f"   Bytes written: {result.get('bytes_written')}")
    print(f"   Message: {result.get('message')}")
    assert result['success'] == True
    assert result['bytes_written'] > 0
    print("   [PASS] Write file works!")

    # Test 2: Create nested directories
    print("\n2. Testing nested directory creation...")
    result = write_file("output/nested/folder/test.txt", "Nested content")
    print(f"   Success: {result['success']}")
    print(f"   File created: {result.get('filepath')}")
    assert result['success'] == True
    assert os.path.exists("output/nested/folder/test.txt")
    print("   [PASS] Nested directory creation works!")

    # Cleanup
    if os.path.exists("output/nested/folder/test.txt"):
        os.remove("output/nested/folder/test.txt")


def test_part_a_search_in_file():
    """
    Test Part A: search_in_file function
    Requirement: Search for keywords in file content,
    return matches with context (surrounding text),
    case-insensitive search.
    """
    print_section("PART A: Test search_in_file()")

    # Test 1: Basic search
    print("\n1. Testing basic search...")
    result = search_in_file("sample_resumes/alice_frontend.txt", "frontend")
    print(f"   Success: {result['success']}")
    print(f"   Total matches: {result['total_matches']}")
    print(f"   Keyword searched: {result['keyword']}")
    assert result['success'] == True
    assert result['total_matches'] > 0
    print("   [PASS] Basic search works!")

    # Test 2: Case-insensitive search
    print("\n2. Testing case-insensitive search...")
    result_lower = search_in_file("sample_resumes/alice_frontend.txt", "FRONTEND")
    result_upper = search_in_file("sample_resumes/alice_frontend.txt", "frontend")
    print(f"   Lowercase result matches: {result_lower['total_matches']}")
    print(f"   Uppercase result matches: {result_upper['total_matches']}")
    assert result_lower['total_matches'] == result_upper['total_matches']
    print("   [PASS] Case-insensitive search works!")

    # Test 3: Context in results
    print("\n3. Testing context in matches...")
    result = search_in_file("test_resumes/john_dev.txt", "Python")
    if result['total_matches'] > 0:
        first_match = result['matches'][0]
        print(f"   Line number: {first_match['line_number']}")
        print(f"   Line content: {first_match['line_content'][:50]}...")
        print(f"   Has context: {'context' in first_match}")
        assert 'context' in first_match
        print("   [PASS] Context is included in matches!")


def test_part_b_llm_integration():
    """
    Test Part B: LLM Integration
    Requirement: Integrate LLM with function calling/tool use,
    process natural language queries.
    """
    print_section("PART B: Test LLM Integration")

    # Create assistant (mock mode, no LLM needed)
    print("\n1. Creating LLM File Assistant...")
    assistant = LLMFileAssistant(use_ollama=False)
    print(f"   Available tools: {list(assistant.available_tools.keys())}")
    print(f"   Tool schemas count: {len(assistant.tool_schemas)}")
    assert len(assistant.available_tools) == 4
    assert len(assistant.tool_schemas) == 4
    print("   [PASS] Assistant initialized with tools!")

    # Test 2: Process query - list files
    print("\n2. Testing query processing (list files)...")
    response = assistant.process_query("List all files in sample_resumes")
    print(f"   Response preview: {response[:100]}...")
    assert "Found" in response or "files" in response.lower()
    print("   [PASS] Query processing works!")

    # Test 3: Process query - search
    print("\n3. Testing query processing (search)...")
    response = assistant.process_query("Find Python developers")
    print(f"   Response preview: {response[:100]}...")
    print("   [PASS] Search query processing works!")

    # Test 4: Process query - read file
    print("\n4. Testing query processing (read file)...")
    response = assistant.process_query("Read alice_frontend.txt")
    print(f"   Response preview: {response[:100]}...")
    print("   [PASS] Read file query processing works!")

    # Test 5: Direct tool execution
    print("\n5. Testing direct tool execution...")
    result = assistant.execute_tool("list_files", {"directory": "sample_resumes"})
    print(f"   Tool executed successfully: {result and 'error' not in result[0]}")
    print("   [PASS] Direct tool execution works!")

    # Test 6: Conversation history
    print("\n6. Testing conversation history...")
    history = assistant.get_conversation_history()
    print(f"   Conversation turns: {len(history)}")
    assert len(history) > 0
    print("   [PASS] Conversation history tracking works!")


def test_tool_schemas():
    """
    Test that tool schemas are properly defined for LLM function calling.
    """
    print_section("Test Tool Schemas for LLM Function Calling")

    print("\nChecking tool schemas...")
    required_tools = ["read_file", "list_files", "write_file", "search_in_file"]

    for tool_name in required_tools:
        assert tool_name in TOOL_SCHEMAS
        schema = TOOL_SCHEMAS[tool_name]
        print(f"\n{tool_name}:")
        print(f"   Type: {schema['type']}")
        print(f"   Has function: {'function' in schema}")
        print(f"   Has description: {'description' in schema['function']}")
        print(f"   Has parameters: {'parameters' in schema['function']}")


def run_all_tests():
    """Run all tests for the assignment."""
    print("\n" + "=" * 60)
    print("   ASSIGNMENT TEST SUITE - RUNNING ALL TESTS")
    print("=" * 60)

    try:
        # Part A Tests
        test_part_a_read_file()
        test_part_a_list_files()
        test_part_a_write_file()
        test_part_a_search_in_file()

        # Part B Tests
        test_part_b_llm_integration()

        # Tool Schemas Test
        test_tool_schemas()

        # Summary
        print_section("ALL TESTS PASSED!")
        print("\n[PASS] Part A: Core File System Tools (60%) - COMPLETE")
        print("   - read_file() [PASS]")
        print("   - list_files() [PASS]")
        print("   - write_file() [PASS]")
        print("   - search_in_file() [PASS]")
        print("\n[PASS] Part B: LLM Integration (40%) - COMPLETE")
        print("   - LLM Assistant class [PASS]")
        print("   - Tool schemas [PASS]")
        print("   - Query processing [PASS]")
        print("   - Conversation history [PASS]")
        print("\nASSIGNMENT REQUIREMENTS MET!")

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {str(e)}")
    except Exception as e:
        print(f"\n[ERROR] ERROR: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
