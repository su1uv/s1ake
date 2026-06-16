import os

from google.genai import types


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir: bool = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not os.path.isdir(target_dir):
            raise ValueError
        if not valid_target_dir:
            raise AssertionError

        files: list[str] = os.listdir(target_dir)
        files_info: list[str] = list(
            map(
                lambda f: (
                    f"- {f}: file_size={os.path.getsize(os.path.join(target_dir, f))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, f))}"
                ),
                files,
            )
        )
        return "\n".join(files_info)
    except ValueError:
        return f'Error: "{directory}" is not a directory'
    except AssertionError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
