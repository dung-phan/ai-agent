import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_dir_path = os.path.abspath(working_directory)

        if not full_file_path.startswith(working_dir_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_file_path):
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        return write_content(full_file_path, content)
    except Exception as e:
        return f"Error: {e}"


def write_content(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the content of a file with the new content, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be added to the file"
            )
        },
        required=["file_path", "content"]
    )
)
