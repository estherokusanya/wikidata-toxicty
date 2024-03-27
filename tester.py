import requests
import json
from llamaapi import LlamaAPI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI

def do_llama(message):
    llama = LlamaAPI('LL-aSPK15aXNXFA5G0hCQ4KG6nZemedW2MBU6eKTiOT2XsuQPtNtRTsQhBXrjGGg1dk')
    api_request_json = {
        "model" : "llama-13b-chat",
        "messages": [
            {"role": "system", "content": "Hello how can i help you, i am a chat asisstant"},
            {"role": "user", "content": message}
        ],
    }
    response = llama.run(api_request_json)
    print(response)
    return response.json()["choices"][0]["message"]["content"]


print(do_llama("who is barack"))