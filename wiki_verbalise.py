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



#######################################################################

# with open("triple_results/trans_wiki_results.json", "r") as f:
#     triples = json.load(f)

# # Initialize the verbalization module

# # Create a list to store verbalized triples
# verbalized_triples = []

# # Process each triple
# for triple in triples:
#     verbalized_text = vm.verbalise_triples([triple])  # Use the module's function for triples
#     verbalized_triple = {
#         "subject": triple["subject"],
#         "predicate": triple["predicate"],
#         "object": triple["object"],
#         "verbalisation": verbalized_text
#     }
#     verbalized_triples.append(verbalized_triple)
#     print("",verbalized_triple)

# # Save verbalized triples to a new JSON file
# with open("trans_verbalised_triples.json", "w") as f:
#     json.dump(verbalized_triples, f, indent=2)  # Indent for readability