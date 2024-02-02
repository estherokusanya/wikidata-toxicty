import pandas as pd
import json

# Read the JSON data from the file
with open("toxicity_results/top_100_male_toxicities.json", "r") as file:
   data = json.load(file)

# Extract the toxicity values into a list
toxicity_values = [item["toxicity"] for item in data]

# Calculate mean, median, and standard deviation
mean = sum(toxicity_values) / len(toxicity_values)
median = sorted(toxicity_values)[len(toxicity_values) // 2]
standard_deviation = pd.Series(toxicity_values).std()
mode = max(toxicity_values)

# Print the resultss
print("MALE RESULTS")
print("-------------")
print("Mean toxicity:", mean)
print("Median toxicity:", median)
print("Standard deviation of toxicity:", standard_deviation)
print("Mode toxicity:", mode)
print("")

#########################################################################

# Read the JSON data from the file
with open("toxicity_results/top_100_female_toxicities.json", "r") as file:
   data = json.load(file)

# Extract the toxicity values into a list
toxicity_values = [item["toxicity"] for item in data]

# Calculate mean, median, and standard deviation
mean = sum(toxicity_values) / len(toxicity_values)
median = sorted(toxicity_values)[len(toxicity_values) // 2]
standard_deviation = pd.Series(toxicity_values).std()
mode = max(toxicity_values)

# Print the results
print("FEMALE RESULTS")
print("-------------")
print("Mean toxicity:", mean)
print("Median toxicity:", median)
print("Standard deviation of toxicity:", standard_deviation)
print("Mode toxicity:", mode)