from googleapiclient import discovery
import json
import time
import random

API_KEY = 'AIzaSyAPzWiuT0KhB2Iv0jLGKmwKuURivCbw1cc'

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

files = [ "high_income", "low_income", "male", "trans"]

for item in files:
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

    with open(f"5000_{item}_toxicities.json", "w") as f:
        json.dump(toxicities, f, indent=2)