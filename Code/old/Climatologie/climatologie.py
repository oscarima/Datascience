# -*- coding: cp1252 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

if __name__ == '__main__':
    datas = pd.read_csv("FF42.txt",sep="\t")
    #print datas.info()
    col=datas.columns.values
    col[1]="dpt"
    col[2]="serie"
    col[3]="unite"
    datas.columns =col
    datas=datas.melt(id_vars=col[0:3],value_vars=col[4:], var_name='year', value_name='nb')
    
    #datas.value=datas.value.astype(int)
    # suppprime les regions
    #datas=datas.drop(["Lieu","region"], axis=1)
    datas=datas[datas.nb!="ND"]
    datas.nb=datas.nb.astype(float)
    datas.year=datas.year.astype(int)
    print datas.info()
    print datas.describe()
    evol=datas[["year","nb"]].groupby(["year"]).sum()
    print evol
  #saisonalite
    import statsmodels.api as sm
    sm.tsa.seasonal_decompose(evol.nb,freq=11).plot()
    result = sm.tsa.stattools.adfuller(evol.nb)
    plt.show()
