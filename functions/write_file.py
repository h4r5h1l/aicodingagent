import os

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, target_file_path]) != working_directory:
        return f'   Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(target_file_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'   Error: {str(e)}'