

import pandas as pd
import numpy as np

data = pd.read_csv('q5.csv')
prior = [0.1, 0.3, 0.5, 0.8]


for prior_val in prior:
    print("For P(Ho) = ",prior_val," the hypotheses selected are::", end = " ")
    for cols in data:
        sum_w = np.sum(data[cols].values)
        log_val = np.log(prior_val/(1 - prior_val))
        if sum_w < log_val:
            res = 0
        else:
            res = 1
        print(res, end = " ")
    print(" ")

