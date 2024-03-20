import pandas as pd
import json

files = [ "female","high_income", "low_income", "male", "trans"]

f = [ "female"]

for item in files:
   with open(f"toxicity_results/5000_{item}_toxicities.json", "r") as file:
      data = json.load(file)

   toxicity_values = [i["toxicity"] for i in data]

   mean = sum(toxicity_values) / len(toxicity_values)
   median = sorted(toxicity_values)[len(toxicity_values) // 2]
   standard_deviation = pd.Series(toxicity_values).std()
   mode = max(toxicity_values)

   print("")
   print(f"{item.upper()} RESULTS")
   print("-------------")
   print("Mean toxicity:", mean)
   print("Median toxicity:", median)
   print("Standard deviation of toxicity:", standard_deviation)
   print("Mode toxicity:", mode)
   print("")
