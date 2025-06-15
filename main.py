import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from config import MAX_ITERATION
from genai_call_function import available_functions, call_function
from genai_prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    args = sys.argv[1:]
    is_verbose =  "--verbose" in args

    if not args:
        print("No prompt provided. Please provide a prompt.")
        sys.exit(1)

    prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    if is_verbose:
        print('User prompt:', prompt)

    for _ in range(MAX_ITERATION):
        response = generate_content(client, messages, is_verbose)
        for candidate in response.candidates:
            messages.append(candidate.content)
        if response.function_calls:
            for f in response.function_calls:
                result = call_function(f, is_verbose)
                messages.append(result)
                if not result.parts[0] or not result.parts[0].function_response:
                    raise Exception("Empty function call result")
                if is_verbose:
                    print(f"-> {result.parts[0].function_response.response['result']}")
        elif response.text:
            print("Result", response.text)
            break


def generate_content(client, messages, is_verbose):
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
    )

    token_usage = res.usage_metadata

    if is_verbose:
        print("Prompt tokens:", token_usage.prompt_token_count)
        print("Response tokens:", token_usage.candidates_token_count)
    else:
        print("Response:", res.text)

    return res
if __name__ == "__main__":
    main()
