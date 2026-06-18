import argparse

from google.genai import Client, types

from call_function import available_functions, call_function
from prompts import system_prompt


# TODO: clean this function, too much side-effects
def get_agent_response(
    messages: list[types.Content], client: Client, args: argparse.Namespace
) -> types.GenerateContentResponse:
    response: types.GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.function_calls is not None:
        func_results: list[types.Part] = []
        for fc in response.function_calls:
            func_call_result = call_function(fc)
            if (
                not func_call_result.parts
                or not isinstance(
                    func_call_result.parts[0].function_response,
                    types.FunctionResponse,
                )
                or not func_call_result.parts[0].function_response.response
            ):
                raise Exception("no function response")
            func_results.append(func_call_result.parts[0])
            if args.verbose:
                print(f"-> {func_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=func_results))

        return response
    else:
        print(response.text)
        return response
