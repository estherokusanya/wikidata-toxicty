import matplotlib.pyplot as plt
import json
from mpl_toolkits.mplot3d import Axes3D
 
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
    z = []
    for item in data:
        x.append(item["toxicity"])
        average = sum(item["toxic_fraction"]) /len(item["toxic_fraction"])
        y.append(average)
        z.append(item["sentiment"])
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.scatter(x, y,z, c=colours[file], marker='x' )
 
# naming the x axis
plt.xlabel('toxicity')

# naming the y axis
plt.ylabel('toxic fraction')
ax.set(xticklabels=["hi"],
       yticklabels=["oshdg"],
       zticklabels=["gggggg"])

# giving a title to my graph
plt.title('Toxicity to toxic fraction')
plt.grid()
# function to show the plot
plt.show()
