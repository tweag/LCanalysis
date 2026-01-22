#!/usr/bin/python

import csv
from frozendict import frozendict
from glob import glob

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
    pass
    
if __name__ == "__main__":
    main()
