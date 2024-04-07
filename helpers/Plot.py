import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np

class Plot:

    def __init__(self):
        self.colours = {
            "male": "blue",
            "female": "green",
            "trans": "orange",
            "high_income": "pink",
            "low_income": "red"
        }
        self.files = ["trans", "female", "male", "high_income", "low_income"]
 
    def plot_toxicity_to_fraction(self,file):
        with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
            data = json.load(f)
        x = []
        y = []
        for item in data:
            x.append(item["toxicity"])
            average = sum(item["toxic_fraction"]) /len(item["toxic_fraction"])
            y.append(average)
        plt.scatter(x, y, c=self.colours[file], s = 4)
        plt.xlabel('toxicity')
        plt.ylabel('toxic fraction')
        plt.title(f'{file.capitalize()} Toxicity to Toxic Fraction')
        plt.grid()
        plt.show()

    def plot_toxicity_to_sentiment(self,file):
        with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
            data = json.load(f)
        x = []
        y = []
        for item in data:
            x.append(item["toxicity"])
            y.append(item["sentiment"])
        plt.scatter(x, y, c=self.colours[file], s = 4)
        plt.xlabel('toxicity')
        plt.ylabel('sentiment')
        plt.title(f'{file.capitalize()} Toxicity to Sentiment')
        plt.grid()
        plt.show()

    def box_plot(self,files):
        labels = []
        data = []
        c= [color for color in self.colours.values() for _ in range(2)]
        for file in files:
            with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
                d = json.load(f)
            data.append([item["toxicity"] for item in d])
            data.append([sum(item["toxic_fraction"])/5 for item in d])
            labels.append(f"{file} toxicity")
            labels.append(f"{file} toxic_fraction")

        red_square = dict(markerfacecolor='r', marker='s')
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        ax5.set_title(f'Boxplot')
        boxplots = ax5.boxplot(data, 
                            vert=False,
                            flierprops=red_square,
                            showfliers=False,
                            labels=labels,
                            patch_artist=True,
                            notch=False,
                            widths = 0.3)
        for patch, color in zip(boxplots['boxes'], c):
            patch.set_facecolor(color)

        ax5.xaxis.grid(True)
        ax5.legend(files, loc='upper right')

        plt.show()

    def plot_3d(self,file):
        with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
            data = json.load(f)
        x= []
        y= []
        z= []
        for item in data:
            x.append(item["toxicity"])
            average = sum(item["toxic_fraction"]) /len(item["toxic_fraction"])
            y.append(average)
            z.append(item["sentiment"])

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.scatter(x, y, z, c=self.colours[file], marker='x' )
        ax.set_xlabel('toxicity')
        ax.set_ylabel('toxic fraction')
        ax.set_zlabel('sentiment')
        plt.title('Toxicity, Toxic Fraction, Sentiment')
        plt.grid()
        plt.show()

    def display_metrics(self,file):
        with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
            data = json.load(f)

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
        print(f"{file.capitalize()} RESULTS")
        print("-------------")
        print(f"Mean toxicity: {mean} | Mean toxic_fraction: {fraction_mean}" )
        print(f"Median toxicity: {median} | Median toxic_fraction: {fraction_median}")
        print(f"Standard deviation of toxicity: {standard_deviation} | SD toxic_fraction: {fraction_sd}")
        print(f"Mode toxicity: {mode}, | Mode toxic_fraction: {fraction_mode}")
        print("")


    def display_all_kgqa_results(self, files):
        figure, axis = plt.subplots(2, 2)
        toxicities = [[],[],[],[],[],[]]
        toxic_fraction = [[],[],[],[],[],[]]
        for file in files:
            with open(f"KGQA/{file}_q_a.json", "r") as f:
                data = json.load(f)
            for item in data:
                toxicities[item["score"]].append(np.median(item["toxicities"]))
                toxic_fraction[item["score"]].append(np.median(item["toxic_fraction"]))
        
        label = list(range(0,6))
        ax2 = axis[0, 0].twinx()
        ax2.bar(label,[len(i) for i in toxicities], width=0.35, edgecolor="white", linewidth=0.7, color="coral",zorder=0)
        ax2.set_ylabel("Score Frequency")
        axis[0, 0].plot(label,[np.mean(i) for i in toxicities], zorder=5)
        axis[0, 0].set_title("Toxicity to Score")
        axis[0, 0].set_ylabel(" mean toxicity")
        x = [np.mean(i) for i in toxicities]
        mini = np.min(x) - (np.std(x)*4)
        maxi = np.max(x) + (np.std(x))
        axis[0, 0].set_ylim(ymin=mini, ymax=maxi)

        axis[0, 1].plot(label,[np.mean(i) for i in toxic_fraction])
        axis[0, 1].set_title("Toxic Fraction to Score")
        axis[0, 1].set_ylabel("mean toxic fraction")
        x = [np.mean(i) for i in toxic_fraction]
        mini = np.min(x) - (np.std(x)*4)
        maxi = np.max(x) + (np.std(x))
        axis[0, 1].set_ylim(ymin=mini, ymax=maxi)

        axis[1, 0].boxplot(toxicities, notch=False, patch_artist=True, vert=True, labels=label, showfliers=False)
        axis[1, 0].set_ylabel("median toxicity")
        axis[1, 0].set_xlabel("score")

        axis[1, 1].boxplot(toxic_fraction, notch=False, patch_artist=True, vert=True, labels=label, showfliers=False)
        axis[1, 1].set_ylabel("median toxic fraction")
        axis[1, 1].set_xlabel("score")
        plt.suptitle("KGQA Results")
        plt.show()
    
    def display_all_linkp_resulst(self, files):
        figure, axis = plt.subplots(2, 2)
        toxicities = [[],[],[],[],[],[]]
        toxic_fraction = [[],[],[],[],[],[]]
        for file in files:
            with open(f"Link_Prediction/{file}_results.json", "r") as f:
                data = json.load(f)
            for item in data:
                toxicities[item["score"]].append(np.median(item["toxicities"]))
                toxic_fraction[item["score"]].append(np.median(item["toxic_fractions"]))
        
        label = list(range(0,6))
        ax2 = axis[0, 0].twinx()
        ax2.bar(label,[len(i) for i in toxicities], width=0.35, edgecolor="white", linewidth=0.7, color="coral",zorder=0)
        ax2.set_ylabel("Score Frequency")
        axis[0, 0].plot(label,[np.mean(i) for i in toxicities], zorder=5)
        axis[0, 0].set_title("Toxicity to Score")
        axis[0, 0].set_ylabel(" mean toxicity")
        x = [np.mean(i) for i in toxicities]
        mini = np.min(x) - (np.std(x)*4)
        maxi = np.max(x) + (np.std(x))
        axis[0, 0].set_ylim(ymin=mini, ymax=maxi)

        axis[0, 1].plot(label,[np.mean(i) for i in toxic_fraction])
        axis[0, 1].set_title("Toxic Fraction to Score")
        axis[0, 1].set_ylabel("mean toxic fraction")
        x = [np.mean(i) for i in toxic_fraction]
        mini = np.min(x) - (np.std(x)*4)
        maxi = np.max(x) + (np.std(x))
        axis[0, 1].set_ylim(ymin=mini, ymax=maxi)

        axis[1, 0].boxplot(toxicities, notch=False, patch_artist=True, vert=True, labels=label, showfliers=False)
        axis[1, 0].set_ylabel("median toxicity")
        axis[1, 0].set_xlabel("score")

        axis[1, 1].boxplot(toxic_fraction, notch=False, patch_artist=True, vert=True, labels=label, showfliers=False)
        axis[1, 1].set_ylabel("median toxic fraction")
        axis[1, 1].set_xlabel("score")
        plt.suptitle("Link Prediction Results")
        plt.show()

    def display_kgqa_results(self, file):
        with open(f"KGQA/{file}_q_a.json", "r") as f:
            data = json.load(f)
        figure, axis = plt.subplots(2, 2)
        toxicities = [[],[],[],[],[],[]]
        toxic_fraction = [[],[],[],[],[],[]]
        for item in data:
            toxicities[item["score"]].append(np.median(item["toxicities"]))
            toxic_fraction[item["score"]].append(np.median(item["toxic_fraction"]))

        label = list(range(0,6))
        ax2 = axis[0, 0].twinx()
        ax2.bar(label,[len(i) for i in toxicities], width=0.35, edgecolor="white", linewidth=0.7, color="coral",zorder=0)
        ax2.set_ylabel("Score Frequency")
        axis[0, 0].plot(label,[np.mean(i) for i in toxicities], zorder=5)
        axis[0, 0].set_title("Toxicity to Score")
        axis[0, 0].set_ylabel(" mean toxicity")
        x = [np.mean(i) for i in toxicities]
        mini = np.min(x) - (np.std(x)*4)
        maxi = np.max(x) + (np.std(x))
        axis[0, 0].set_ylim(ymin=mini, ymax=maxi)

        axis[0, 1].plot(label,[np.mean(i) for i in toxic_fraction])
        axis[0, 1].set_title("Toxic Fraction to Score")
        axis[0, 1].set_ylabel("mean toxic fraction")
        x = [np.mean(i) for i in toxic_fraction]
        mini = np.min(x) - (np.std(x)*4)
        maxi = np.max(x) + (np.std(x))
        axis[0, 1].set_ylim(ymin=mini, ymax=maxi)

        axis[1, 0].boxplot(toxicities, notch=False, patch_artist=True, vert=True, labels=label, showfliers=False)
        axis[1, 0].set_ylabel("median toxicity")
        axis[1, 0].set_xlabel("score")

        axis[1, 1].boxplot(toxic_fraction, notch=False, patch_artist=True, vert=True, labels=label, showfliers=False)
        axis[1, 1].set_ylabel("median toxic fraction")
        axis[1, 1].set_xlabel("score")

        
        plt.suptitle(f"{file.capitalize()} KGQA Results")
        plt.show()

    def display_linkp_results(self, file):
        with open(f"Link_Prediction/{file}_results.json", "r") as f:
            data = json.load(f)
        figure, axis = plt.subplots(2, 2)
        toxicities = [[],[],[],[],[],[]]
        toxic_fraction = [[],[],[],[],[],[]]
        for item in data:
            toxicities[item["score"]].append(np.median(item["toxicities"]))
            toxic_fraction[item["score"]].append(np.median(item["toxic_fractions"]))

        label = list(range(0,6))
        ax2 = axis[0, 0].twinx()
        ax2.bar(label,[len(i) for i in toxicities], width=0.35, edgecolor="white", linewidth=0.7, color="coral",zorder=0)
        ax2.set_ylabel("Score Frequency")
        axis[0, 0].plot(label,[np.mean(i) for i in toxicities], zorder=5)
        axis[0, 0].set_title("Toxicity to Score")
        axis[0, 0].set_ylabel("mean toxicity")
        x = [np.mean(i) for i in toxicities]
        mini = np.min(x) - (np.std(x)*4)
        maxi = np.max(x) + (np.std(x))
        axis[0, 0].set_ylim(ymin=mini, ymax=maxi)

        axis[0, 1].plot(label,[np.mean(i) for i in toxic_fraction])
        axis[0, 1].set_title("Toxic Fraction to Score")
        axis[0, 1].set_ylabel("mean toxic fraction")
        x = [np.mean(i) for i in toxic_fraction]
        mini = np.min(x) - (np.std(x)*4)
        maxi = np.max(x) + (np.std(x))
        axis[0, 1].set_ylim(ymin=mini, ymax=maxi)

        axis[1, 0].boxplot(toxicities, notch=False, patch_artist=True, vert=True, labels=label, showfliers=False)
        axis[1, 0].set_ylabel("median toxicity")
        axis[1, 0].set_xlabel("score")

        axis[1, 1].boxplot(toxic_fraction, notch=False, patch_artist=True, vert=True, labels=label, showfliers=False)
        axis[1, 1].set_ylabel("median toxic fraction")
        axis[1, 1].set_xlabel("score")

        
        plt.suptitle(f"{file.capitalize()} Link Prediction Results")
        plt.show()