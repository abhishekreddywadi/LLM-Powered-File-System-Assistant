"""
Test if Ollama is running and accessible
"""
import requests
import json

def test_ollama():
    print("Testing Ollama connection...")
    print("-" * 40)

    # Test 1: Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("[OK] Ollama is running!")
            models = response.json().get("models", [])
            print(f"    Available models: {[m['name'] for m in models]}")
        else:
            print(f"[ERROR] Ollama returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Cannot connect to Ollama: {e}")
        print("\nMake sure Ollama is running:")
        print("  1. Open a new terminal")
        print("  2. Run: ollama serve")
        print("  3. Or just run: ollama run llama3")
        return False

    # Test 2: Try a simple chat
    print("\nTesting chat with llama3...")
    payload = {
        "model": "llama3",
        "messages": [{"role": "user", "content": "Say 'Hello!' in one word."}],
        "stream": False
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        print(f"[OK] LLM response: {result['message']['content']}")
        return True
    except Exception as e:
        print(f"[ERROR] Chat failed: {e}")
        return False

if __name__ == "__main__":
    if test_ollama():
        print("\n[SUCCESS] Ollama is working! You can now use:")
        print("  python llm_file_assistant.py")
        print("  (Select option 2 for Ollama mode)")
    else:
        print("\n[FAILED] Please fix Ollama first.")
