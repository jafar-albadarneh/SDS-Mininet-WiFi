#!/usr/bin/python

import os


def main():
    keys = []
    valuesArray = []
    directory = "c1"

    """ Reading Input Files """
    for filename in os.listdir(directory):
        if filename.endswith(".dat"):
            # print(os.path.join(directory, filename))
            results = {}
            with open(os.path.join(directory, filename)) as infile:
                lines = infile.readlines()
                for line in lines[24:-1]:
                    key, value = processLine(line)
                    results[key] = value

            keys = results.keys()
            valuesArray.append(results.values())

    """ write results to file """
    with open(os.path.join(directory, "%s.csv" % directory), "w") as outFile:
        for k in keys:
            outFile.write("%s," % k)
        outFile.write("\n")
        for values in valuesArray:
            for v in values:
                outFile.write("%s," % v)
            outFile.write("\n")


def processLine(line):
    """ extract results from line"""
    results = line.split('=')
    return results[0].strip(), float(results[1].split()[0])


if __name__ == "__main__":
    main()
