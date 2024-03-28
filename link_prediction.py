from openai import OpenAI
import os
import json
import random

#files = ["female", "high_income", "low_income", "male", "trans"]
files = ["male"]

def combine_verbalisations(file, graph_size):
    with open(f"new_5000_{file}_toxicities.json", "r") as f:
        data = json.load(f)
    remaining = data[:3000]
    counter= 0
    grouped = []

    while counter<len(remaining):
        counter+=1
        group = []
        current = remaining[0]
        group.append(current)
        remaining.remove(current)
        for item in remaining:
            if (item["subject"] in [x["subject"] for x in group]) or (item["object"] in [x["object"] for x in group]):# or (item["predicate"] in [x["predicate"] for x in group]):
                group.append(item)
                remaining.remove(item)
            if len(group)==graph_size:
                break

        if len(group)!=graph_size:
            remaining.extend(group)
        else:
            grouped.append(group)
            remaining.append(random.choice(group))
            counter=0

    structured = []
    for item in grouped:
        structured.append({
            "verbalisations": " ".join([x["verbalisation"] for x in item]),
            "toxicities": [x["toxicity"] for x in item],
            "toxic_fraction": [sum(x["toxic_fraction"])/5 for x in item],
            "sentiments": [x["sentiment"] for x in item]
        })

        with open(f"link_prediction/{file}_results.json", "w") as f:
            json.dump(structured, f, indent=2)

def remove_triple(file):
    with open(f"link_prediction/{file}_results.json", "r") as f:
        data = json.load(f)
    results = []
    for item in data:
        sentence_split = item["verbalisations"].split(". ")
        chosen1 = random.choice(sentence_split)
        sentence_split.remove(chosen1)
        chosen2 = random.choice(sentence_split)
        sentence_split.remove(chosen2)
        results.append({
            "subset_verbalisation": sentence_split,
            "chosen_triple": [chosen1, chosen2],
            "toxicities": item["toxicities"],
            "toxic_fraction": item["toxic_fraction"],
            "sentiments": item["sentiments"]
        })
        
    with open(f"link_prediction/removed_triple_{file}_results.json", "w") as f:
            json.dump(results, f, indent=2)

def produce_questions(file):
    output = []
    context = "Create a fill in the blank question along the answer based on this sentence:"
    with open(f"link_prediction/{file}_results.json", "r") as f:
        data = json.load(f)
    for item in data:
        questions=[]
        for i in range(2):
            message = context + item["chosen_triple"]
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content": message}]
            )
            for i in json.loads(response.choices[0].message.content):
                questions.append(json.loads(response.choices[0].message.content)[i])
        item["questions"] = questions
        output.append(item)
    with open(f"link_prediction/{file}_questions.json", "w") as f:
        json.dump(output, f, indent=2)

for item in files:
    combine_verbalisations(item, 10)
    print("reached")
    remove_triple(item)
    produce_questions(item)
