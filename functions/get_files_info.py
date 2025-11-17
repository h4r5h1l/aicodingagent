import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    working_directory = os.path.abspath(working_directory)
    target_directory = os.path.abspath(os.path.join(working_directory, directory))
    if os.path.commonpath([working_directory, target_directory]) != working_directory:
        return f'   Error: Cannot list "{directory}" as it is outside the working directory'
    if os.path.isdir(target_directory) == False:
        return f'   Error: "{directory}" is not a directory'
    contents_list =  os.listdir(target_directory)
    content_string = ""
    try:
        for file in contents_list:
            file_path = os.path.join(target_directory, file)
            content_string += f'- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}\n '
    except Exception as e:
        return f'   Error: {str(e)}'
    return content_string