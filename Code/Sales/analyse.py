#Import models from scikit learn module:
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold   #For K-fold cross validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def afficheAllData(datas):
  datas.hist(bins=50, figsize=(20,15))
  plt.savefig("attribute_histogram_plots")
  plt.show()
  
def correlation(datas,output):
  corr_matrix=datas.corr()
  print corr_matrix[output].sort_values(ascending=False)


def afficheCorr(datas,field1,field2):
  datas.plot(kind="scatter", x=field1, y=field2, alpha=0.5)
  plt.savefig('scatter.png')
  plt.show()
