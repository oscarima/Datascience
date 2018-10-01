#Import models from scikit learn module:
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold   #For K-fold cross validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
import pandas as pd
import numpy as np


#Generic function for making a classification model and accessing performance:
def classification_model(model, data, predictors, outcome):
  #Fit the model:
  model.fit(data[predictors],data[outcome])
  
  #Make predictions on training set:
  predictions = model.predict(data[predictors])
  
  #Print accuracy
  accuracy = metrics.accuracy_score(predictions,data[outcome])
  print ("Accuracy : %s" % "{0:.3%}".format(accuracy))


  #Perform k-fold cross-validation with 5 folds
  kf = KFold(data.shape[0], n_folds=5)
  error = []
  for train, test in kf:
    # Filter training data
    train_predictors = (data[predictors].iloc[train,:])
    
    # The target we're using to train the algorithm.
    train_target = data[outcome].iloc[train]
    
    # Training the algorithm using the predictors and target.
    model.fit(train_predictors, train_target)
    
    #Record error from each cross-validation run
    error.append(model.score(data[predictors].iloc[test,:], data[outcome].iloc[test])) 
  print ("Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(error)))

  
  #Fit the model again so that it can be refered outside the function:
  model.fit(data[predictors],data[outcome]) 

def linear_model(model, data,pred, predictors, outcome):
  #Fit the model:
  model.fit(data[predictors],data[outcome])

  #Make predictions on training set:
  predictions = model.predict(pred[predictors])
  
  #Print accuracy
  accuracy = model.score(pred[predictors],pred[outcome])
  print ("Accuracy : %s" % "{0:.3%}".format(accuracy))
  pred['predictions']=predictions


def classification_model_with2src(model, data,data2, predictors, outcome):
  #Fit the model:
  model.fit(data[predictors],data[outcome])
  
  #Make predictions on training set:
  predictions = model.predict(data2[predictors])

  #Print accuracy
  accuracy = metrics.accuracy_score(predictions,data2[outcome])
  print ("Accuracy : %s" % "{0:.3%}".format(accuracy))
  data2['predictions']=predictions

  #Fit the model again so that it can be refered outside the function:
  model.fit(data[predictors],data[outcome]) 

def view_predict(model, data, predictors, outcome):
  #Fit the model:
  model.fit(data[predictors],data[outcome])
  
  #Make predictions on training set:
  predictions = model.predict(data[predictors])
  
  #Print accuracy
  accuracy = metrics.accuracy_score(predictions,data[outcome])
  print ("Accuracy : %s" % "{0:.3%}".format(accuracy))
  data['predictions']=predictions
  #print data



#Binning:
def binning(col, cut_points, labels=None,minval=None,maxval=None):
  #Define min and max values:
  if minval==None:
    minval = col.min()
  if maxval==None:
    maxval = col.max()

  #create list by adding min and max to cut_points
  break_points = [minval] + cut_points + [maxval]
  
  #if no labels provided, use default labels 0 ... (n-1)
  if not labels:
    labels = range(len(cut_points)+1)

  #Binning using cut function of pandas
  colBin = pd.cut(col,bins=break_points,labels=labels,include_lowest=True)
  return colBin

#Define a generic function using Pandas replace function
def coding(col, codeDict):
  colCoded = pd.Series(col, copy=True)
  for key, value in codeDict.items():
    colCoded.replace(key, value, inplace=True)
  return colCoded


