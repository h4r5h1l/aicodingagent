import os
from functions.config import CHAR_LIMIT

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, target_file_path]) != working_directory:
        return f'   Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file_path):
        return f'   Error: "File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file_path, 'r') as file:
            content = file.read()
            if len(content) > CHAR_LIMIT:
                content = content[:CHAR_LIMIT] + f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
        return content
    except Exception as e:
        return f'   Error: {str(e)}'