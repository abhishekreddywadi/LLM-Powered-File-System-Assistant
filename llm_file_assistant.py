"""
llm_file_assistant.py - LLM Integration with Function Calling
=============================================================================
This module integrates file system tools with multiple LLM options.

Part B: LLM Integration (40%)

AVAILABLE OPTIONS:
1. Mock Mode (Default) - Uses pattern matching, no LLM needed
2. OpenRouter - Cloud API with multiple free models (requires API key)

Installation:
- OpenRouter: pip install requests
"""

import json
import os
import re
import requests
from typing import Dict, List, Optional, Callable, Union

# Import file system tools
from fs_tools import (
    read_file,
    list_files,
    write_file,
    search_in_file,
    TOOL_SCHEMAS
)


class LLMFileAssistant:
    """
    An AI assistant that uses LLMs with function calling for file operations.

    This class works with:
    1. Mock mode (default) - Pattern matching, no dependencies
    2. OpenRouter - Cloud API with multiple free models (requires API key)

    Example:
        >>> # Use mock mode (no LLM needed)
        >>> assistant = LLMFileAssistant(use_openrouter=False)
        >>> response = assistant.process_query("List all PDF files")

        >>> # Use OpenRouter
        >>> assistant = LLMFileAssistant(use_openrouter=True, api_key="your-api-key")
        >>> response = assistant.process_query("Find Python developers")
    """

    def __init__(self, use_openrouter: bool = False, api_key: Optional[str] = None, model: str = "openai/gpt-4o-mini"):
        """
        Initialize the LLM File Assistant with OpenRouter support.

        Args:
            use_openrouter (bool): If True, uses OpenRouter API.
                                 If False, uses pattern matching (no dependencies).
            api_key (str): OpenRouter API key. If None, tries to get from
                          OPENROUTER_API_KEY environment variable.
            model (str): OpenRouter model name (default: "google/gemma-3-27b-it:free").
                        Other free options: "google/gemma-2-9b-it:free", "mistralai/mistral-7b-instruct:free"

        To get OpenRouter API key:
        1. Go to https://openrouter.ai/keys
        2. Sign up and get your API key

        To set API key:
        export OPENROUTER_API_KEY="sk-or-v1-<Secret Key>"
        """
        # Map tool names to actual Python functions
        self.available_tools: Dict[str, Callable] = {
            "read_file": read_file,
            "list_files": list_files,
            "write_file": write_file,
            "search_in_file": search_in_file
        }

        # Get tool schemas for LLM function calling
        self.tool_schemas = list(TOOL_SCHEMAS.values())

        # LLM configuration
        self.use_openrouter = use_openrouter
        self.model = model
        self.openrouter_api_key = None
        self.openrouter_base_url = "https://openrouter.ai/api/v1"

        # Get API key from parameter or environment variable
        if api_key is None:
            api_key = os.environ.get("OPENROUTER_API_KEY")

        if use_openrouter:
            if not api_key:
                print("[WARN] No OpenRouter API key provided.")
                print("   Set OPENROUTER_API_KEY environment variable or pass api_key parameter.")
                print("   Falling back to mock mode.")
                self.use_openrouter = False
            else:
                self.openrouter_api_key = api_key
                print(f"[OK] Connected to OpenRouter (model: {model})")

        # Conversation history for OpenRouter
        self.conversation_history: List[Dict] = []

    def process_query(self, user_query: str) -> str:
        """
        Process a user query using LLM with function calling.

        Args:
            user_query (str): The user's natural language query

        Returns:
            str: The assistant's response
        """
        # Choose processing method
        if self.use_openrouter:
            response = self._process_with_openrouter(user_query)
        else:
            response = self._process_with_mock_llm(user_query)

        return response

    def _process_with_openrouter(self, user_query: str) -> str:
        """
        Process query using OpenRouter API with function calling.

        Uses the standard /chat/completions endpoint (OpenAI-compatible).
        """
        # Define tools in OpenAI function format
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read and extract text from PDF, TXT, or DOCX files",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Path to the file to read"
                            }
                        },
                        "required": ["filepath"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List files in a directory, optionally filtered by extension",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directory path to list files from"
                            },
                            "extension": {
                                "type": "string",
                                "description": "Optional file extension filter (e.g., .pdf, .txt)"
                            }
                        },
                        "required": ["directory"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_in_file",
                    "description": "Search for a keyword in a file with context",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Path to the file to search"
                            },
                            "keyword": {
                                "type": "string",
                                "description": "Keyword to search for"
                            }
                        },
                        "required": ["filepath", "keyword"]
                    }
                }
            }
        ]

        # System message
        system_message = {
            "role": "system",
            "content": """You are a helpful File Assistant with access to file system tools.

CRITICAL RULES:
1. You MUST use tools for ALL file operations - NEVER make up file names or content
2. ALWAYS call list_files() before claiming any files exist in a directory
3. ALWAYS call read_file() or search_in_file() to get actual data from files
4. NEVER invent information - only use data from actual tool results
5. When asked about file contents, you MUST read the files first

Always use tools to get real data. Never hallucinate fake files or content."""
        }

        try:
            # Build messages with history
            messages = [system_message]
            for msg in self.conversation_history:
                messages.append({"role": msg["role"], "content": msg["content"]})

            # Add current user query
            messages.append({"role": "user", "content": user_query})

            # Make API call to OpenRouter
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://llm-file-assistant.local",
                "X-OpenRouter-Title": "LLM File Assistant"
            }

            payload = {
                "model": self.model,
                "messages": messages,
                "tools": tools
            }

            response = requests.post(
                f"{self.openrouter_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            # Debug: print response for troubleshooting
            print(f"[DEBUG] Status: {response.status_code}")
            if response.status_code != 200:
                print(f"[DEBUG] Response: {response.text[:500]}")
                return f"OpenRouter API error ({response.status_code}): {response.text[:200]}"

            response_data = response.json()

            # Debug: print response structure
            print(f"[DEBUG] Response keys: {list(response_data.keys())}")

            # Check if the model wants to call tools
            if "choices" not in response_data or len(response_data["choices"]) == 0:
                return "No choices in response"

            assistant_message = response_data["choices"][0]["message"]

            # Debug: check for tool calls
            if "tool_calls" in assistant_message:
                print(f"[DEBUG] Tool calls found: {len(assistant_message['tool_calls'])}")

            # Handle tool calls
            if "tool_calls" in assistant_message and assistant_message["tool_calls"]:
                tool_calls = assistant_message["tool_calls"]

                # Execute all tool calls
                tool_responses = []
                for tool_call in tool_calls:
                    function_name = tool_call["function"]["name"]
                    function_args = json.loads(tool_call["function"]["arguments"])

                    print(f"[DEBUG] Calling tool: {function_name} with args: {function_args}")

                    # Execute the tool
                    result = self.execute_tool(function_name, function_args)

                    tool_responses.append({
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "content": json.dumps(result, default=str)
                    })

                # Add assistant message and tool responses to conversation
                messages.append(assistant_message)
                messages.extend(tool_responses)

                # Make follow-up call with tool results
                follow_up_payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 2000  # Allow longer responses
                }

                follow_up_response = requests.post(
                    f"{self.openrouter_base_url}/chat/completions",
                    headers=headers,
                    json=follow_up_payload,
                    timeout=60
                )

                if follow_up_response.status_code != 200:
                    return f"OpenRouter API error in follow-up ({follow_up_response.status_code}): {follow_up_response.text[:200]}"

                follow_up_data = follow_up_response.json()
                final_response_text = follow_up_data["choices"][0]["message"]["content"]

                # Update conversation history
                self.conversation_history.append({"role": "user", "content": user_query})
                self.conversation_history.append({"role": "assistant", "content": final_response_text})

                return final_response_text
            else:
                # No tool calls, just return the response
                response_text = assistant_message.get("content", "")
                print(f"[DEBUG] No tool calls, response: {response_text[:100]}")

                # Update conversation history
                self.conversation_history.append({"role": "user", "content": user_query})
                self.conversation_history.append({"role": "assistant", "content": response_text})

                return response_text

        except requests.exceptions.Timeout:
            return "Error: OpenRouter API request timed out."
        except requests.exceptions.RequestException as e:
            return f"Error calling OpenRouter API: {str(e)}"
        except Exception as e:
            import traceback
            return f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"

    def _call_ollama(self, messages: List[Dict], tools_description: str = "") -> str:
        """Make API call to local Ollama server."""
        # Add tools description to system message if provided
        if tools_description:
            messages[0]["content"] += f"\n\n{tools_description}"

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/chat",
                json=payload,
                timeout=1220  # Increased timeout for slower computers
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        except requests.exceptions.Timeout:
            return "Error: Ollama took too long to respond. Try a smaller model like 'phi3' or 'tinyllama'."
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure 'ollama serve' is running in another terminal."
        except Exception as e:
            return f"Error calling Ollama: {str(e)}"

    def _format_tools_for_llm(self) -> str:
        """
        Format tool schemas for LLM understanding.

        Returns a concise string that reinforces the JSON-only output format.
        """
        return """
IMPORTANT: When calling a tool, respond with ONLY valid JSON like:
{"tool": "read_file", "parameters": {"filepath": "sample_resumes/file.txt"}}
No extra text, no explanations - just the JSON.
"""

    def _extract_tool_calls(self, response: str) -> List[Dict]:
        """
        Extract tool calls from LLM response with flexible pattern matching.

        This method handles variations in JSON formatting:
        - Different whitespace patterns (spaces, tabs, newlines)
        - Single quotes instead of double quotes
        - Different key orders in the JSON object
        - Missing optional parameters

        Args:
            response (str): The LLM response text that may contain tool calls

        Returns:
            List[Dict]: List of extracted tool calls with 'tool' and 'parameters' keys
        """
        tool_calls = []

        # First, check for TOOL_CALL: prefix format (most explicit)
        tool_call_match = re.search(r'TOOL_CALL:\s*(\{.*\})', response, re.DOTALL)
        if tool_call_match:
            try:
                json_str = tool_call_match.group(1)
                tool_call = json.loads(json_str)
                if isinstance(tool_call, dict) and "tool" in tool_call and "parameters" in tool_call:
                    tool_calls.append(tool_call)
                    return tool_calls  # Return early if we found explicit format
            except json.JSONDecodeError:
                pass  # Fall through to other patterns

        # Pattern 1: Standard double-quoted JSON with flexible whitespace
        # Matches: {"tool": "read_file", "parameters": {"filepath": "test.txt"}}
        json_pattern_double = r'\{\s*"tool"\s*:\s*"(\w+)"\s*,\s*"parameters"\s*:\s*\{[^\}]*\}\s*\}'

        # Pattern 2: Single-quoted JSON (some models output this)
        # Matches: {'tool': 'read_file', 'parameters': {'filepath': 'test.txt'}}
        json_pattern_single = r"\{\s*'tool'\s*:\s*'(\w+)'\s*,\s*'parameters'\s*:\s*\{[^\}]*\}\s*\}"

        # Pattern 3: JSON with newlines (multi-line format)
        # Matches multi-line tool calls that span multiple lines
        json_pattern_multiline = r'\{\s*"tool"\s*:\s*"(\w+)"\s*,\s*"parameters"\s*:\s*\{[^\}]*\}\s*\}'

        # Try all patterns to extract tool calls
        all_patterns = [json_pattern_double, json_pattern_single, json_pattern_multiline]

        for pattern in all_patterns:
            matches = re.finditer(pattern, response, re.MULTILINE | re.DOTALL)

            for match in matches:
                try:
                    json_str = match.group(0)

                    # Normalize quotes: convert single quotes to double quotes for JSON parsing
                    json_str_normalized = json_str.replace("'", '"')

                    # Parse the JSON to get the tool call
                    tool_call = json.loads(json_str_normalized)

                    # Validate the tool call has required fields
                    if isinstance(tool_call, dict) and "tool" in tool_call and "parameters" in tool_call:
                        tool_calls.append(tool_call)
                except (json.JSONDecodeError, ValueError):
                    # If parsing fails, try to extract using a more lenient approach
                    try:
                        # Fallback: Extract tool name and parameters manually
                        tool_match = re.search(r'"tool"\s*:\s*"(\w+)"', match.group(0))
                        if tool_match:
                            tool_name = tool_match.group(1)
                            # Extract the parameters section
                            params_match = re.search(r'"parameters"\s*:\s*(\{[^\}]*\})', match.group(0), re.DOTALL)
                            if params_match:
                                parameters = json.loads(params_match.group(1).replace("'", '"'))
                                tool_calls.append({"tool": tool_name, "parameters": parameters})
                    except Exception:
                        continue

        return tool_calls

    def _clean_response(self, response: str) -> str:
        """
        Clean up LLM response by removing tool call JSON.

        This removes both double-quoted and single-quoted tool call patterns
        to give the user a clean text response.

        Args:
            response (str): Raw LLM response that may contain tool calls

        Returns:
            str: Cleaned response with tool calls removed
        """
        # Remove TOOL_CALL: prefix format first
        cleaned = re.sub(r'TOOL_CALL:\s*\{.*?\}', '', response, flags=re.DOTALL)
        # Remove double-quoted JSON tool calls
        cleaned = re.sub(r'\{\s*"tool"\s*:\s*"\w+"\s*,\s*"parameters"\s*:\s*\{[^}]*\}\s*\}', '', cleaned)

        # Remove single-quoted JSON tool calls (some models output this)
        cleaned = re.sub(r"\{\s*'tool'\s*:\s*'\w+'\s*,\s*'parameters'\s*:\s*\{[^\}]*\}\s*\}", '', cleaned)

        # Remove multi-line tool call patterns
        cleaned = re.sub(r'\{\s*"tool"\s*:\s*"\w+"\s*,\s*"parameters"\s*:\s*\{[^\}]*\}\s*\}', '', cleaned, flags=re.MULTILINE | re.DOTALL)

        return cleaned.strip()

    def _process_with_mock_llm(self, user_query: str) -> str:
        """
        Process query using pattern matching (Mock LLM).
        This simulates LLM function calling without requiring any LLM.
        """
        query_lower = user_query.lower()

        # ============= PATTERN 1: LIST FILES =============
        if any(word in query_lower for word in ["list", "show files", "what files"]):
            directory = self._extract_directory(user_query) or "sample_resumes"
            extension = self._extract_extension(user_query)

            result = list_files(directory=directory, extension=extension)

            if result and "error" in result[0]:
                return f"[ERROR] {result[0]['error']}"

            response = f"[DIR] Found {len(result)} files in '{directory}':\n\n"
            for file_info in result:
                response += f"  - {file_info['name']} ({file_info['size']}) - Modified: {file_info['modified_date']}\n"
            return response

        # ============= PATTERN 2: READ FILE =============
        elif any(word in query_lower for word in ["read", "show content", "open", "display"]):
            filepath = self._extract_filepath(user_query)
            if filepath:
                result = read_file(filepath)

                if result["success"]:
                    response = f"[FILE] File: {result['metadata']['name']}\n"
                    response += f"[SIZE] Size: {result['metadata']['size_human']}\n"
                    response += f"[DATE] Modified: {result['metadata']['modified_date']}\n\n"
                    response += "[CONTENT] Content:\n" + "-" * 50 + "\n"
                    response += result["content"]
                    return response
                else:
                    return f"[ERROR] {result['error']}"
            else:
                return "[INFO] Please specify which file to read (e.g., 'read alice_frontend.txt')"

        # ============= PATTERN 3: SEARCH =============
        elif any(word in query_lower for word in ["search", "find", "look for", "contains"]):
            keyword = self._extract_search_keyword(user_query)
            directory = self._extract_directory(user_query) or "sample_resumes"

            if keyword:
                files = list_files(directory)
                if "error" in files[0]:
                    return f"[ERROR] {files[0]['error']}"

                all_matches = []
                for file_info in files:
                    filepath = f"{directory}/{file_info['name']}"
                    result = search_in_file(filepath, keyword)
                    if result["success"] and result["total_matches"] > 0:
                        all_matches.append({
                            "file": file_info['name'],
                            "matches": result["matches"],
                            "total": result["total_matches"]
                        })

                if not all_matches:
                    return f"[SEARCH] No matches found for '{keyword}' in '{directory}'"

                response = f"[SEARCH] Found '{keyword}' in {len(all_matches)} file(s):\n\n"
                for match in all_matches:
                    response += f"[FILE] {match['file']} ({match['total']} match(es))\n"
                    for m in match['matches'][:2]:  # Show first 2 matches
                        response += f"   Line {m['line_number']}: {m['line_content'][:70]}...\n"
                    response += "\n"
                return response
            else:
                return "[SEARCH] What keyword would you like me to search for?"

        # ============= PATTERN 4: WRITE FILE =============
        elif any(word in query_lower for word in ["write", "save", "create file"]):
            filepath = self._extract_filepath(user_query) or "output.txt"
            content = f"Summary generated by LLM File Assistant on {self._get_timestamp()}"
            result = write_file(filepath, content)

            if result["success"]:
                return f"[OK] {result['message']}"
            else:
                return f"[ERROR] {result['error']}"

        # ============= PATTERN 5: HELP =============
        elif "help" in query_lower:
            return self._get_help_message()

        # Default: unrecognized query
        return self._get_help_message()

    def _extract_directory(self, query: str) -> Optional[str]:
        """Extract directory name from user query."""
        query_lower = query.lower()
        if "sample" in query_lower:
            return "sample_resumes"
        elif "test" in query_lower:
            return "test_resumes"
        elif "resume" in query_lower:
            return "sample_resumes"
        return None

    def _extract_extension(self, query: str) -> Optional[str]:
        """Extract file extension from user query."""
        for ext in [".pdf", ".txt", ".docx"]:
            if ext in query.lower():
                return ext
        return None

    def _extract_filepath(self, query: str) -> Optional[str]:
        """Extract file path from user query."""
        # Look for filename patterns
        match = re.search(r'([\w_\-]+\.(txt|pdf|docx))', query.lower())
        if match:
            filename = match.group(1)
            directory = self._extract_directory(query) or "sample_resumes"
            return f"{directory}/{filename}"
        return None

    def _extract_search_keyword(self, query: str) -> Optional[str]:
        """Extract search keyword from user query."""
        # Common tech keywords
        keywords = ["python", "javascript", "java", "react", "aws", "sql", "docker",
                    "frontend", "backend", "full", "stack", "data", "developer",
                    "engineer", "analyst", "llm", "machine learning"]

        query_lower = query.lower()
        for keyword in keywords:
            if keyword in query_lower:
                return keyword

        # Try to find keyword after "search for" or "find"
        match = re.search(r'(?:search for|find|look for|containing)\s+(\w+)', query_lower)
        if match:
            return match.group(1)

        return None

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _get_help_message(self) -> str:
        """Return help message with available commands."""
        return """
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

[WRITE] WRITE FILES:
   - "Write a summary to output.txt"

[INFO] USAGE MODES:
   - Mock Mode (default): Pattern matching, no LLM needed
   - OpenRouter Mode: Cloud API with multiple free models
     Get API key: https://openrouter.ai/keys
     API Key: Set OPENROUTER_API_KEY environment variable

Type 'exit' to quit.
"""

    def execute_tool(self, tool_name: str, parameters: Dict) -> Dict:
        """
        Execute a tool directly with given parameters.

        Example:
            >>> result = assistant.execute_tool("read_file", {"filepath": "test.txt"})
        """
        if tool_name not in self.available_tools:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        try:
            return self.available_tools[tool_name](**parameters)
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def get_conversation_history(self) -> List[Dict]:
        """Get the current conversation history."""
        return self.conversation_history.copy()


def main():
    """Main function to run the LLM File Assistant interactively."""
    print("=" * 60)
    print("[AI] LLM File Assistant - OpenRouter Edition")
    print("=" * 60)

    # Get API key
    api_key = os.environ.get("OPENROUTER_API_KEY", "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")

    if not api_key or api_key.startswith("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"):
        print("\n[INFO] Using your OpenRouter API key")

    # Create assistant with OpenRouter
    assistant = LLMFileAssistant(use_openrouter=True, api_key=api_key, model="openai/gpt-4o-mini")

    print(assistant._get_help_message())

    # Main interaction loop
    while True:
        try:
            user_input = input("\n[USER] You: ").strip()

            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                print("\n[BYE] Goodbye!")
                break

            if not user_input:
                continue

            response = assistant.process_query(user_input)
            print(f"\n[AI] Assistant:\n{response}")

        except KeyboardInterrupt:
            print("\n\n[BYE] Goodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] Error: {str(e)}")


if __name__ == "__main__":
    main()
