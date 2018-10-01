# -*- coding: cp1252 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold   #For K-fold cross validation
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz

from sklearn import metrics
import meteo as m
import sales as s
import function as f
import analyse as a
import datetime as dt
import imma as i
import glob
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder



def roundSales(row):
  val=row.Sales/100000.00
  return round(val)

def valid(value):
  if value<0:
    return 1
  else:
    return 0

def cleanDatas(datas):
    #encode datas
##  datas.rrsum=datas.apply(lambda row: row.workday*row.rrsum,axis=1)
  datas['Sales'].fillna(0, inplace=True)
##  datas['SalesRound']=datas.apply(lambda row: roundSales(row),axis=1)
##
##  datas['before']=datas.workday.shift(-1)-datas.workday
##  datas['before']=datas.apply(lambda row: valid(row.before),axis=1)
##  datas['before'].fillna(0, inplace=True)
##
##  datas['after']=datas.workday-datas.workday.shift(1)
##  datas['after']=datas.apply(lambda row: valid(-row.after),axis=1)
##  datas['after'].fillna(0, inplace=True)

def percConvert(ser):
  return ser/float(ser[-1])




def num_missing(x):
  return sum(x.isnull())

def test_algo(train,predictor_var,outcome_var):

    print '*************** LogisticRegression ***************'
    model = LogisticRegression()
    f.classification_model(model,train,predictor_var,outcome_var)

    print '*************** RandomForestClassifier ***************'
    model =  RandomForestClassifier(n_estimators=100,random_state =1)
    f.classification_model(model, train,predictor_var,outcome_var)
    
    featimp = pd.Series(model.feature_importances_, index=predictor_var).sort_values(ascending=False)
    print (featimp)
    
    #print "Confusion Matrix"
    #f.view_predict(model, train,predictor_var,outcome_var)
    #print pd.crosstab(train["SalesRound"],train["predictions"],margins=True)#.apply(percConvert, axis=0)
    #print train
 
    print '*************** DecisionTreeClassifier ***************'
    model = DecisionTreeClassifier()
    f.classification_model(model, train,predictor_var,outcome_var)  
 
    print '*************** KNN***********************************'
    model = KNeighborsClassifier(n_neighbors=3)
    f.classification_model(model, train,predictor_var,outcome_var)
    

    

def AssignMeteo(datas,meteofile):
  meteo = pd.read_csv(meteofile,sep=",")
  meteo.date=meteo.date.astype(str)
  datas["SalesDate"]=datas.index
  #print datas.info()
  #print meteo.info()
  datas=datas.set_index('SalesDate').join(meteo.set_index('date'))
  return datas
  #return datas.loc[:,['year','month','week','weekday','workday','t','u','rrsum','Sales']]


def AssignImma(datas):
  imma=i.load_imma()  
  datas["fk"]=datas.index.strftime("%Y%m")
  datas["SalesDate"]=datas.index
  datas=datas[["fk","Sales","rrsum","workday"]].groupby(["fk"]).sum()
  datas["fk"]=datas.index.astype(str)

  datas=datas.set_index('fk').join(imma.set_index('Date'))
  datas["ym"]=datas.index
  datas["y"]=datas.apply(lambda row: row.ym[0:4],axis=1).astype(int)
  datas["m"]=datas.apply(lambda row: row.ym[4:6],axis=1).astype(int)
  return datas
  #return datas.loc[:,['ym','Sales','rrsum','Cyclo','Moto','SalesRound','y','m']]
  


if __name__ == '__main__':
  
  #objectif 84 253 362,00 €
  print "** par mois avec imma**"
  #salesFamille2
  filesales="salesfr.csv"
  #filesales="salesFamille9.csv"
  train_imma=s.loadDatas(filesales,"20150101","20171231")
  train_imma=AssignMeteo(train_imma,"meteo.csv",)
  cleanDatas(train_imma)
  train_imma=AssignImma(train_imma)
  
  pred_imma=s.loadDatas(filesales,"20160101","20180930")
  pred_imma=AssignMeteo(pred_imma,"meteo.csv",)
  cleanDatas(pred_imma)
  pred_imma=AssignImma(pred_imma)
  #print pred_imma.info()
 
  train_imma["Moto"]=train_imma.Moto.shift(24)
  train_imma=train_imma[train_imma.Moto.isnull()==False]
  pred_imma["Moto"]=pred_imma.Moto.shift(24)
  pred_imma=pred_imma[pred_imma.Moto.isnull()==False]

  a.correlation(train_imma,"Sales")
  #a.afficheCorr(train_imma,"Sales","Moto")
  #a.afficheAllData(train_imma)

  
  predictor_var = ['Moto','rrsum']
  outcome_var = 'Sales'
  #test_algo(train_imma,predictor_var,outcome_var)

  print '*************** Linear regression***********************************'
  model = LinearRegression()
  f.linear_model(model, train_imma,pred_imma,predictor_var,outcome_var)
  print pred_imma[['m','Sales','predictions','Moto']]
  pred_imma.to_csv("previsionfr.csv",index=False)
  
  plt.plot(pred_imma.m,pred_imma.Sales,label='Sales',color='r')
  plt.plot(pred_imma.m,pred_imma.predictions,label='predictions',color='b')
  plt.xlabel('Mois')
  plt.ylabel('Sales')
  plt.title('Ventes')
  plt.legend()
  plt.show()

  print pred_imma[['Sales','predictions']].sum()


