from helpers.CalculateMetrics import toxicity_metric, sentiment_metric
from helpers.KGQA import KGQA
from helpers.LinkPrediction import LinkPrediction
from helpers.Plot import Plot
from helpers.ToxicFraction import ToxicFraction
from helpers.WikiVerbalise import WikiVerbalise

files = ["male","female", "trans", "high_income", "low_income"]

"""
    It's advisable to comment each section separately and excute one at a time,
    than running the entire process all at once.
"""

########## For calculating metrics: toxicity, sentiment, toxic fraction #########
for file in files:
    WikiVerbalise.verbalise(file) #verbalises the triples
    toxicity_metric(file) # calculates the toxicity score
    sentiment_metric(file) # calculates the sentiment score
    tf = ToxicFraction()
    tf.run(file) # caluculates the toxic fraction scores


######### Visualising metrics ###########
plotter = Plot()
plotter.box_plot(files) # places all files in one box plot
for file in files:
    plotter.plot_3d(file) # plots a 3d scatter graph of toxicity against the toxic fraction against the sentiment

    plotter.display_metrics(file) # prints mean, median, mode and standard deviation

    plotter.plot_toxicity_to_fraction(file) # plots a scatter graph of toxicity against the toxic fraction
    



######## For processing downstream tasks #########
kgqa = KGQA()
link_pred = LinkPrediction()
for file in files:
    print(file.upper())
    print("starting kgqa set up")
    kgqa.context_set_up(file,200,6) #creates 200 questions with a context budget of 6

    print("starting kgqa answer")
    kgqa.answer(file) #calls on the language models to answer the questions

    print("starting link prediction set up")
    link_pred.context_set_up(file, 200,10) # creates 200 question with a context budget of 10

    print("starting link prection answer")
    link_pred.answer(file) # calls on the language models to complete the tasks


########## Visualising downstream task performance ##########
### Many more charts and graphs available in Plot Class
plotter = Plot()
plotter.plot_kgqa_results(files) #plots line graphs of kgqa results of all files

plotter.plot_bar_chart(files) # plots line graphs of link prediction results of all files

plotter.display_kgqa_results("trans") # plots 4 graphs depicting kgqa results of a specific file

plotter.display_all_linkp_results(files) # plots 4 graphs depicting cummulative kgqa results of a all files

plotter.calculate_gradient(files) # performs linear regression and plots line of best fit

plotter.box_plot(files) # creats toxicity and toxic fractionboxplot of all files

