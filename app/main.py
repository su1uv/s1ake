import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.client import Client

from ui.bootgent import Bootgent

load_dotenv()


def main():
    messages: list[types.Content] = []

    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("error loading api key")

    client: Client = genai.Client(api_key=api_key)

    Bootgent(messages, client).run()


if __name__ == "__main__":
    main()
