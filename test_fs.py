# test_fs.py
from fs_tools import FileSystemTools
import json  

# Create our toolbox
tools = FileSystemTools()

# Test reading a file (create a test.txt file first!)
# Create a simple text file called "test.txt" in your folder with some text

result = tools.read_file("test.txt")
print("\n📦 Final result:")
print(json.dumps(result, indent=2))