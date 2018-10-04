# -*- coding: cp1252 -*-
import pandas as pd
import numpy as np
import datetime as dt
import statsmodels.api as sm
import meteo as mt


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

def workday(row):
  if row.dayoff==False:
    return 1
  else:
    return 0

def load_imma(input_file):
    imma = pd.read_csv(input_file,";")
    imma["Date"]=imma["Date"].astype(str)
    imma["Date"]=pd.to_datetime(imma["Date"], format='%Y%m%d',errors='coerce')
    imma=imma.set_index(imma.Date)
    return imma

def load_sales(input,region='FR',universe='OFFROAD'):
    sales = pd.read_csv(input,sep=",")
    sales.columns=['day','month','group','salesregion','universe','year','sales']
    sales["month"]=sales.apply(lambda row: replace_month(str(row.month)),axis=1)
    sales["ymd"]=sales.apply(lambda row:dt.datetime(int(row.year), int(row.month), 1),axis=1)
    sales=sales[sales.salesregion==region]
    sales=sales[sales.universe==universe]    
    sales=sales[["ymd","sales"]].groupby(["ymd"]).sum()
    return sales

def load_holidays():
    holiday=pd.read_csv("jours_feries_alsace_moselle.csv",sep=",")
    holiday.date=pd.to_datetime(holiday['date'], format='%Y-%m-%d',errors='coerce')
    return holiday

def load_meteo(inputfile):
    meteo = pd.read_csv(inputfile,sep=",")
    meteo["date"]=pd.to_datetime(meteo["date"], format='%Y%m%d',errors='coerce')
    meteo["ymd"]=meteo.apply(lambda row:dt.datetime(int(row.date.year), int(row.date.month), 1),axis=1)
    meteo=meteo[["ymd","rrsum"]].groupby(["ymd"]).sum()
    #imma=imma.set_index(imma.Date)
    return meteo

def load_calendar(inputfile,start,end):
    dates = pd.date_range(start=start,end=end)
    calendar = pd.DataFrame({'date':dates})
    holiday=pd.read_csv(inputfile,sep=",")
    holiday.date=pd.to_datetime(holiday['date'], format='%Y-%m-%d',errors='coerce')
    datas=calendar.set_index('date').join(holiday.set_index('date'))
    datas["date"]=datas.index
    datas["weekday"]=datas.apply(lambda row: row.date.weekday(),axis=1)
    datas["week"]=datas.apply(lambda row: int(row.date.strftime("%U")),axis=1)
    datas["dayoff"]=datas.apply(lambda row: row.weekday==5 or row.weekday==6 or row.est_jour_ferie==True,axis=1)
    datas["workday"]=datas.apply(lambda row: workday(row),axis=1)  
    datas["month"]=datas.apply(lambda row: row.date.month,axis=1)
    datas["year"]=datas.apply(lambda row: row.date.year,axis=1)  
    return datas

def load_calendar_bymonth(input_ferie,start,end):
    datas=load_calendar(input_ferie,start,end)
    datas["ymd"]=datas.apply(lambda row:dt.datetime(int(row.year), int(row.month), 1),axis=1)
    datas=pd.pivot_table(datas,values='workday', index=['ymd'],columns=['weekday'], aggfunc=np.sum)
    #datas=datas[["ymd","dayoff","workday"]].groupby(["ymd"]).sum()
    return datas
    
def build_sales_immat_calendar(outputfile,region,universe,input_meteo,imma=True):
    input_sales = "../sources/SalesBENEFRACH.csv"
    #input_meteo = "../sources/meteo.csv"
    input_ferie ="../sources/jours_feries_alsace_moselle.csv"
    input_imma="../sources/imma.csv"
    #load data
    sales=load_sales(input_sales,region,universe)
    if (imma==True):
        imma=load_imma(input_imma)
    meteo=load_meteo(input_meteo)
    calendar=load_calendar_bymonth(input_ferie,"20150101","20191231")
    
  

    #calcul nb jour    
    datas=calendar.join(sales)    
    datas=datas.join(meteo)
    if (imma==True):    
        datas=datas.join(imma)
        datas= datas.drop('Date', 1)
    datas= datas.drop(5, 1)
    datas= datas.drop(6, 1)
    datas['sales'].fillna(0, inplace=True)
    if (imma==True):
        datas["Moto"]=datas.Moto.shift(24)
        datas["Cyclo"]=datas.Cyclo.shift(24)
        datas=datas[datas.Moto.isnull()==False]
    
    datas.to_csv(outputfile,index=True)

    return datas
    



if __name__ == '__main__':

    file="../datas/work.csv"
##    mt.getMeteo("201810")
##    mt.buildMeteo("../sources/meteo.csv")
##    mt.buildMeteo("../sources/meteoFull.csv",True)
##    build_sales_immat_calendar("../work/sales_OFFROAD_FR.csv","FR","OFFROAD","../sources/meteoFull.csv")
##    build_sales_immat_calendar("../work/sales_50CC_FR.csv","FR","50CC","../sources/meteo.csv")
##    build_sales_immat_calendar("../work/sales_STREET_FR.csv","FR","STREET","../sources/meteo.csv")


    build_sales_immat_calendar("../work/sales_OFFROAD_FR_noimma.csv","FR","OFFROAD","../sources/meteoFull.csv",False)
    build_sales_immat_calendar("../work/sales_50CC_FR_noimma.csv","FR","50CC","../sources/meteo.csv",False)
    build_sales_immat_calendar("../work/sales_STREET_FR_noimma.csv","FR","STREET","../sources/meteo.csv",False)
    
    



