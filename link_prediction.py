from openai import OpenAI
import os
import json
import random

def combine_verbalisations(file):
    with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
        data = json.load(f)
    remaining = data
    grouped = []
    for i in range(int(len(remaining)/4)):
        group = []
        current = random.choice(remaining)
        group.append(current)
        remaining.pop(0)
        for x in range(19):
            for item in remaining:
                if current["subject"]==item["subject"] or current["object"]==item["object"] or current["predicate"]==item["predicate"]:
                    group.append(item)
                    remaining.remove(item)
                    break
        if len(group)!=4:
            remaining.extend(group)
        else:
            grouped.append(group)
    group = []
    for i in range(0,len(remaining)):
        if i+1%4 ==0:
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
            "toxic_fraction": [x["toxic_fraction"] for x in item],
            "sentiments": [x["sentiment"] for x in item]
        })

    with open(f"combined_verbals/{file}_results.json", "w") as f:
        json.dump(structured, f, indent=2)