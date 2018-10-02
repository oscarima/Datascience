# -*- coding: cp1252 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import statsmodels.api as sm
#Create a new function:
def num_missing(x):
  return sum(x.isnull())

def replace_month(x):
    if x=="January":
        return 1
    elif x=='February':
        return 2
    elif x=='March':
        return 3
    elif x=="April":
        return 4
    elif x=="May":
        return 5
    elif x=="June":
        return 6
    elif x=="July":
        return 7
    elif x=="August":
        return 8
    elif x=="September":
        return 9
    elif x=="October":
        return 10
    elif x=="November":
        return 11
    elif x=="December":
        return 12
    
    else:
        return x


def load_imma():
    imma = pd.read_csv("imma.csv",";")
    imma["Date"]=imma["Date"].astype(str)
    imma["Date"]=pd.to_datetime(imma["Date"], format='%Y%m%d',errors='coerce')
    imma=imma.set_index(imma.Date)
    return imma
        
def load_meteo():
  meteo = pd.read_csv("meteo.csv",sep=",")
  meteo["date"]=meteo["date"].astype(str)
  meteo["date"]=pd.to_datetime(meteo["date"], format='%Y%m%d',errors='coerce')
  return meteo
def changeday(row):
  return row.date.replace(day=1)


if __name__ == '__main__':
    sales = pd.read_csv("SalesBENEFRACH.csv",sep=",")
    #rename columns
    sales.columns=['day','month','group','salesregion','universe','year','sales']
    
    #print sales.info()
    #check missing

    #print sales.apply(num_missing)
    #replace month name by value

    sales["month"]=sales.apply(lambda row: replace_month(str(row.month)),axis=1)
    sales["ymd"]=sales.apply(lambda row:dt.datetime(int(row.year), int(row.month), 1),axis=1)

    #print sales.pivot_table(values=["sales"],index=["year","month","universe"],aggfunc=np.sum)
    #print sales
    #imma=load_imma()
    meteo=load_meteo()
    print meteo.info()
    meteo.date = meteo.apply(lambda row: changeday(row),axis=1)
    meteo=meteo[["date","rrsum"]].groupby(["date"]).sum()

  
    plt.subplot(211)
    plt.plot(meteo.index.to_pydatetime(),meteo.rrsum,label='Meteo',color='r')
    
    
##    plt.plot(imma.Date,imma.Moto,label='Moto',color='r')
##    plt.plot(imma.Date,imma.Cyclo,label='Cyclo',color='b')
##    plt.xlabel('Mois')
##    plt.ylabel('Qty')
##    plt.title('Ventes')
##    plt.legend()
##    plt.show()
    
    sales=sales[sales.salesregion=='FR']
    sales=sales[sales.universe=='OFFROAD']
    
    sales=sales[["ymd","sales"]].groupby(["ymd"]).sum()
    #merge
    
    print sales.info()
    plt.subplot(212)
    plt.legend()
    plt.plot(sales.index.to_pydatetime(),sales.sales,label='Ventes',color='r')

##    sm.tsa.seasonal_decompose(imma.Moto,freq=12).plot()
##    result = sm.tsa.stattools.adfuller(imma.Moto)
##    #plt.savefig("Famille{0}.png".format(group))
##    #plt.title('Groupe Famille {0}'.format(group))
    plt.show()
    #print sales.describe()
    #print sales[["year","month","sales"]].groupby(["month","year"]).sum()
    
##  print sales.describe()
##  print sales.head(10)
##  print sales.shape
    
