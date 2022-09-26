from genericpath import exists
from os import makedirs
import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

column_names = ["Hogwarts House", "Arithmancy", "Astronomy","Herbology","Defense Against the Dark Arts", \
    "Divination","Muggle Studies", "Ancient Runes","History of Magic","Transfiguration","Potions", \
    "Care of Magical Creatures","Charms","Flying"]
houses = ["Ravenclaw", "Gryffindor", "Slytherin", "Hufflepuff"]
colors = ["y", "r", "g", "b"]
feauture_list = column_names[1:]

def main():
    if exists("./scatter_plot/") == False: 
        makedirs("./scatter_plot/")
    for feauture_1 in feauture_list:
        for feauture_2 in feauture_list:
            if (feauture_1 != feauture_2):
                if exists("./scatter_plot/{0}_{1}_scatter.png".format(feauture_1, feauture_2)) == False and \
                exists("./scatter_plot/{0}_{1}_scatter.png".format(feauture_2, feauture_1)) == False:
                    for house in houses:
                        fd = pd.read_csv("./describe/house_marks/{0}_marks.csv".format(house))
                        i = houses.index(house)
                        x = fd[feauture_1]
                        y = fd[feauture_2]
                        sns.scatterplot(x=x, y=y, color=colors[i], label=house)
                    plt.savefig("./scatter_plot/{0}_{1}_scatter.png".format(feauture_1, feauture_2))
                    plt.close()

if __name__ == '__main__':
    sys.exit(main())
