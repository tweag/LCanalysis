import csv
from frozendict import frozendict
from glob import glob
import numpy as np
from sklearn.linear_model import LinearRegression

def filter_data(data, alpha = None, delta = None, K = None):
    result = {}
    for (old_key,v) in data.items():
        new_key = {}

        if alpha is None:
            new_key["alpha"] = old_key["alpha"]
        elif old_key["alpha"] != alpha:
            continue

        if delta is None:
            new_key["delta"] = old_key["delta"]
        elif old_key["delta"] != delta:
            continue

        if K is None:
            new_key["K"] = old_key["K"]
        elif old_key["K"] != K:
            continue

        result[frozendict(new_key)] = v

    return result

def build_data():
    data = {}
    for filename in glob("../results/*.csv"):
        with open(filename) as csvfile:
            for line in csv.DictReader(csvfile):
                line = {k: float(v) for (k, v) in line.items()}
                errorUB = line.pop("errorUB")
                data[frozendict(line)] = errorUB
    return data

def main():
    data = build_data()
    filtered = filter_data(data, alpha = 0.90, delta = 2)

    inputs = np.array([])
    outputs = np.array([])
    for (k,v) in filtered.items():
        input = k["K"]
        output = np.log(v) # I suspect the log of the upper bound is linear
        # strange behavior for K = 1; the paper starts with K = 2
        if input == 1:
            continue
        inputs = np.append(inputs, input)
        outputs = np.append(outputs, output)
    inputs = inputs.reshape((-1, 1))

    model = LinearRegression().fit(inputs, outputs)
    r_sq = model.score(inputs, outputs)

    print(f"r_sq: {r_sq}\nintercept: {model.intercept_}\nslope: {model.coef_}")
    
if __name__ == "__main__":
    main()
