import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from util import save_data

if __name__ == '__main__':

    # Load SLR genration parameter for 2000 to 2100
    SLR_par = pd.read_csv('SLR.csv')
    SLR_1 = np.zeros((500,10))
    SLR_2 = np.zeros((500,10))
    SLR_3 = np.zeros((500,10))

    # Generate 500 realizations of SLR from 2000 to 2100 for each scenario
    h = np.arange(2000,2100,10)
    for n in np.arange(500):
        for i in np.arange(10):
            SLR_1i = np.random.normal(SLR_par['mean_1'][i*10],SLR_par['sd_1'][i*10])*0.0328084 # From cm to feet
            SLR_2i = np.random.normal(SLR_par['mean_2'][i*10],SLR_par['sd_2'][i*10])*0.0328084
            SLR_3i = np.random.normal(SLR_par['mean_3'][i*10],SLR_par['sd_3'][i*10])*0.0328084
            SLR_1[n,i] = SLR_1i
            SLR_2[n,i] = SLR_2i
            SLR_3[n,i] = SLR_3i

    save_data('SLR_1.dat',SLR_1)
    save_data('SLR_2.dat',SLR_2)
    save_data('SLR_3.dat',SLR_3)
