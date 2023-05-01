import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from component import Building, Region
from util import save_data

if __name__ == '__main__':

    # Load NYC Building Database
    df1 = pd.read_csv('nybuilding.csv')
    df2 = pd.read_csv('pluto.csv')
    df2 = df2.rename(columns={'bbl': 'BBL'})
    df2['BBL'] = df2['BBL'].astype('int64')
    df = pd.merge(df1, df2, on='BBL', how='left')
    df = df.loc[:,~df.columns.duplicated()]

    bldg = {}
    for index, row in df.iterrows():
        resarea = row['resarea']
        height = row['HEIGHT_ROO']
        elev = row['GROUND_ELE']
        cat = row['bldgclass']
        building = Building(resarea,height,elev,cat)
        bldg[index]=building

    reg = Region(bldg)

    # Estimate the value loss for the region given flood height h
    loss_val = []
    for h in np.arange(0,50,0.1):
        loss_h = reg.loss_estim(h)
        loss_val.append(loss_h)

    save_data(f"loss_val.dat", loss_val)
