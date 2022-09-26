import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sys

def predict(X, _w, _K):
    X = np.insert(X, 0, 1, axis=1)
    predictions = net_input(X, _w).T
    return [_K[x] for x in predictions.argmax(1)]

def sigmoid(z):
    g = 1.0 / (1.0 + np.exp(-z))
    return g

def net_input(X, _w):
    return sigmoid(_w.dot(X.T))

def train(X, y, sample_weight=None):
    max_iter = 100
    Lambda = 0
    eta = 0.1
    cost_list = []
    errors = []
    w_list = []

    K = np.unique(y).tolist()
    newX = np.insert(X, 0, 1, axis=1)
    m = newX.shape[0]

    w = sample_weight
    if not w:
        w = np.zeros(newX.shape[1] * len(K))
    w = w.reshape(len(K), newX.shape[1])

    yVec = np.zeros((len(y), len(K)))
    for i in range(0, len(y)):
        yVec[i, K.index(y[i])] = 1

    for j in range(0, max_iter):
        predictions = net_input(newX, w).T

        lhs = yVec.T.dot(np.log(predictions))
        rhs = (1 - yVec).T.dot(np.log(1 - predictions))

        r1 = (Lambda / (2 * m)) * sum(sum(w[:, 1:] ** 2))
        cost = (-1 / m) * sum(lhs + rhs) + r1
        cost_list.append(cost)
        errors.append(sum(y != predict(X, w, K)))

        r2 = (Lambda / m) * w[:, 1:]
        w = w - (eta * (1 / m) * (predictions - yVec).T.dot(newX) + np.insert(r2, 0, 0, axis=1))
        w_list.append(w)
    return w, cost_list, errors, K, w_list

def main():   
    # INIT DATASET
    columns = ['Defense Against the Dark Arts', 'Charms', 'Herbology', 'Divination', 'Muggle Studies', "Hogwarts House"]
    features = columns[:5]

    if len(sys.argv) != 2:
        print("Usage: python.exe .\logreg_train.py train_dataset")
        exit(0)
    else:
        try:
            with open(sys.argv[1], 'r') as fd:
                fd.close()
        except IOError:
            print("Can't open dataset file")
            exit(0)
    df = pd.read_csv(sys.argv[1], usecols=columns)[columns]

    # HERE WE TRY TO DELETE NaN FROM DATASET
    df = df.dropna()
    df = df.reset_index(drop=True)
    line, col = df.shape

    # STANDARTIZE DATA
    try:
        with open("./describe/describe.csv", 'r') as fd:
            fd.close()
    except IOError:
        print("describe.csv is not found")
        exit(0)
    std_df = pd.read_csv("./describe/describe.csv", usecols=features)[features]
    mean_df = std_df.iloc[1]
    std_df = std_df.iloc[2]

    for i in range(line):
        for feat in features:
            x = df.at[i, feat]
            df.at[i, feat] = (x - mean_df[feat]) / std_df[feat]

    # MAKE DATA
    X = df.iloc[:,:-1].values       # INPUT DATA
    Y = df.iloc[:,-1:].values       # OTPUT DATA

    # SPLITTING DATA
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 1/4, random_state = 0 )

    # TRAINING
    weights, cost, errors, K, _w_list = train(X_train, Y_train)

    # ACCURACY TEST
    y_predict = predict(X_test, weights, K)
    acc = accuracy_score(Y_test, y_predict) * 100
    print("Test data")
    print("Accuracy: {}%".format(acc))

    y_predict = predict(X, weights, K)
    acc = accuracy_score(Y, y_predict) * 100
    print("Full data")
    print("Accuracy: {}%".format(acc))

    data = pd.DataFrame(weights)
    data.to_csv("weights.csv")

if __name__ == "__main__" :
    main()