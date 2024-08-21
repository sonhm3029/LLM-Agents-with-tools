import instructor
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

PROMPT = """
You are a helpful assistant help user to find direction in hospital if were asked. Use the supplied tools to assist the user.
"""

messages = [
    {"role": "system", "content": PROMPT}
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_location",
            "description": "Get the current location of user. Call this whenever you need to know about user current location but only call this if user is outdoor. You have to ask user indoor or outdoor first"
        }
    }
]

while True:
    msg = input("User > ")
    messages.append({
        "role": "user",
        "content": msg
    })
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools
    )
    print(response)
    answer = response.choices[0].message.content
    messages.append({
        "role": "assistant",
        "content": answer
    })