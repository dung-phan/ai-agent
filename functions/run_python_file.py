import os
import subprocess
from google.genai import types

def run_python_file(working_dir, file_path):
    try:
        working_dir_path = os.path.abspath(working_dir)
        full_file_path = os.path.abspath(os.path.join(working_dir_path, file_path))

        if not full_file_path.startswith(working_dir_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        elif not os.path.exists(full_file_path):
            return f'Error: File "{file_path}" not found.'

        elif not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        else:
            return execute_file(working_dir, full_file_path)

    except Exception as e:
            return f'Error: {e}'

def execute_file(working_dir, file):
    try:
        output = subprocess.run(
            ["python3", file],
            timeout=30,
            capture_output=True,
            cwd=working_dir,
            text=True
        )
        returned_output = []
        if output.stdout:
            returned_output.append(f"STDOUT: {output.stdout}")

        if output.stderr:
            returned_output.append(f"STDERR: {output.stderr}")

        if output.returncode != 0:
            returned_output.append(f"Process exited with code {output.returncode}")

        if not returned_output:
            return "No output produced"

        return "\n".join(returned_output)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file and returns the output, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to run the file from, relative to the working directory"
            )
        }
    )
)
