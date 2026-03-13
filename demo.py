"""
demo.py - Quick demonstration of the LLM File Assistant
Shows all features without requiring interactive input.
"""

from llm_file_assistant import LLMFileAssistant

def main():
    print("=" * 60)
    print("   LLM FILE ASSISTANT - DEMO")
    print("=" * 60)

    # Create assistant (mock mode, no LLM needed)
    assistant = LLMFileAssistant(use_ollama=False)

    # Demo 1: List files
    print("\n[DEMO 1] Listing files in sample_resumes:")
    print("-" * 40)
    response = assistant.process_query("List all files in sample_resumes")
    print(response)

    # Demo 2: Read a file
    print("\n[DEMO 2] Reading alice_frontend.txt:")
    print("-" * 40)
    response = assistant.process_query("Read alice_frontend.txt")
    print(response)

    # Demo 3: Search for a skill
    print("\n[DEMO 3] Searching for 'frontend' skills:")
    print("-" * 40)
    response = assistant.process_query("Find frontend developers")
    print(response)

    # Demo 4: Search for Python
    print("\n[DEMO 4] Searching for 'python' skills:")
    print("-" * 40)
    response = assistant.process_query("Find python skills in sample_resumes")
    print(response)

    # Demo 5: Direct tool execution
    print("\n[DEMO 5] Direct tool execution:")
    print("-" * 40)
    result = assistant.execute_tool("list_files", {"directory": "test_resumes"})
    print(f"Files in test_resumes: {len(result)}")

    print("\n" + "=" * 60)
    print("   DEMO COMPLETE!")
    print("=" * 60)
    print("\nTo run interactively:")
    print("  python llm_file_assistant.py")

if __name__ == "__main__":
    main()
