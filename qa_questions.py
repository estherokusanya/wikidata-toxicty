from openai import OpenAI
import os
import json
import random

#change so it takes data from toxicity results to q_a combined verbals. No need to have a combined verbals folder

client = OpenAI(
    api_key= "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"
)

files = ["female", "high_income", "low_income", "male", "trans"]

def combine_verbalisations(file,size):
    with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
        data = json.load(f)
    remaining = data
    grouped = []
    changed = True
    while changed and len(remaining)>=size:
        changed = False
        group = []
        current = random.choice(remaining)
        group.append(current)
        remaining.pop(0)
        for x in range(size-1):
            for item in remaining:
                if current["subject"]==item["subject"] or current["object"]==item["object"] or current["predicate"]==item["predicate"]:
                    group.append(item)
                    remaining.remove(item)
                    break
        if len(group)!=size:
            remaining.extend(group)
        else:
            grouped.append(group)
    group = []
    for i in range(0,len(remaining)):
        if i+1%size ==0:
            group.append(remaining[i])
            grouped.append(group)
            group.clear()
        else:
            group.append(remaining[i])

    structured = []
    for item in grouped:
        structured.append({
            "verbalisations": " ".join([x["verbalisation"] for x in item]),
            "toxicities": [x["toxicity"] for x in item],
            "toxic_fraction": [sum(x["toxic_fraction"])/5 for x in item],
            "sentiments": [x["sentiment"] for x in item]
        })

    with open(f"combined_verbals/{file}_results.json", "w") as f:
        json.dump(structured, f, indent=2)

def produce_questions(file):
    output = []
    t = "Give 3 comprehension questions with their answers that can be answered by these sentences as context: "
    text = "Create 3 fill in the blank questions along with their answer based on the information provided in the sentences: "
    with open(f"combined_verbals/{file}_results.json", "r") as f:
        data = json.load(f)
    for item in data:
        message = text + item['verbalisations']
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": message}
            ]
        )
        q_a_json = []
        for i in json.loads(response.choices[0].message.content):
            q_a_json.append(json.loads(response.choices[0].message.content)[i])
            
        current = {
            "verbalisations": item['verbalisations'],
            "toxicities": item['toxicities'],
            "sentiments": item['sentiments'],
            "q_a": q_a_json[0]
        }
        output.append(current)
    with open(f"q_a_verbals/{file}_qa_results.json", "w") as f:
        json.dump(output, f, indent=2)


def calculate():
    for item in files:
        print("currently combining verbalisations of: ",item)
        combine_verbalisations(item)
        print("currently producing questions of: ",item)
        produce_questions(item)

calculate()