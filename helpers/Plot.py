import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
from scipy import stats

class Plot:

    def __init__(self):
        self.colours = {
            "male": "blue",
            "female": "green",
            "trans": "orange",
            "high_income": "hotpink",
            "low_income": "red"
        }
 
    def plot_toxicity_to_fraction(self,file):
        """
            Plots Scatter Graph for one category
            x axis: toxicity
            y axis: toxic fraction
        """
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
        plt.ylim(0,0.3)
        plt.title(f'{file.capitalize()} Toxicity to Toxic Fraction')
        plt.grid()
        plt.show()


    def plot_toxicity_to_sentiments(self,files):
        """
            Plots Scatter Graph for multiple categories
            x axis: toxicity
            y axis: sentiment
        """
        for file in files:
            with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
                data = json.load(f)
            x = []
            y = []
            for item in data:
                x.append(sum(item["toxic_fraction"])/5)
                y.append(item["sentiment"])
            plt.scatter(x, y, c=self.colours[file], s = 4)
        plt.xlabel('toxicity')
        plt.ylabel('sentiment')
        plt.title(f'All Triples Toxicity to Sentiment')
        plt.grid()
        plt.show()

    def box_plot(self,files):
        """
            Plots Horizontal Box plots of multiple categories
            x axis: toxicity
            y axis: each file toxicity and toxic fraction
        """
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

        plt.show()

    def plot_3d(self,file):
        """
            Plots 3D Scatter Graph for one category
            x axis: toxicity
            y axis: toxic_fraction
            z axis: sentiment
        """
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
        """
            Prints to terminal toxicity and toxic fraction; mean, median, mode and standard deviation
        """
        with open(f"toxicity_results/5000_{file}_toxicities.json", "r") as f:
            data = json.load(f)

        toxicity_values = [i["toxicity"] for i in data]
        fraction_values = [sum(x["toxic_fraction"])/5 for x in data]

        fraction_mean = sum(fraction_values) /len(fraction_values)
        fraction_median = np.median(fraction_values)
        fraction_sd = pd.Series(fraction_values).std()
        fraction_mode = max(fraction_values)

        mean = sum(toxicity_values) / len(toxicity_values)
        median = np.median(toxicity_values)
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
        """
            Plots 4 graphs boxplot, line graphs and box plots for multiple categories
        """
        figure, axis = plt.subplots(2, 2)
        toxicities = [[],[],[],[],[],[]]
        toxic_fraction = [[],[],[],[],[],[]]
        for file in files:
            with open(f"KGQA/{file}_q_a.json", "r") as f:
                data = json.load(f)
            for item in data:
                toxicities[item["score"]].append(np.mean(item["toxicities"]))
                toxic_fraction[item["score"]].append(np.mean(item["toxic_fraction"]))
        
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
    
    def display_all_linkp_results(self, files):
        """
            Plots 4 graphs boxplot, line graphs and box plots for multiple categories
        """
        figure, axis = plt.subplots(2, 2)
        toxicities = [[],[],[],[],[],[]]
        toxic_fraction = [[],[],[],[],[],[]]
        for file in files:
            with open(f"Link_Prediction/{file}_results.json", "r") as f:
                data = json.load(f)
            for item in data:
                toxicities[item["score"]].append(np.mean(item["toxicities"]))
                toxic_fraction[item["score"]].append(np.mean(item["toxic_fractions"]))

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
        """
            Plots 4 graphs boxplot, line graphs and box plots for one category
        """
        with open(f"KGQA/{file}_q_a.json", "r") as f:
            data = json.load(f)
        figure, axis = plt.subplots(2, 2)
        toxicities = [[],[],[],[],[],[]]
        toxic_fraction = [[],[],[],[],[],[]]
        for item in data:
            toxicities[item["score"]].append(np.mean(item["toxicities"]))
            toxic_fraction[item["score"]].append(np.mean(item["toxic_fraction"]))

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
        """
            Plots 4 graphs boxplot, line graphs and box plots for one category
        """
        with open(f"Link_Prediction/{file}_results.json", "r") as f:
            data = json.load(f)
        figure, axis = plt.subplots(2, 2)
        toxicities = [[],[],[],[],[],[]]
        toxic_fraction = [[],[],[],[],[],[]]
        for item in data:
            toxicities[item["score"]].append(np.mean(item["toxicities"]))
            toxic_fraction[item["score"]].append(np.mean(item["toxic_fractions"]))

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


    def plot_kgqa_results(self, files):
        """
            Plots KGQA Results
            Line chart of mean toxicities or toxic fractions for multiple categories
        """
        for file in files:
            with open(f"KGQA/{file}_q_a.json", "r") as f:
                data = json.load(f)
            toxicities = [[],[],[],[],[],[]]
            toxic_fraction = [[],[],[],[],[],[]]
            for item in data:
                toxicities[item["score"]].append(np.mean(item["toxicities"]))
                toxic_fraction[item["score"]].append(np.mean(item["toxic_fraction"]))

            plt.plot(list(range(0,6)),[len(i) for i in toxicities])
            # plt.plot(list(range(0,6)),[np.median(i) for i in toxic_fraction])
        plt.xlabel('score')
        plt.ylabel('toxicity')
        plt.title(f'Toxic Fraction to Score')
        plt.grid()
        plt.legend(files)
        plt.show()
    
    def plot_linkp_results(self, files):
        """
            Plots Link Prediction Results
            Line chart of mean toxicities or toxic fractions for multiple categories
        """
        for file in files:
            with open(f"Link_Prediction/{file}_results.json", "r") as f:
                data = json.load(f)
            toxicities = [[],[],[],[],[],[]]
            toxic_fraction = [[],[],[],[],[],[]]
            for item in data:
                toxicities[item["score"]].append(np.mean(item["toxicities"]))
                toxic_fraction[item["score"]].append(np.mean(item["toxic_fractions"]))

            plt.plot(list(range(0,6)),[np.median(i) for i in toxicities])
            # plt.plot(list(range(0,6)),[np.median(i) for i in toxic_fraction])
        plt.xlabel('score')
        plt.ylabel('toxicity')
        plt.title(f'Link Prediction Toxicity to Score')
        plt.grid()
        plt.legend(files)
        plt.show()
    
    def plot_bar_chart(self,files):
        """
            Plots KGQA Score Frequency of 'sex or gender' predicate
        """
        dictionary = dict()
        dictionary["score"]= list(range(0,6))
        for file in files:
            with open(f"KGQA/{file}_q_a.json", "r") as f:
                data = json.load(f)
            toxic_fractions = [[],[],[],[],[],[]]
            for item in data:
                if "sex" in item["question"] or "gender" in item["question"] or "aromantic" in item["answer"]:
                    toxic_fractions[item["score"]].append(np.mean(item["toxicities"]))
            dictionary[file]=[len(i) for i in toxic_fractions]
        
        df = pd.DataFrame(dictionary)
        df.plot(x="score", y=files, kind="bar")
        plt.ylabel("frequency")
        plt.show()
    

    def calculate_gradient(self,files):
        """
            Linear Regression combining KGQA, Link Prediction
            Line Graph for toxicity and toxic fraction
            Prints Gradient in terminal
        """
        x_data = list(range(2,6))
        toxicities = [[],[],[],[],[],[]]
        toxic_fraction = [[],[],[],[],[],[]]
        complete=[]
        for file in files:
            with open(f"Link_Prediction/{file}_results.json", "r") as f:
                data = json.load(f)
            for item in data:
                toxicities[item["score"]].append(np.mean(item["toxicities"]))
                toxic_fraction[item["score"]].append(np.mean(item["toxic_fractions"]))
                toxic_fraction[item["score"]].append(np.mean(item["toxic_fractions"]))
            with open(f"KGQA/{file}_q_a.json", "r") as f:
                data = json.load(f)
            for item in data:
                toxicities[item["score"]].append(np.mean(item["toxicities"]))
                toxic_fraction[item["score"]].append(np.mean(item["toxic_fraction"]))
        complete.append((x_data,[np.mean(i) for i in toxicities[2:]]))
        complete.append((x_data,[np.mean(i) for i in toxic_fraction[2:]]))

        for x_data, y_data in complete:
            m, b = np.polyfit(x_data, y_data, 1)

            x_fit = np.linspace(min(x_data), max(x_data), 100)

            y_fit = m * x_fit + b
            print(f"Slope (m): {m}, Y-intercept (b): {b}")
            # plt.plot(x_data, y_data, 'o', label='Original Data')
            plt.plot(x_fit, y_fit, '-', label='Line of Best Fit')
            plt.xlabel('Score')
            plt.ylabel('Toxicity')
            plt.title('Line of Best Fit')
            plt.legend(["Toxicity","Toxic Fraction"])
        plt.show()
        print(f"Slope (m): {m}, Y-intercept (b): {b}")