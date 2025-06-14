import os

MAX_CHARS = 10000

def get_file_content(working_dir, file_path):
    try:
        full_file_path = os.path.abspath(os.path.join(working_dir, file_path))
        working_dir_path = os.path.abspath(working_dir)

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
