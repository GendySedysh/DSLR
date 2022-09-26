import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

column_names = ["Hogwarts House", "Arithmancy", "Astronomy","Herbology","Defense Against the Dark Arts", \
    "Divination","Muggle Studies", "Ancient Runes","History of Magic","Transfiguration","Potions", \
    "Care of Magical Creatures","Charms","Flying"]
houses = ["Ravenclaw", "Gryffindor", "Slytherin", "Hufflepuff"]

def main():
    df = pd.read_csv("./datasets/dataset_train.csv", usecols=column_names) #, usecols=column_names
    sns.pairplot(df, hue="Hogwarts House", markers=["o", "s", "D", "h"])
    plt.savefig("./pair_plt.png")
    plt.close()

if __name__ == '__main__':
    sys.exit(main())