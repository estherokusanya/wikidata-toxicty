import matplotlib.pyplot as plt
import json
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import  numpy as np
 
def scatter_plot():
    colours = {
        "male": "blue",
        "female": "red",
        "trans": "orange"
    }
    #files = ["trans", "female", "male"]
    files = ["female"]

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
        plt.scatter(x, y, c=colours[file], s = 4)
        plt.xlabel('toxicity')
        plt.ylabel('toxic fraction')

        plt.title(f'{file.upper()} Toxicity to toxic fraction')
        plt.grid()
    plt.show()


def box_plot():
    files = ["male", "trans"]
    labels = []
    colors = ["green", "green", "blue", "blue"] 
    data = []
    for file in files:
        with open(f"new_5000_{file}_toxicities.json", "r") as f:
            d = json.load(f)
        data.append([item["toxicity"] for item in d])
        data.append([sum(item["toxic_fraction"])/5 for item in d])
        labels.append(f"{file} toxicity")
        labels.append(f"{file} toxic_fraction")

    
    red_square = dict(markerfacecolor='r', marker='s')
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    ax5.set_title(f'{file.capitalize()} Boxplot')
    boxplots = ax5.boxplot(data, 
                           vert=False, 
                           flierprops=red_square, 
                           showfliers=False, 
                           labels=labels, 
                           patch_artist=True,
                           notch=True,
                           widths = 0.3)
    for patch, color in zip(boxplots['boxes'], colors):
        patch.set_facecolor(color)
    
    # values = [x * 0.005 for x in list(range(0, 25))]
    # ax5.xaxis.set_ticks(values)

    ax5.xaxis.grid(True)
    ax5.legend(files, loc='upper right')

    plt.show()
    
box_plot()

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