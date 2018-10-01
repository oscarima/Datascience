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
  #datas.rrsum=datas.apply(lambda row: row.workday*row.rrsum,axis=1)
  datas['Sales'].fillna(0, inplace=True)


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


def AssignImma(datas):
  imma=i.load_imma()  
  datas["fk"]=datas.index.strftime("%Y%m")

  datas["SalesDate"]=datas.index
  datas=datas[["fk","ProductGroupFamilyId","Sales","rrsum","workday"]].groupby(["fk","ProductGroupFamilyId"],as_index=False).sum()

  datas=datas.set_index('fk').join(imma.set_index('Date'))
  datas["ym"]=datas.index
  datas["y"]=datas.apply(lambda row: row.ym[0:4],axis=1).astype(int)
  datas["m"]=datas.apply(lambda row: row.ym[4:6],axis=1).astype(int)  
  return datas
  


if __name__ == '__main__':

  print "** par mois avec imma**"
  train_imma=s.loadDatas("salesfamille.csv","20150101","20171231")
  train_imma=AssignMeteo(train_imma,"meteo.csv")  
  cleanDatas(train_imma)
  train_imma=AssignImma(train_imma)
  #print train_imma.describe()
  
  pred_imma=s.loadDatas("salesfamille.csv","20160901","20181231")
  
  print pred_imma

  pred_imma=AssignMeteo(pred_imma,"meteo.csv")
  cleanDatas(pred_imma)

  pred_imma=AssignImma(pred_imma)
  print pred_imma
  
  for grfam in [1,2,3,4,5,6,7,8,9,14,15]:

    train=train_imma[train_imma.ProductGroupFamilyId==grfam]
    
    pred=pred_imma[pred_imma.ProductGroupFamilyId==grfam]

    print '*************** Linear regression for {0}***********************************'.format(grfam)
    
   #le decalage est faux
    train["Moto"]=train.Moto.shift(24)
    train=train[train.Moto.isnull()==False]
    

    pred["Moto"]=pred.Moto.shift(24)
    pred=pred[pred.Moto.isnull()==False]


    #a.correlation(train,"Sales")
   # datas=train_imma[train_imma.ProductGroupFamilyId==15] #No 1,2,3,4,5,6, 7
    #print datas
    #a.afficheCorr(datas,"Sales","Moto")
    #a.afficheAllData(datas)

    
    predictor_var = ['Moto','y']
    outcome_var = 'Sales'
    #test_algo(train_imma,predictor_var,outcome_var)


    model = LinearRegression()
    f.linear_model(model, train,pred,predictor_var,outcome_var)
    print pred_imma[['m','Sales','predictions','Moto']]
    #pred.to_csv("prev/prevision{0}.csv".format(grfam),index=False)

    if (grfam ==2):
      plt.plot(pred.m,pred.Sales,label='Sales_{0}'.format(grfam),color='r')
      plt.plot(pred.m,pred.predictions,label='predictions_{0}'.format(grfam),color='b')
    if (grfam ==9):
      plt.plot(pred.m,pred.Sales,label='Sales_{0}'.format(grfam),color='g')
      plt.plot(pred.m,pred.predictions,label='predictions_{0}'.format(grfam),color='y')

    print pred[['Sales','predictions']].sum()
##
  plt.xlabel('Mois')
  plt.ylabel('Sales')
  plt.title('Ventes')
  plt.legend()
  #plt.show()
##
