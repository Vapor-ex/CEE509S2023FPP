import numpy as np
from scipy.stats import genextreme as gev
from util import *
from component import *

def get_ss_parameter(curr_year):
    """Get the storm-tide parameter given the current year."""
    shape0 = -0.48337643673799413
    shape1 = -0.4875244611560601
    loc0 = 0.16832598911170035
    loc1 = 0.18642054403373093
    scale0 = 0.12251560468745198
    scale1 = 0.13368245375059845

    shape = (shape1-shape0)/100*curr_year+shape0
    loc = (loc1-loc0)/100*curr_year+loc0
    scale = (scale1-scale0)/100*curr_year+scale0

    return [shape,loc,scale]

def loss_estim(h_SLR,h_build,par_surge,reg_loss):
    """Loss Estimation of building seawall versus taking damage for a particular
    flood height. reg_loss is a list of loss from h=0 to h=50 with step 0.1"""

    xx = np.arange(0,50,0.1)
    shape = par_surge[0]
    loc = par_surge[1]
    scale = par_surge[2]
    p_surge = gev.pdf(xx,shape,loc,scale)

    h_eff = h_SLR-h_build
    if h_eff < -50:
        damage = -reg_loss[0]
    elif h_eff < 0:
        damage = -0.1*np.dot(p_surge[normal_round(h_eff*10):],reg_loss[normal_round(h_eff*10):])
    elif h_eff == 0:
        damage = -0.1*np.dot(p_surge,reg_loss)
    elif h_eff < 50:
        damage = -0.1*np.dot(p_surge[0:500-normal_round(h_eff*10)],reg_loss[normal_round(h_eff*10):])
    else:
        damage = -reg_loss[-1]

    risk_comp = 5.5e2*abs(h_eff)**(1/3)*reg_loss[0]
    if h_eff < 0:
        damage += risk_comp

    return damage

def tot_value_estim(h_build_prev,h_build_curr,loss_fn,pln_horizon,interest):
    """Estimate the total value earned by building a new seawall height h_build_curr
    given the previous seawall height, loss function, planning horizon, and interest."""
    value_gained = 0
    for i in np.arange(pln_horizon):
        value_gained += (loss_fn[h_build_curr]-loss_fn[h_build_prev])/(1+interest)**pln_horizon
    if h_build_prev == 0:
        value_loss = build_seawall(h_build_curr-h_build_prev,initial=True)
    else:
        value_loss = build_seawall(h_build_curr-h_build_prev)
    return value_gained-value_loss
