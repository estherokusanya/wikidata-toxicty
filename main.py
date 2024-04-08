from helpers.CalculateMetrics import toxicity_metric, sentiment_metric
from helpers.KGQA import KGQA
from helpers.LinkPrediction import LinkPrediction
from helpers.Plot import Plot
from helpers.ToxicFraction import ToxicFraction
from helpers.WikiVerbalise import WikiVerbalise

files = ["male","female", "trans", "high_income", "low_income"]

########## For calculating metrics: toxicity, sentiment, toxic fraction #########
# for file in files:
#     WikiVerbalise.verbalise(file)
#     toxicity_metric(file)
#     sentiment_metric(file)
#     tf = ToxicFraction()
#     tf.run(file)


######### Visualising metrics ###########
# plotter = Plot()
# plotter.box_plot(files)
# for file in files:
#     plotter.plot_3d(file)
    # plotter.display_metrics(file)
    # plotter.plot_toxicity_to_fraction(file)
    


######## For processing downstream tasks #########
# kgqa = KGQA()
# link_pred = LinkPrediction()
# for file in files:
    # print(file.upper())
    # print("starting kgqa set up")
    # kgqa.context_set_up(file,200,6)
    # print("starting kgqa answer")
    # kgqa.answer(file)
    # print("starting link prediction set up")
    # link_pred.context_set_up(file, 200,10)
    # print("starting link prection answer")
    # link_pred.answer(file)


########## Visualising downstream task performance ##########
plotter = Plot()
plotter.display_all_linkp_results(["male","female","trans", "low_income", "high_income"])
# plotter.display_all_linkp_results(files)
# plotter.plot_downstream_kgqa_toxicity("trans")
# plotter.display_kgqa_results("low_income")

