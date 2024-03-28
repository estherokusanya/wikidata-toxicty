import pandas as pd
import json

files = [ "female", "male", "trans"]

for item in files:
   with open(f"new_5000_{item}_toxicities.json", "r") as file:
      data = json.load(file)

   toxicity_values = [i["toxicity"] for i in data]
   fraction_values = [sum(x["toxic_fraction"])/5 for x in data]

   fraction_mean = sum(fraction_values) /len(fraction_values)
   fraction_median = sorted(fraction_values)[len(fraction_values) // 2]
   fraction_sd = pd.Series(fraction_values).std()
   fraction_mode = max(fraction_values)

   mean = sum(toxicity_values) / len(toxicity_values)
   median = sorted(toxicity_values)[len(toxicity_values) // 2]
   standard_deviation = pd.Series(toxicity_values).std()
   mode = max(toxicity_values)

   print("")
   print(f"{item.capitalize()} RESULTS")
   print("-------------")
   print(f"Mean toxicity: {mean} | Mean toxic_fraction: {fraction_mean}" )
   print(f"Median toxicity: {median} | Median toxic_fraction: {fraction_median}")
   print(f"Standard deviation of toxicity: {standard_deviation} | SD toxic_fraction: {fraction_sd}")
   print(f"Mode toxicity: {mode}, | Mode toxic_fraction: {fraction_mode}")
   print("")
