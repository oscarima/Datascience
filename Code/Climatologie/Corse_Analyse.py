# -*- coding: cp1252 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

if __name__ == '__main__':
    meteo = pd.read_csv("meteoCorseAjacio.csv",sep=",")
    meteo['date']=pd.to_datetime(meteo['date'], format='%Y%m%d',errors='coerce')
    meteo['y']=meteo.date.dt.year
    meteo['m']=meteo.date.dt.month
    meteo['d']=meteo.date.dt.day
    meteo=meteo[meteo.date.dt.month==10] 
    meteo=meteo.set_index("date")
    m4=meteo[meteo.y==2014]
    m5=meteo[meteo.y==2015]
    m6=meteo[meteo.y==2016]
    m7=meteo[meteo.y==2017]
    m8=meteo[meteo.y==2018]
    plt.title('Meteo Corse')
    plt.subplot(511)
    plt.plot(m4.d,m4.t,label='temperature',color='r')
    plt.plot(m4.d,m4.rrsum,label='rrsum',color='b')
    plt.subplot(512)
    plt.plot(m5.d,m5.t,label='temperature',color='r')
    plt.plot(m5.d,m5.rrsum,label='rrsum',color='b')    
    plt.subplot(513)
    plt.plot(m6.d,m6.t,label='temperature',color='r')
    plt.plot(m6.d,m6.rrsum,label='rrsum',color='b')
    #plt.title('Meteo Corse')
    plt.subplot(514)
    plt.plot(m7.d,m7.t,label='temperature',color='r')
    plt.plot(m7.d,m7.rrsum,label='rrsum',color='b')
    plt.subplot(515)
    plt.plot(m8.d,m8.t,label='temperature',color='r')
    plt.plot(m8.d,m8.rrsum,label='rrsum',color='b')

    
##    meteo=meteo.set_index("date")
##    m4=meteo[meteo.y==2014]
##    m5=meteo[meteo.y==2015]
##    m6=meteo[meteo.y==2016]
##    m7=meteo[meteo.y==2017]
##    m8=meteo[meteo.y==2018]
##    plt.title('Meteo Corse')
##    plt.subplot(511)
##    plt.plot(m4.index,m4.t,label='temperature',color='r')
##    plt.plot(m4.index,m4.rrsum,label='rrsum',color='b')
##    plt.subplot(512)
##    plt.plot(m5.index,m5.t,label='temperature',color='r')
##    plt.plot(m5.index,m5.rrsum,label='rrsum',color='b')    
##    plt.subplot(513)
##    plt.plot(m6.index,m6.t,label='temperature',color='r')
##    plt.plot(m6.index,m6.rrsum,label='rrsum',color='b')
##    #plt.title('Meteo Corse')
##    plt.subplot(514)
##    plt.plot(m7.index,m7.t,label='temperature',color='r')
##    plt.plot(m7.index,m7.rrsum,label='rrsum',color='b')
##    plt.subplot(515)
##    plt.plot(m8.index,m8.t,label='temperature',color='r')
##    plt.plot(m8.index,m8.rrsum,label='rrsum',color='b')
    
    plt.legend()
    plt.show()

##  #saisonalite
##    import statsmodels.api as sm
##    sm.tsa.seasonal_decompose(meteo.t,freq=360).plot()
##    result = sm.tsa.stattools.adfuller(meteo.t)
##    plt.show()



