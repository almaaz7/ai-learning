from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv('API_KEY')
)


def make_request(message_array):
    completion = client.chat.completions.create(
        model="meta/llama-3.2-3b-instruct",
        messages=message_array,
        stream=True
    )

    return completion


user_input = input("What is in your mind: ")

message_array = [
    {
        "role": "user",
        "content": user_input
    }
]

response = make_request(message_array)

assistant_response = ""

for chunk in response:

    text = chunk.choices[0].delta.content # here the message is not used instead we use delta.content to get the text

    if text:
        assistant_response += text
        print(text, end="", flush=True)
    print("\n")

# print(response.choices[0].message.content)

message_array.append({
    "role": "assistant",
    "content": assistant_response
})

while True:

    new_message = input("You: ")

    if new_message.lower() == "exit":
        print("Exiting chat")
        break

    conversation_dict = {
        "role": "user",
        "content": new_message
    }

    message_array.append(conversation_dict)

    response = make_request(message_array)

    for chunk in response:

        text = chunk.choices[0].delta.content # here the message is not used instead we use delta.content to get the text

        if text:
            assistant_response += text
            print(text, end="", flush=True)
        print("\n")

    message_array.append({
        "role": "assistant",
        "content": assistant_response
    })