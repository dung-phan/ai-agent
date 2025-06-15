import os
from google.genai import types

def get_files_info(working_dir, directory=None):
    try:
        current_dir = '' if directory is None else directory
        working_dir_path = os.path.abspath(working_dir)
        merged_path = os.path.abspath(os.path.join(working_dir, current_dir))
        is_dir = os.path.isdir(merged_path)

        if not (merged_path.startswith(working_dir_path + os.sep) or merged_path == working_dir_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not is_dir:
            return f'Error: "{directory}" is not a directory'

        return generate_dir_content(merged_path)

    except Exception as e:
        return f"Error: {e}"

def generate_dir_content(path):
    files = os.listdir(path)

    def get_file_info(file):
        file_path = os.path.join(path, file)
        return f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"

    return "\n".join(list((map(get_file_info,files))))

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
            )
        }
    )
)
