import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.client import Client

from functions.get_agent_response import get_agent_response

load_dotenv()


def main():
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("error loading api key")

    client: Client = genai.Client(api_key=api_key)

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")

    messages: list[types.Content] = []
    args: argparse.Namespace = parser.parse_args()
    messages.append(
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    )
    for _ in range(20):
        r: types.GenerateContentResponse = get_agent_response(messages, client, args)

        if r.usage_metadata is None:
            raise RuntimeError("api request went wrong")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {r.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {r.usage_metadata.candidates_token_count}")

    sys.exit("the prompt reach the maximum number of iterations")


if __name__ == "__main__":
    main()
