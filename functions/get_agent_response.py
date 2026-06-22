from google.genai import Client, types

from src.call_function import available_functions, call_function
from src.prompts import system_prompt


async def get_agent_response(
    messages: list[types.Content],
    client: Client,
) -> types.GenerateContentResponse | str:
    r: types.GenerateContentResponse = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if r.function_calls is not None:
        func_results: list[types.Part] = []

        for fc in r.function_calls:
            func_call_result = call_function(fc)

            if (
                not func_call_result.parts
                or not isinstance(
                    func_call_result.parts[0].function_response,
                    types.FunctionResponse,
                )
                or not func_call_result.parts[0].function_response.response
            ):
                return "[Error] no function response"
            func_results.append(func_call_result.parts[0])

            messages.append(types.Content(role="user", parts=func_results))

    return r
