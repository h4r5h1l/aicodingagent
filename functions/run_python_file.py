import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file using the python interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The list of arguments to pass if any.",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, target_file_path]) != working_directory:
        return f'   Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file_path):
        return f'   Error: "File "{file_path}" not found.'

    if not target_file_path.endswith('.py'):
        return f'   Error: "File "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ['python', target_file_path] + args,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30
        )
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if not result.stdout.strip() and not result.stderr.strip():
            return "No output produced."
        return f"STDOUT: {result.stdout.strip()}\nSTDERR: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return f'   Error: Execution of "{file_path}" timed out'
    except Exception as e:
        return f'   Error: executing Python file: {str(e)}'