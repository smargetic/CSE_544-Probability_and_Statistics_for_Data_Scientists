import math
import argparse
import statistics
import numpy as np
import pandas as pd
import csv

with open("q2_sigma3.dat", "r") as myfile:
    priorMean=0
    priorVariance=1
    newMean=0
    newVariance=0
    givenSigmaSquare=9
    n=100
    seSquare=givenSigmaSquare/n
    for line in myfile:
        total=0
        expectedMean=0
        currentline = line.split(",")
        for value in currentline:
            total+=float(value)
        expectedMean=total/n
        newMean=(priorVariance*expectedMean+seSquare*priorMean)/(priorVariance+seSquare)
        newVariance=(priorVariance*seSquare)/(priorVariance+seSquare)
        print("New mean: ",  newMean, " New Variance: ", newVariance)
        priorMean=newMean
        priorVariance=newVariance
        print("\n")  