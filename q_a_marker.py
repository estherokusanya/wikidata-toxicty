import json
import requests
from llamaapi import LlamaAPI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI

f = ["female", "high_income", "low_income", "male", "trans"]
files = ["female"]
llm = ["gpt 3.5", "llama", "davinci", "jurassic", "mistral"]


def marker():
    for file in files:
        with open(f"q_a_verbals/{file}_qa_results.json", "r") as f:
            data = json.load(f)
        new_data = []
        for set in data[:20]:
            score = 0
            questions = set["q_a"]
            verbalisation = set["verbalisations"]
            # print(verbalisation)
            for item in questions:
                question = item["question"]
                answer = item["answer"]
                prompt = f"Given this context\"{verbalisation}\".  What is the answer to this question: {question}"
                for model in llm:
                    response = get_llm_response(prompt,model)
                    score+=calculate_score(answer,response)
            set["score"] = score
            new_data.append(set)

        with open(f"{file}_qna_results.json", "w") as f:
            json.dump(new_data, f, indent=2)

def calculate_score(answer, response):
    print(answer)
    if type(answer) is list:
        correct = 0
        for x in answer:
            if x.lower() in response.lower():
                correct+=1
        if correct==len(answer):
            return 1
    elif answer.lower() in response.lower():
        
        return 1
    return 0

def get_llm_response(input, llm):
    if llm=="gpt 3.5":
        return do_gpt35(input)
    elif llm=="llama":
        return do_llama(input)
    elif llm=="davinci":
        return do_davinci(input)
    elif llm=="jurassic":
        return do_jurassic(input)
    elif llm=="mistral":
        return do_mistral(input)
    else:
        "ERROR llm not found"


def do_llama(message):
    llama = LlamaAPI('LL-BcBaAuQCqrxRWT5huFSQjIFbsOSHCFyUlFkWYk3BdCMYSLrXtWrEworc7xOOv5eu')
    api_request_json = {
        "model" : "llama-13b-chat",
        "messages": [
            {"role": "system", "content": "Hello how can i help you, I am a chat asisstant"},
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
    return response.choices[0].message.content
 

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
        "system": "Chat Asisstant",
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

marker()