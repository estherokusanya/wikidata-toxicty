import json
import asyncio
import tracemalloc
from helpers.CalculateMetrics import PerspectiveAPIClient
from helpers.LLMHelper import LLMHelper

class ToxicFraction:

    def __init__(self) -> None:
        pass

    def run(self, file):
        tracemalloc.start()
        asyncio.run(self.__toxic_fraction(file))
        tracemalloc.stop()
    
    async def __toxic_fraction(self,file):
        with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
            data = json.load(f)
        llm = LLMHelper()
        for item in data:
            responses = []
            verbalisation = item["verbalisation"]
            for model in ["llama","gpt 3.5", "davinci", "jurassic", "mistral"]:
                response = await llm.get_llm_response(verbalisation,model)
                toxic_fraction = PerspectiveAPIClient.get_toxicity_score(response)
                responses.append(toxic_fraction)
            item["toxic_fraction"] = responses
            with open(f"toxicity_results/5000_{file}_toxicities.json", "a") as x:
                json.dump(data, x, indent=2)

        print("complete")
