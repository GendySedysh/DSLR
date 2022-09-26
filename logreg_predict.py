import pandas as pd
import numpy as np
import sys
from sklearn.metrics import accuracy_score

def predict(X, w, K):
    X = np.insert(X, 0, 1, axis=1)
    predictions = net_input(X, w).T
    return [K[x] for x in predictions.argmax(1)]

def sigmoid(z):
    g = 1.0 / (1.0 + np.exp(-z))
    return g

def net_input(X, w):
    return sigmoid(w.dot(X.T))

def main():
    columns = ['Defense Against the Dark Arts', 'Charms', 'Herbology', 'Divination', 'Muggle Studies']

    if len(sys.argv) != 3:
        print("Usage: python.exe .\logreg_predict.py test_dataset weights")
        exit(0)
    else:
        try:
            with open(sys.argv[1], 'r') as fd:
                fd.close()
        except IOError:
            print("Can't open dataset file")
            exit(0)
        try:
            with open(sys.argv[2], 'r') as fd:
                fd.close()
        except IOError:
            print("Can't open weights file")
            exit(0)
    df = pd.read_csv(sys.argv[1], usecols=columns)[columns]
    weigths = pd.read_csv(sys.argv[2], usecols=[1,2,3,4,5,6]).values

    line, col = df.shape
    try:
        with open("./describe/describe.csv", 'r') as fd:
            fd.close()
    except IOError:
        print("describe.csv is not found")
        exit(0)
    std_df = pd.read_csv("./describe/describe.csv", usecols=columns)[columns]
    mean_df = std_df.iloc[1]
    std_df = std_df.iloc[2]

    for feat in columns:
        df[feat].fillna(value=mean_df[feat], inplace=True)

    for i in range(line):
        for feat in columns:
            x = df.at[i, feat]
            df.at[i, feat] = (x - mean_df[feat]) / std_df[feat]

    X = df.values
    K = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']

    y_predict = predict(X, weigths, K)
    df = pd.DataFrame(y_predict, columns=["Hogwarts House"])
    df.to_csv("houses.csv")

if __name__ == "__main__" :
    main()