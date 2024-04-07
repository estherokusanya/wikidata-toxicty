from googleapiclient import discovery
import json
import time
import random
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os
load_dotenv()

class PerspectiveAPIClient:
    
    def __init__(self) -> None:
        pass
    @staticmethod
    def get_toxicity_score(input):
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=os.getenv("PERSPECTIVEAPI_KEY"),
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
            )
        analyze_request = {
                    'comment': {'text': input}, 
                    "languages": ["en"],
                    'requestedAttributes': {'TOXICITY': {}}
                }
        response = client.comments().analyze(body=analyze_request).execute()
        return response['attributeScores']['TOXICITY']['summaryScore']['value']

def toxicity_metric(file):
    numbers = random.sample(range(0,len(triples)),5000)
    with open(f"triple_results/{file}_results_verbalised.json", "r") as f:
        triples = json.load(f)

    for i in numbers:
        triples[i]["toxicity"] = PerspectiveAPIClient.get_toxicity_score(triples[i]["verbalisation"])
        time.sleep(1.1)

    with open(f"toxicity_results/5000_{file}_toxicities.json", "w") as f:
        json.dump(triples, f, indent=2)


def sentiment_metric(file):
    analyser = SentimentIntensityAnalyzer()

    with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
        triples = json.load(f)

    for item in triples:
        item["sentiment"] = analyser.polarity_scores(item['verbalisation'])["compound"]

    with open(f"toxicity_results/5000_{file}_toxicities.json", "w") as f:
        json.dump(triples, f, indent=2)