import requests
import json
from llamaapi import LlamaAPI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI

def do_llama(message):
    llama = LlamaAPI('LL-BcBaAuQCqrxRWT5huFSQjIFbsOSHCFyUlFkWYk3BdCMYSLrXtWrEworc7xOOv5eu')
    api_request_json = {
        "model" : "llama-13b-chat",
        "messages": [
            {"role": "system", "content": "Hello how can i help you, i am a chat asisstant"},
            {"role": "user", "content": message}
        ],
    }
    response = llama.run(api_request_json)
    return response.json()["choices"][0]["message"]["content"]

def do_mistral(message):
    mistral_key = "ErRXZzwBKT73q1YgFt1RR7egukO9hkzM"
    client = MistralClient(api_key=mistral_key)
    model = "open-mistral-7b"
    messages = [
        ChatMessage(role="user", content=message)
    ]
    chat_response = client.chat(
        model=model,
        messages=messages,
    )
    return chat_response.choices[0].message.content

def do_gpt35(message):
    client = OpenAI(api_key= "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")
    response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": message}
            ]
        )
    print(response.choices[0].message.content)

def do_davinci(message):
    client = OpenAI(api_key= "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")
    response = client.completions.create(
        model="davinci-002",
        prompt=message,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text


def do_jurassic(message):
    url = "https://api.ai21.com/studio/v1/j2-ultra/chat"

    payload = {
        "numResults": 1,
        "temperature": 1,
        "system": "chatbot",
        "messages": [
            {
            "text": " I am a helpful assistant",
            "role": "assistant"
            },
            {
                "text": message,
                "role": "user"
            }
        ],
        
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer UXwkj2IWKajoMFdRGQatlPdMXgmVk0AG"
    }

    response = requests.post(url, json=payload, headers=headers)
    return json.loads(response.text)["outputs"][0]["text"]

print(do_llama("Romano Prodi's sibling is Giorgio Prodi."))