import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function, available_functions
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


# for model in client.models.list():
#     print(model.name)

def main():
    verbose_flag = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    # parser = argparse.ArgumentParser(description="Gemini Agent Loop")
    # # --verbose 옵션 설정
    # parser.add_argument(
    #     '--verbose',
    #     action='store_true',  # --verbose True x
    #     help='디버깅을 위한 상세 로그를 출력합니다.'
    # )
    # args = parser.parse_args()  # args.verbose == True or False

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        return
        # sys.exit(1)
    user_prompt = " ".join(args)

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    generate_content_loop(client, messages, config, verbose_flag)


def generate_content_loop(client, messages, config, verbose_flag, max_iterations=20):
    for iteration in range(max_iterations):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config,
        )

        # 1. 모델의 응답(Assistant 역할)을 히스토리에 추가
        # response.candidates[0].content에는 'model' role이 이미 포함되어 있음
        messages.append(response.candidates[0].content)
        if verbose_flag:
            print(
                f"- Iteration {iteration + 1} "
                f"- Prompt: {response.usage_metadata.prompt_token_count} "
                f"- Resp: {response.usage_metadata.candidates_token_count}")

        # 2. Final agent text message
        # 텍스트 응답이 있으면 종료 (도구 호출과 동시에 텍스트가 올 수도 있으나 보통은 분리됨)
        if response.candidates[0].content.parts and not response.function_calls:
            print("✨ 드디어 최종 답변입니다!")
            print(response.text)
            return

        # 3. 함수 호출 처리
        if response.function_calls:
            if verbose_flag:
                print(f"AI Thinking...: {response.text}")

            tool_parts = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose_flag)
                tool_parts.append(function_call_result.parts[0])

            # 루프가 끝난 뒤, Part들을 하나의 Content(role="tool")로 묶어서 추가합니다.
            messages.append(types.Content(role="tool", parts=tool_parts))
            #     print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    else:  # After all for-iterations
        print(f"최대 반복 횟수({max_iterations})에 도달했습니다. 에이전트가 작업을 완료하지 못했을 수 있습니다.")


if __name__ == "__main__":
    main()
