from openai import OpenAI
import os
import json
import random

#files = ["female", "high_income", "low_income", "male", "trans"]
files = ["female"]

def combine_verbalisations(file, size):
    with open(f"new_5000_{file}_toxicities.json", "r") as f:
        data = json.load(f)
    remaining = data[:200]
    changed= True
    grouped = []
    while changed and len(remaining)>=size:
        changed = False
        group = []
        current = random.choice(remaining)
        group.append(current)
        remaining.remove(current)
        for x in range(size-1):
            for item in remaining:
                if current["subject"]==item["subject"] or current["object"]==item["object"] or current["predicate"]==item["predicate"]:
                    group.append(item)
                    remaining.remove(item)
                    changed=True
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

        with open(f"link_prediction/{file}_results.json", "w") as f:
            json.dump(structured, f, indent=2)

def remove_triple(file):
    with open(f"link_prediction/{file}_results.json", "r") as f:
        data = json.load(f)
    results = []
    for item in data:
        sentence_split = item["verbalisations"].split(". ")
        chosen = random.choice(sentence_split)
        sentence_split.remove(chosen)
        results.append({
            "subset_verbalisation": sentence_split,
            "chosen_triple": chosen,
            "toxicities": item["toxicities"],
            "toxic_fraction": item["toxic_fraction"],
            "sentiments": item["sentiments"]
        })

    with open(f"link_prediction/removed_triple_{file}_results.json", "w") as f:
            json.dump(results, f, indent=2)
            print("reached")


for item in files:
    combine_verbalisations(item, 20)
    remove_triple(item)
