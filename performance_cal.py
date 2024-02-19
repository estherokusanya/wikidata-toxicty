from openai import OpenAI
import os
import json

client = OpenAI(
    api_key= "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"
)

files = ["female", "high_income", "low_income", "male", "trans"]

def produce_questions(file):
    output = []
    text = "Give 3 comprehension questions with their answers that can be answered by these sentences as context: "
    with open(f"combined_verbals/{file}_results.json", "r") as file:
        data = json.load(file)

    for item in data:
        message = text + item['verbalisation']
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": message}
            ]
        )
        q_a_json = [value for value in json.loads(response.choices[0].message.content)]
        current = {
            "verbalisation": item['verbalisation'],
            "toxicity": item['toxicity'],
            "q_a": q_a_json
        }
        output.append(current)
    with open(f"q_a_verbals/{file}_qa_results.json", "w") as f:
        json.dump(output, f, indent=2)


def share_element(v1, v2):
    return (v1["subject"] == v2["subject"] or
            v1["predicate"] == v2["predicate"] or
            v1["object"] == v2["object"])


def combine_verbalisations(file):
    with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as file:
        data = json.load(file)
    combined_verbalisations = []
    current_group = []
    for i, v in enumerate(data):
        if len(current_group) == 2:
            if share_element(current_group[0], v) or share_element(current_group[1], v):
                current_group.append(v)
                toxicities = [item["toxicity"] for item in current_group]
                combined_verbalisation = " ".join([item["verbalisation"] for item in current_group])
                combined_verbalisations.append({"verbalisation": combined_verbalisation, "toxicity": toxicities})
                current_group = []
            else:
                current_group = [v]
        else:
            current_group.append(v)

    if current_group:
        toxicities = [item["toxicity"] for item in current_group]
        combined_verbalisation = " ".join([item["verbalisation"] for item in current_group])
        combined_verbalisations.append({"verbalisation": combined_verbalisation, "toxicity": toxicities})
        
    with open(f"combined_verbals/{file}_results.json", "w") as f:
        json.dump(combined_verbalisations, f, indent=2)


def calculate():
    for item in files:
        combine_verbalisations(item)
        produce_questions(item)
