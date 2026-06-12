import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir: bool = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            raise AssertionError
        if not os.path.isdir(target_dir):
            raise ValueError

        files: list[str] = os.listdir(target_dir)
        files_metadata: list[str] = list(
            map(
                lambda f: (
                    f"- {f}: file_size={os.path.getsize(os.path.join(target_dir, f))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, f))}"
                ),
                files,
            )
        )
        return "\n".join(files_metadata)
    except ValueError:
        return f'Error: "{directory}" is not a directory'
    except AssertionError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"
