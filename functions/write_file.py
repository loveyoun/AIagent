import os
from pathlib import Path
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(abs_file_path):  # 경로 존재 확인 + 디렉토리인가?
        return f'Error: "{file_path}" is a directory, not a file'

    try:  # 부모 dir 만들기
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    except Exception as e:
        return f"Error: creating directory: {e}"

    try:  # create a new file or
        with open(abs_file_path, "w") as f:  # "a", encoding="utf-8"
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to file: {file_path} {e}"


def write_file_v2(working_directory, file_path, content):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    path = Path(abs_file_path)

    # 1. 부모 디렉토리 생성
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return f"Error: creating directory: {e}"

    # 2. 디렉토리인지 확인
    if path.is_dir():
        return f'Error: "{path.name}" is a directory, not a file'
    return "Success!"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="작업 디렉토리 내의 파일에 내용을 씁니다. 파일이 존재하지 않으면 생성합니다.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="작업 디렉토리에 상대적인, 쓸 파일의 경로.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="파일에 쓸 내용",
            ),
        },
        required=["file_path", "content"],
    ),
)