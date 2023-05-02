import numpy as np
import math
from util import *
from analysis import *
from component import *
from solve import *

def solve_RL_n1(N,SLR,loss_val,interest,start_year=0):
    """Perform the RL algorithm taking N the total planing period, SLR the sea
    level rise realization, and interest/discounting rate to generate a sequence
    of optimal levee height increases with optimal planning horizon to be 1."""

    ci = np.ones(N,dtype='int')
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

    hL_star = h_seq
    n_star = ci
    val_star = tot_val

    return hL_star, n_star, val_star

def solve_RL_nN(N,SLR,loss_val,interest,start_year=0):
    """Perform the RL algorithm taking N the total planing period, SLR the sea
    level rise realization, and interest/discounting rate to generate a sequence
    of optimal levee height increases with optimal planning horizon to be N."""

    ci = [N]
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

    hL_star = h_seq
    n_star = ci
    val_star = tot_val

    return hL_star, n_star, val_star
