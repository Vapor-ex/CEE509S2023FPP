import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import genextreme as gev
import math
import ast
from util import *
from component import *
from analysis import *
from solve import *
from baseline import *

if __name__ == '__main__':
    SLR_1 = np.genfromtxt('SLR_1.dat',
                     dtype=None,
                     delimiter=' ')
    SLR_2 = np.genfromtxt('SLR_2.dat',
                     dtype=None,
                     delimiter=' ')
    SLR_3 = np.genfromtxt('SLR_3.dat',
                     dtype=None,
                     delimiter=' ')
    loss_val = np.genfromtxt('loss_val.dat',
                     dtype=None,
                     delimiter=' ')

    d = 0.03 # Discounting Rate

    # Initialize result DataFrame
    result = {
        'Optimal Height': [],
        'Optimal Value': [],
        'Scenario': []
    }
    result = pd.DataFrame(result)

    baseline_n1 = {
    'Optimal Height': [],
    'Optimal Value': [],
    'Scenario': []
    }
    baseline_n1 = pd.DataFrame(baseline_n1)

    baseline_nN = {
    'Optimal Height': [],
    'Optimal Value': [],
    'Scenario': []
    }
    baseline_nN = pd.DataFrame(baseline_nN)

    for i in np.arange(1500):
        j = i//500
        if j == 0:
            SLR = SLR_1[i%500]
        elif j == 1:
            SLR = SLR_2[i%500]
        elif j == 2:
            SLR = SLR_3[i%500]

        hL_star, n_star, val_star = solve_RL(7,SLR,loss_val,d,start_year=2030)
        hL = get_opt_all(hL_star,n_star)
        result_i = [hL,val_star,j+1]
        result.loc[i] = result_i

        hL_star, n_star, val_star = solve_RL_n1(7,SLR,loss_val,d,start_year=2030)
        hL = get_opt_all(hL_star,n_star)
        result_i = [hL,val_star,j+1]
        baseline_n1.loc[i] = result_i

        hL_star, n_star, val_star = solve_RL_nN(7,SLR,loss_val,d,start_year=2030)
        hL = get_opt_all(hL_star,n_star)
        result_i = [hL,val_star,j+1]
        baseline_nN.loc[i] = result_i

        if i % 10 ==0:
            print(f'Progress: {i} of 1500')

    result.to_csv('result.csv')
    baseline_n1.to_csv('n1.csv')
    baseline_nN.to_csv('nN.csv')
