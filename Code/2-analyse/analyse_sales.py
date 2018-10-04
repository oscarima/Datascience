# -*- coding: cp1252 -*-
import pandas as pd
import numpy as np
import datetime as dt
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels.api as sm

def load_work(file):
    datas = pd.read_csv(file,",")
    #datas.Moto=datas.Moto.astype(int)
    #datas.Cyclo=datas.Cyclo.astype(int)
    datas.ymd=pd.to_datetime(datas['ymd'], format='%Y-%m-%d',errors='coerce')
    datas=datas[(datas.ymd.dt.year<2018) ]
    datas=datas.set_index('ymd')
    return datas

def infos(datas):    
    print datas.info()
    print datas.describe()
    #print datas.head(10)
    
def afficheAllData(datas):
  datas.hist(bins=50, figsize=(20,15))
  #plt.savefig("attribute_histogram_plots")
  plt.show()
  
def correlation(datas,output):
  corr_matrix=datas.corr()
  print corr_matrix[output].sort_values(ascending=False)


def afficheCorr(datas,field1,field2):
  datas.plot(kind="scatter", x=field1, y=field2, alpha=0.5)
  #plt.savefig('scatter.png')
  plt.show()

def saisonalite(datas):
    sm.tsa.seasonal_decompose(datas.sales,freq=12).plot()
    result = sm.tsa.stattools.adfuller(datas.sales)
    plt.show()
    
if __name__ == '__main__':
    
    file='../work/sales_STREET_FR.csv'
##    file='../work/sales_OFFROAD_FR.csv'
##    file='../work/sales_50CC_FR.csv'
    file='../work/sales_STREET_FR_noimma.csv'
##    file='../work/sales_OFFROAD_FR.csv'
##    file='../work/sales_50CC_FR.csv'
    datas=load_work(file)
    infos(datas)
    correlation(datas,"sales")
    #afficheAllData(datas)
    #afficheCorr(datas,"Moto","sales")
    saisonalite(datas)
    

