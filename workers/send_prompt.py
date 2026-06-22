from google.genai import Client, types

from functions.get_agent_response import get_agent_response


async def send_prompt(
    user_prompt: str,
    messages: list[types.Content],
    client: Client,
    metadata: dict[str, int],
) -> str:
    messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

    for _ in range(20):
        r: types.GenerateContentResponse | str = await get_agent_response(
            messages, client
        )

        if isinstance(r, str):
            return r
        if r.usage_metadata is None:
            return "[Error] api request went wrong"
        if (
            r.usage_metadata.prompt_token_count
            and r.usage_metadata.candidates_token_count
        ):
            metadata["prompt_token_count"] += r.usage_metadata.prompt_token_count
            metadata["candidates_token_count"] += (
                r.usage_metadata.candidates_token_count
            )

        if r.text:
            return r.text

    return "[Warning] the prompt reach the maximum number of iterations"
