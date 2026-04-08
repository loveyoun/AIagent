import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)

    # working_directory/directory
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
    print('찾을 경로:', os.path.abspath(directory))  # 현재경로/directory

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)  # 결과 #
    except Exception as e:
        return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="작업 디렉터리 내에서 지정된 디렉터리의 파일 목록과 크기를 반환합니다.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="작업 디렉터리를 기준으로 파일을 나열할 디렉터리 경로입니다. 지정하지 않으면 작업 디렉터리 자체의 파일을 나열합니다.",
            ),
        },
    ),
)
