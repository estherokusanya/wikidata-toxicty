from helpers.WDV.Verbalisation.verbalisation_module import VerbModule
import json

class WikiVerbalise:
    def __init__(self) -> None:
        pass

    @staticmethod
    def verbalise(file):
        print("starting verbalisation")
        vm = VerbModule()
        with open(f"triple_results/{file}_results.json", "r") as f:
            triples = json.load(f)

        for triple in triples:
            verbalized_text = vm.verbalise_triples([triple])
            triple["verbalisation"] = verbalized_text

        with open(f"triple_results/{file}_results_verbalised.json", "w") as f:
            json.dump(triples, f, indent=2)
