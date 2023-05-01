import numpy as np
import math
from util import *
from analysis import *
from component import *

def get_opt(curr_period,SLR,h_build_prev,loss_val,pln_horizon,interest):
    """Get the optimal selections of new seawall height."""
    h_SLR = SLR[curr_period]
    value = []
    loss_fn = []
    for i in np.arange(50):
        loss_fn.append(loss_estim(h_SLR,i,get_ss_parameter(curr_period*10+pln_horizon),loss_val))

    for h in np.arange(h_build_prev,50,1):
        value.append(tot_value_estim(h_build_prev,h,loss_fn,pln_horizon,interest)/(1+interest)**(curr_period*10))

    h_opt = value.index(max(value))
    value_opt = max(value)

    return h_opt, value_opt

def solve_RL(N,SLR,loss_val,interest,start_year=0):
    """Perform the RL algorithm taking N the total planing period, SLR the sea
    level rise realization, and interest/discounting rate to generate a sequence
    of optimal levee height increases and optimal planning horizon."""

    comb = decomp(N)
    comb_val = np.zeros(len(comb))
    comb_h = []

    for i in np.arange(len(comb)):
        ci = comb[i]
        curr_period = normal_round((start_year-2000)/10)
        h_prev = 0
        h_seq = []
        tot_val = 0

        for j in np.arange(len(ci)):
            n = ci[j]

            h_opt,value_opt = get_opt(curr_period,SLR,h_prev,loss_val,n*10,interest) # 1 period is 10 years
            curr_period += n
            h_prev += h_opt
            h_seq.append(h_prev)
            tot_val += value_opt

        comb_val[i] = tot_val
        comb_h.append(h_seq)

    hL_star = comb_h[np.argmax(comb_val)]
    n_star = comb[np.argmax(comb_val)]
    val_star = comb_val[np.argmax(comb_val)]

    return hL_star, n_star, val_star
