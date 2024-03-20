import matplotlib.pyplot as plt
import json
 
# x axis values
colours = {
    "male": "blue",
    "female": "red",
    "trans": "orange"
}
files = ["trans", "female", "male"]
#files = ["trans"]
#files = ["female",]
#files = ["male"]

for file in files:
    with open(f"new_5000_{file}_toxicities.json", "r") as f:
        data = json.load(f)

    x = []
    y = []
    for item in data:
        x.append(item["toxicity"])
        average = sum(item["toxic_fraction"]) /len(item["toxic_fraction"])
        y.append(average)
 
    plt.scatter(x, y, c=colours[file] )
 
# naming the x axis
plt.xlabel('toxicity')

# naming the y axis
plt.ylabel('toxic fraction')

# giving a title to my graph
plt.title('Toxicity to toxic fraction')
plt.grid()
# function to show the plot
plt.show()
