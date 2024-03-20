from googleapiclient import discovery
import json
import time
import random
import nltk
import requests
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from llamaapi import LlamaAPI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
#create toxic metric
#create toxic fraction metric
#create sentiment metric

API_KEY = 'AIzaSyAPzWiuT0KhB2Iv0jLGKmwKuURivCbw1cc'

client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
    )
analyser = SentimentIntensityAnalyzer()

def toxicity_metric():
    files = [ "high_income", "low_income", "male", "trans"]

    for item in files:
        print("Start: ", item)
        toxicities = []
        with open(f"verbalised_triples/{item}_wiki_results_verbalised.json", "r") as f:
            triples = json.load(f)

        numbers = random.sample(range(0,len(triples)),5000)

        for i in numbers:
            analyze_request = {
                'comment': {'text': triples[i]['verbalisation']}, 
                "languages": ["en"],
                'requestedAttributes': {'TOXICITY': {}}
            }
            response = client.comments().analyze(body=analyze_request).execute()
            data = {
                "subject": triples[i]["subject"],
                "predicate": triples[i]["predicate"],
                "object": triples[i]["object"],
                "verbalisation": triples[i]['verbalisation'],
                "toxicity": response['attributeScores']['TOXICITY']['summaryScore']['value']
            }
            toxicities.append(data)
            time.sleep(1.2)
        print("Finished: ", item)
        with open(f"toxicity_results/5000_{item}_toxicities.json", "w") as f:
            json.dump(toxicities, f, indent=2)


def sentiment_metric():
    files = [ "female","high_income", "low_income", "male", "trans"]

    for i in files:
        print("Start: ", i)
        sentiments = []
        with open(f"toxicity_results/5000_{i}_toxicities.json", "r") as f:
            triples = json.load(f)
        for item in triples:
            data = {
                "subject": item["subject"],
                "predicate": item["predicate"],
                "object": item["object"],
                "verbalisation": item['verbalisation'],
                "toxicity": item['toxicity'],
                "sentiment": analyser.polarity_scores(item['verbalisation'])["compound"]
            }
            sentiments.append(data)
        with open(f"toxicity_results/5000_{i}_toxicities.json", "w") as f:
            json.dump(sentiments, f, indent=2)


def toxic_fraction():
    files = [ "female","high_income", "low_income", "male", "trans"]
    llm = ["gpt 3.5", "llama", "davinci", "jurassic", "mistral"]
    for i in files:
        triples = []
        print("Starting: ", i)
        with open(f"toxicity_results/5000_{i}_toxicities.json", "r") as f:
                data = json.load(f)
        for item in data:
            responses = []
            verbalisation = item["verbalisation"]
            for model in llm:
                toxic_fraction = get_toxicity(get_llm_respose(verbalisation, model))
                responses.append(toxic_fraction)
            triple = {
                "subject" : item["subject"],
                "predicate": item["predicate"],
                "object": item["object"],
                "verbalisation": item["verbalisation"],
                "toxicity": item["toxicity"],
                "sentiment": item["sentiment"],
                "toxic_fraction" : responses
            }
            triples.append(triple)

        with open(f"toxicity_results/new_5000_{i}_toxicities.json", "w") as f:
                json.dump(triples, f, indent=2)
    
def get_llm_respose(input, llm):
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

def get_toxicity(text):
    if text == "" or text is None or text.isspace():
        return 0
    time.sleep(1)
    analyze_request = {
                'comment': {'text': text}, 
                "languages": ["en"],
                'requestedAttributes': {'TOXICITY': {}}
            }
    response = client.comments().analyze(body=analyze_request).execute()
    return response['attributeScores']['TOXICITY']['summaryScore']['value']

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

toxic_fraction()