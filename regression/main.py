import csv
from frozendict import frozendict
from glob import glob
import numpy as np
from sklearn.linear_model import LinearRegression
from pprint import pprint

# Filter input data according to the given alpha, delta, and K values.
# Remove the specified keys from the output data.
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

# Aggregate data from various *.csv output files
def build_data():
    data = {}
    for filename in glob("../results/*.csv"):
        with open(filename) as csvfile:
            for line in csv.DictReader(csvfile):
                line = {k: float(v) for (k, v) in line.items()}
                if line["K"] == 1:
                    # strange behavior for K = 1; the paper starts with K = 2
                    continue
                errorUB = line.pop("errorUB")
                data[frozendict(line)] = errorUB
    return data

# Enumerate all values in input data for alpha, delta, and K parameters
def parameter_values(data):
    values = {"alpha": set(), "delta": set(), "K": set()}
    for params in data.keys():
        for (param, value) in params.items():
            values[param].add(value)
    return values

# Enumerate all possible values for pairs of parameters in {alpha, delta, K}
def parameter_pairs(parameter_values):
    pairs = []
    params = list(parameter_values.keys())
    for i in range(len(params)):
        for j in range(i+1, len(params)):
            param1 = params[i]
            param2 = params[j]
            for val1 in parameter_values[param1]:
                for val2 in parameter_values[param2]:
                    pairs.append({param1: val1, param2: val2})
    return pairs

# Interpolate the data to find suspected linear coefficients.
# I suspect the formula looks is close to:
#   errorUB(alpha,delta,K) = f(alpha) * g(delta) * e^{h(K)}
# With f, g, and h linear functions
def interpolate(data):
    inputs = np.array([])
    outputs = np.array([])
    for (k,v) in data.items():
        if len(k) != 1:
            raise Exception("filtered parameter should only have one key: " + str(k))
        param = list(k.keys())[0]
        if param == "K":
            v = np.log(v)
        inputs = np.append(inputs, k[param])
        outputs = np.append(outputs, v)
    inputs = inputs.reshape((-1, 1))

    model = LinearRegression().fit(inputs, outputs)
    r_sq = model.score(inputs, outputs)

    return (r_sq, model.intercept_, model.coef_[0])

def main():
    data = build_data()
    param_values = parameter_values(data)
    param_pairs = parameter_pairs(param_values)

    with open("interpolation_results.csv", "w") as output_file:
        output_fields = [
            "param1",
            "param1_value",
            "param2",
            "param2_value",
            "data_points",
            "r_squared",
            "intercept",
            "slope",
        ]
        writer = csv.DictWriter(output_file, output_fields)
        writer.writeheader()
        for param_pair in param_pairs:
            filtered = filter_data(data, **param_pair)
            l = len(filtered)
            if l == 0:
                continue
            param1 = list(param_pair.keys())[0]
            param2 = list(param_pair.keys())[1]
            result = {
                "param1": param1,
                "param1_value": param_pair[param1],
                "param2": param2,
                "param2_value": param_pair[param2],
                "data_points": l,
            }
            (r_squared, intercept, slope) = interpolate(filtered)
            result.update({
                "r_squared":r_squared,
                "intercept":intercept,
                "slope":slope,
            })
            writer.writerow(result)
            output_file.flush()

if __name__ == "__main__":
    main()
