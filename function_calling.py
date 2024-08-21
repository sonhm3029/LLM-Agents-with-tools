import instructor
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import json

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

def get_user_location():
    r = requests.post(
        'https://www.googleapis.com/geolocation/v1/geolocate',
        params={
            "key": os.environ["GOOGLE_API_KEY"]}, json={"homeMobileCountryCode":310,
    "homeMobileNetworkCode":410,
    "radioType":"gsm",
    "carrier":"Vodafone",
    "considerIp":True})
    # Export the data for use in future steps
    return r.json()

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
    if not answer and response.choices[0].finish_reason=="tool_calls":
        tool_call = response.choices[0].message.tool_calls[0]
        # arguments = json.loads(tool_call['function']['arguments'])
        location = get_user_location()
        print(f"LOC: {location}")
        messages = messages + [
            response.choices[0].message,
            {"role": "tool", "content": json.dumps(location), "tool_call_id": tool_call.id}
        ]
    else: 
        messages.append({
            "role": "assistant",
            "content": answer
        })