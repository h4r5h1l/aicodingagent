import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

def main():
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ]
        configs = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
            )
        response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=configs)
        if "--verbose" in sys.argv:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            for call in response.function_calls:
                function_call_result = call_function(call, verbose="--verbose" in sys.argv)
                if "--verbose" in sys.argv:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        print(response.text)
    else:
        print("No Prompt Found!, exiting program...")
        sys.exit(1)
if __name__ == "__main__":
    main()
