import os
import subprocess
from subprocess import CompletedProcess
from sys import stdout


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not os.path.isfile(target_file):
            raise ValueError(f'"{file_path}" does not exist or is not a regular file')
        if not valid_target_dir:
            raise ValueError(
                f'Cannot execute "{file_path}" as it is outside the permitted working directory'
            )
        if not target_file.endswith(".py"):
            raise ValueError(f'"{file_path}" is not a Python file')

        command: list[str] = ["python", target_file]
        if args:
            command.extend(args)

        r: CompletedProcess = subprocess.run(
            command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs
        )

        output: str = (
            f"Process exited with code: {r.returncode}"
            if r.returncode != 0
            else "" + "\n No output produced"
            if not r.stderr and not r.stdout
            else f"\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
        )

        return output

    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
