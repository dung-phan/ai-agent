import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    args = sys.argv[1:]

    if not args:
        print("No prompt provided. Please provide a prompt.")
        sys.exit(1)

    prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    res = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    token_usage = res.usage_metadata
    print('prompt:', res.text)
    print("Prompt tokens:", token_usage.prompt_token_count)
    print("Response tokens:", token_usage.candidates_token_count)

if __name__ == "__main__":
    main()
