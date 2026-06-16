import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.client import Client

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()


def main():
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("error loading api key")

    client: Client = genai.Client(api_key=api_key)

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    args: argparse.Namespace = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    response: types.GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("api request went wrong")

    func_results: list[types.Part] = []
    if response.function_calls is not None:
        for fc in response.function_calls:
            func_call_result = call_function(fc)
            if (
                not func_call_result.parts
                or not isinstance(
                    func_call_result.parts[0].function_response, types.FunctionResponse
                )
                or not func_call_result.parts[0].function_response.response
            ):
                raise Exception
            func_results.append(func_call_result.parts[0])
            if args.verbose:
                print(f"-> {func_call_result.parts[0].function_response.response}")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)


if __name__ == "__main__":
    main()
