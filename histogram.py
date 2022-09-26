from genericpath import exists
from os import makedirs
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

column_names = ["Best Hand","Arithmancy", "Astronomy","Herbology","Defense Against the Dark Arts", \
    "Divination","Muggle Studies", "Ancient Runes","History of Magic","Transfiguration","Potions", \
    "Care of Magical Creatures","Charms","Flying"]
houses = ["Ravenclaw", "Gryffindor", "Slytherin", "Hufflepuff"]
metrics = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]

features_in_houses = {}     # {house, {feature, [metics]}}
for house in houses:
    df = pd.read_csv("./describe/houses/{0}_features.csv".format(house), names=column_names)
    metrics_in_features = {}
    for i in range(len(column_names)):
        metrics_in_features[column_names[i]] = df[column_names[i]].to_list()
        metrics_in_features[column_names[i]].pop(0)
    features_in_houses[house] = metrics_in_features

dataframes = []
for house in houses:
    data = []
    names = []
    for i in column_names:
        names.append(i)
    for i in range(len(column_names)):
        tmp = []
        for j in range(len(metrics)):
            tmp.append(features_in_houses[house][column_names[i]][j])
        data.append(tmp)
    df = pd.DataFrame(data, index=names, columns=metrics) #pd.DataFrame(data, index=names, columns=metrics)
    dataframes.append(df)

def create_list_of_metric_feauture(metric, feauture_name):
    out_list = []
    for i in range(len(houses)):
        out_list.append(float(dataframes[i][metric][feauture_name]))
    return out_list

def show_dataframe_of_feauture(std_feauture, mean_feauture):
    data = []
    data.append(std_feauture)
    data.append(mean_feauture)
    df = pd.DataFrame(data, index=["Std", "Mean"], columns=houses)
    print(df)


def main():
    x = np.arange(len(houses))
    width=0.4

    if exists("./histogram/") == False: 
        makedirs("./histogram/")
    if exists("./histogram/graphs/") == False: 
        makedirs("./histogram/graphs/")
        for feauture in column_names:
            fig, ax = plt.subplots()
            std_feauture = create_list_of_metric_feauture("Std", feauture)
            mean_feauture = create_list_of_metric_feauture("Mean", feauture)
            bar1 = ax.bar(x - width/2, height=std_feauture, width=width, label='Std of {0}'.format(feauture))
            bar2 = ax.bar(x + width/2, height=mean_feauture, width=width, label='Mean of {0}'.format(feauture))
            ax.set_xticks(x)
            ax.set_xticklabels(houses)
            plt.title(feauture)
            plt.savefig("./histogram/graphs/{0}_std_mean.jpg".format(feauture))
            plt.close()
    if exists("./histogram/histograms/") == False: 
        makedirs("./histogram/histograms/")
        for feauture in column_names:
            df = pd.read_csv("./describe/features/{0}.csv".format(feauture))
            df.drop("Unnamed: 0", inplace=True, axis=1)
            sns.displot(df)
            plt.title(feauture)
            plt.savefig("./histogram/histograms/{0}_histogram.jpg".format(feauture))
            plt.close()

if __name__ == '__main__':
    sys.exit(main())