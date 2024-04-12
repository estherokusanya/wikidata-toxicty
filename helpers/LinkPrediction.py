import json
import random
import tracemalloc
from helpers.LLMHelper import LLMHelper
import asyncio

class NeighbourhoodHop:
    def __init__(self) -> None:
        pass

    def hop(self,subject, object, graph, current_relations, context_budget):
        output= []
        for triple in graph:
            compare = [triple["subject"], triple["object"]]
            for x in compare:
                if not(triple in current_relations or triple in output) and (subject in x or object in x):
                    output.append(triple)
            if len(output)>=context_budget:
                break
        return output

    def two_hop_neighbourhood(self, graph, q_num, hop1_budget, hop2_budget):
        output = []
        choices=random.sample(graph, q_num)
        for choice in choices:
            hop1 = self.hop(choice["subject"], choice["object"], graph, current_relations=[], context_budget=hop1_budget)
            hop2 = []
            for item in hop1:
                hop2.extend(self.hop(item["subject"], item["object"], graph, hop1+hop2.copy(), hop2_budget))
            complete = hop1+hop2

            while choice in complete:  
                complete.remove(choice)
            output.append([choice, complete])

        return output


class LinkPrediction:

    def __init__(self) -> None:
        self.training_example =  """
                For example a triple with a missing link: 
                (Darvin Ham, ________, Basketball Coach)

                Given this context:
                (Darvin Ham, colleague_of, Mike Brown)
                (Mike Brown, occupation, Basketball Coach)
                (Mike Brown, coaches_team, Los Angeles Lakers)
                (Los Angeles Lakers, league, National Basketball Association)

                The missing link in the triple is: occupation. (Darvin Ham, occupation, Basketball Coach)
                End of Example. 
        """

    def context_set_up(self, file, q_num, context_budget):
        """
            Performs two hop negihbourhood and creates link prediction tasks

            file: name of category ie. male, female
            qnum: the number of tasks to create
            sub_graph_size: context budget for each task
            
        """

        nHopper = NeighbourhoodHop()
        with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
            data = json.load(f)
        budget1 = round(context_budget*0.8)
        budget2 = context_budget-budget1
        output = self.reformat(nHopper.two_hop_neighbourhood(data, q_num, budget1, budget2))

        with open(f"Link_Prediction/{file}_results.json", "w") as x:
            json.dump(output, x, indent=2)

    def answer(self, file):
        tracemalloc.start()
        asyncio.run(self.__answer_helper(file))
        tracemalloc.stop()

    async def __answer_helper(self, file):
        with open(f"Link_Prediction/{file}_results.json", "r") as f:
            data = json.load(f)
        helper = LLMHelper()
        for item in data:
            subgraph = item["subgraph"]
            missing_link = item["missing_link"]
            prompt = self.training_example + f"Here is some context: {subgraph}. What is the missing link in this triple: {missing_link}"
            score = 0
            for model in ["llama","gpt 3.5", "davinci", "jurassic", "mistral"]:
                response = await helper.get_llm_response(prompt,model)
                if self.__is_correct(item["answer"], response):
                    score+=1
            item["score"] = score
        with open(f"Link_Prediction/{file}_results.json", "w") as x:
            json.dump(data, x, indent=2)

    def __is_correct(self,answer, response):
        if answer.lower() in response.lower():
            return True
        elif all(item in response.lower().split() for item in answer.lower().split()):
            return True
        return False

    def __triple_as_string(self,triple):
        return "("+triple["subject"]+", "+triple["predicate"]+", "+ triple["object"]+")"

    def reformat(self,input):
        output = []
        for item in input:
            verbalisation= "("+item[0]["subject"]+", "+ "______, "+item[0]["object"]+")"
            subgraph = [self.__triple_as_string(x) for x in item[1]]
            triple = "("+item[0]["subject"] +", "+ item[0]["predicate"]+", "+ item[0]["object"]+")"
            item[1].append(item[0])
            output.append({
                "chosen_triple": triple,
                "missing_link": verbalisation,
                "answer": item[0]["predicate"],
                "subgraph": subgraph,
                "toxicities": [x["toxicity"] for x in item[1]],
                "toxic_fractions": [sum(x["toxic_fraction"])/5 for x in item[1]],
                "sentiments": [x["sentiment"] for x in item[1]]
            })
        return output
