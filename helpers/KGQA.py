from openai import OpenAI
import json
import random
from helpers.LinkPrediction import NeighbourhoodHop
from helpers.LLMHelper import LLMHelper
import tracemalloc
import asyncio

class KGQA:

    def __init__(self) -> None:
        pass

    def context_set_up(self, file, q_num, sub_graph_size):
        nHopper = NeighbourhoodHop()
        with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
            data = json.load(f)
        output = []
        questions = random.sample(data, q_num)
        for q in questions:
            sub_graph = nHopper.hop(q["subject"],q["object"], data, current_relations=[], context_budget=sub_graph_size)
            if q not in sub_graph:
                sub_graph.append(q)
            output.append([q, sub_graph])

        with open(f"KGQA/{file}_results.json", "w") as x:
            json.dump(output, x, indent=2)
        self.__create_questions(file)

    def __create_questions(self,file):
        with open(f"KGQA/{file}_results.json", "r") as f:
            data = json.load(f)
        output = []
        for item in data:
            response = self.__open_ai(item[0]["verbalisation"])
            j_object = {
                "verbalisations": " ".join([x["verbalisation"] for x in item[1]]),
                "toxicities": [x["toxicity"] for x in item[1]],
                "toxic_fraction": [sum(x["toxic_fraction"])/5 for x in item[1]],
                "sentiments": [x["sentiment"] for x in item[1]],
                "question": response[0],
                "answer": response[1]
            }
            output.append(j_object)
        with open(f"KGQA/{file}_q_a.json", "w") as x:
            json.dump(output, x, indent=2)
                    
    def __open_ai(self, prompt):
        example = "\'question: Ada Lovelace was born in ______. answer: Marylebone\'"
        t = f"Create a fill in the gap question in the style of {example}, along with its answer that can be answered by this sentence: {prompt}"
        client = OpenAI(api_key= "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")
        response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a helpful assistant who response in json"},
                    {"role": "user", "content": t}
                ],
                max_tokens= 200,
            )
        return list(json.loads(response.choices[0].message.content).values())
    
    def answer(self, file):
        tracemalloc.start()
        asyncio.run(self.answer_helper(file))
        tracemalloc.stop()

    async def answer_helper(self, file):
        with open(f"KGQA/{file}_q_a.json", "r") as f:
            data = json.load(f)
        for item in data:
            verbalisations = item["verbalisations"]
            question  = item["question"]
            prompt = f"Here are some facts that might be relevant to the question: \'{verbalisations}\'. question: {question}  answer: ???"
            score = 0
            for model in ["llama","gpt 3.5", "davinci", "jurassic", "mistral"]:
                helper = LLMHelper()
                response = await helper.get_llm_response(prompt,model)
                if item["answer"].lower() in response.lower():
                    score+=1
            item["score"] = score

        with open(f"KGQA/{file}_q_a.json", "w") as x:
            json.dump(data, x, indent=2)
