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
    for item in data:
        x.append(item["toxicity"])
        average = sum(item["toxic_fraction"]) /len(item["toxic_fraction"])
        y.append(average)

    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    plt.scatter(x, y, c=colours[file])
    plt.xlabel('toxicity')
    plt.ylabel('toxic fraction')

    plt.title(f'{file.upper()} Toxicity to toxic fraction')
    plt.grid()
    plt.show()



##########mapping each file to it's owen 3d grid################
# for file in files:
#     with open(f"new_5000_{file}_toxicities.json", "r") as f:
#         data = json.load(f)

#     x = []
#     y = []
#     z = []
#     for item in data:
#         x.append(item["toxicity"])
#         average = sum(item["toxic_fraction"]) /len(item["toxic_fraction"])
#         y.append(average)
#         z.append(item["sentiment"])

#     fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#     ax.scatter(x, y, z, c=colours[file], marker='x' )
#     ax.set_xlabel('toxicity')
#     ax.set_ylabel('toxic fraction')
#     ax.set_zlabel('sentiment')

# # giving a title to my graph
# plt.title('Toxicity to toxic fraction')
# plt.grid()
# # function to show the plot
# plt.show()



###########mapping all three files on one 3d grid############
# all_x = []
# all_y = []
# all_z = []

# all_colors =[]

# for file in files:
#     with open(f"new_5000_{file}_toxicities.json", "r") as f:
#         data = json.load(f)

#     for item in data:
#         all_x.append(item["toxicity"])
#         average = sum(item["toxic_fraction"]) / len(item["toxic_fraction"])
#         all_y.append(average)
#         all_z.append(item["sentiment"])
#         all_colors.append(colours[file])

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# # Use list comprehension to assign colors from the dictionary
# #all_colors = [colours[file] for file in files]
# print(all_colors)

# ax.scatter(all_x, all_y, all_z, c=all_colors, marker='x')

# ax.set_xlabel('toxicity')
# ax.set_ylabel('toxic fraction')
# ax.set_zlabel('sentiment')

# plt.title('Toxicity to Toxic Fraction Across All Files')
# plt.grid()
# plt.show()