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
        messages=message_array
    )

    return completion

system_prompt_msg = """You are a senior software engineer.

Your job is to answer programming questions.

When writing code:

- Explain briefly.
- Produce clean code.
- Mention time complexity.
- Mention space complexity.
- If multiple solutions exist, mention the better one."""


user_input = input("What is in your mind: ")

message_array = [
    {
        "role": "system",
        "content": system_prompt_msg
    },
    {
        "role": "user",
        "content": user_input
    }
]

response = make_request(message_array)

print(response.choices[0].message.content)

message_array.append({
    "role": "assistant",
    "content": response.choices[0].message.content
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

    assistant_response = response.choices[0].message.content

    print(assistant_response)

    message_array.append({
        "role": "assistant",
        "content": assistant_response
    })