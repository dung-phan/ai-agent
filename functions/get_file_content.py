import os
from google.genai import types

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_dir_path = os.path.abspath(working_directory)

        if not full_file_path.startswith(working_dir_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            return read_file_content(full_file_path, file_path)
    except Exception as e:
        return f"Error: {e}"

def read_file_content(full_path, short_path):
    with open(full_path, 'r') as f:
        file_content = f.read()
        if len(file_content) > MAX_CHARS:
            return file_content[0:MAX_CHARS] + f' [...File "{short_path}" truncated at 10000 characters]'

    return file_content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file and truncates if it is more than 10000 characters long, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory"
            ),
        },
        required=["file_path"]
    )
)
