import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import genextreme as gev
import math
from util import *
from component import *
from analysis import *
from solve import *

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
    result = {
        'Optimal Height': [],
        'Optimal Horizon': [],
        'Optimal Value': [],
        'Scenario': []
    }
    result = pd.DataFrame(result)
    for i in np.arange(1500):
        j = i//500
        if j == 0:
            SLR = SLR_1[i%500]
        elif j == 1:
            SLR = SLR_2[i%500]
        elif j == 2:
            SLR = SLR_3[i%500]
        hL_star, n_star, val_star = solve_RL(7,SLR,loss_val,d,start_year=2030)
        result_i = [hL_star,n_star,val_star,j+1]
        result.loc[i] = result_i
