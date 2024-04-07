from llamaapi import LlamaAPI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
import asyncio
import os
import json
import requests
from dotenv import load_dotenv

class LLMHelper:

    def __init__(self) -> None:
        load_dotenv()

    async def get_llm_response(self,input, llm):
        if llm=="gpt 3.5":
            return self.do_gpt35(input)
        elif llm=="llama":
            return await self.do_llama_with_timeout(input)
        elif llm=="davinci":
            return self.do_davinci(input)
        elif llm=="jurassic":
            return self.do_jurassic(input)
        elif llm=="mistral":
            return self.do_mistral(input)
        else:
            "ERROR llm not found"

    async def do_llama(self,message):
        loop = asyncio.get_running_loop()
        llama = LlamaAPI(os.getenv("LLAMA_KEY"))
        api_request_json = {
            "model" : "llama-13b-chat",
            "messages": [
                {"role": "system", "content": "Hello how can i help you, I am a chat assistant"},
                {"role": "user", "content": message}
            ],
            "max_tokens": 200,
        }
        response = await loop.run_in_executor(None, llama.run, api_request_json)
        return response.json()["choices"][0]["message"]["content"]

    async def do_llama_with_timeout(self,message):
        while True:
            try:
                result = await asyncio.wait_for(self.do_llama(message), timeout=7)
                return result
            except asyncio.TimeoutError:
                print("Timeout occurred. Retrying...")

    def do_mistral(self,message):
        # mistral_key = "3Xa02zCJ9vJ3GnTQo6d3C0MBylIitf5G"
        client = MistralClient(api_key=os.getenv("MISTRAL_KEY"))
        model = "open-mistral-7b"
        messages = [
            ChatMessage(role="user", content=message)
        ]
        chat_response = client.chat(
            model=model,
            messages=messages,
        )
        return chat_response.choices[0].message.content

    def do_gpt35(self,message):
        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
        response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": message}
                ],
                max_tokens= 200,
            )
        return response.choices[0].message.content
    
    def do_davinci(self,message):
        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
        response = client.completions.create(
            model="davinci-002",
            prompt=message,
            temperature=1,
            max_tokens=115,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text

    def do_jurassic(self,message):
        url = "https://api.ai21.com/studio/v1/j2-ultra/chat"
        payload = {
            "numResults": 1,
            "temperature": 1,
            "system": "Chat Asisstant",
            "maxTokens": 200,
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
            "Authorization": f"Bearer {os.getenv('JURASSIC_KEY')}"
        }
        response = requests.post(url, json=payload, headers=headers)
        return json.loads(response.text)["outputs"][0]["text"]
    