import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai.client import Client
from google.genai.types import GenerateContentResponse

load_dotenv()


def main():
    api_key: str | None = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("error loading api key")

    client: Client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    args = parser.parse_args()

    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash", contents=args.user_prompt
    )
    if response.usage_metadata is None:
        raise RuntimeError("api request went wrong")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)


if __name__ == "__main__":
    main()
