from WDV.Verbalisation.verbalisation_module import VerbModule
import json

#"female_wiki_results"
files = [ "high_income_wiki_results", "low_income_wiki_results", "male_wiki_results", "trans_wiki_results"]

vm = VerbModule()

for item in files:
    with open(f"triple_results/{item}.json", "r") as f:
        triples = json.load(f)

    verbalized_triples = []

    for triple in triples:
        verbalized_text = vm.verbalise_triples([triple])
        verbalized_triple = {
            "subject": triple["subject"],
            "predicate": triple["predicate"],
            "object": triple["object"],
            "verbalisation": verbalized_text
        }
        verbalized_triples.append(verbalized_triple)
        # print("",verbalized_triple)

    with open(f"verbalised_triples/{item}_verbalised.json", "w") as f:
        json.dump(verbalized_triples, f, indent=2)
