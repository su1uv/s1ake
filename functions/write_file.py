import os

from google.genai import types


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir: bool = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            raise AssertionError
        if not os.path.isdir(os.path.dirname(target_dir)):
            raise FileNotFoundError

        os.makedirs(os.path.dirname(target_dir), exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except AssertionError:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except FileNotFoundError:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Return a success message with the edited file name and the number of characters written of the file edited",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path file to write, relative to the working directory (it does not have a default value)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Value to write on the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
