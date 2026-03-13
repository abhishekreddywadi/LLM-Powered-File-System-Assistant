# test_free_assistant.py
from llm_file_assistant_free import FreeLLMFileAssistant

print("Testing FREE LLM Assistant (No API Key!)")
print("-" * 40)

# Create assistant (downloads model first time)
assistant = FreeLLMFileAssistant()

# Test simple queries
test_queries = [
    "Hello, what can you do?",
    "List all files in sample_resumes folder",
    "Read a resume file"
]

for query in test_queries:
    print(f"\n📝 Query: {query}")
    response = assistant.process_query(query)
    print(f"🤖 Response: {response}")
    print("-" * 40)