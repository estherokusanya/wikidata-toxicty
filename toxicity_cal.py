from googleapiclient import discovery
import json
import time

API_KEY = 'AIzaSyAPzWiuT0KhB2Iv0jLGKmwKuURivCbw1cc'

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

# analyze_request = {
#   'comment': { 'text': 'Entity[\"Concept\", \"EdgarAllanPoe::dkz2d\"]' },
#   'requestedAttributes': {'TOXICITY': {}}
# }

# response = client.comments().analyze(body=analyze_request).execute()
# # print(json.dumps(response, indent=2))
# print(response['attributeScores']['TOXICITY']['summaryScore']['value'])


##################################

toxicities = []  # Empty list to store toxicity scores

with open("verbalised_triples/female_wiki_resultsverbalised.json", "r") as f:
    triples = json.load(f)

for triple in triples[:100]:  # Iterates through first 100 objects
    analyze_request = {
        'comment': {'text': triple['verbalisation']}, 
        "languages": ["en"],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = client.comments().analyze(body=analyze_request).execute()
    data = {
        "subject": triple["subject"],
        "predicate": triple["predicate"],
        "object": triple["object"],
        "verbalisation": triple['verbalisation'],
        "toxicity": response['attributeScores']['TOXICITY']['summaryScore']['value']
    }
    toxicities.append(data)
    time.sleep(2)

with open("top_100_female_toxicities.json", "w") as f:
    json.dump(toxicities, f, indent=2)