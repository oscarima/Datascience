# -*- coding: cp1252 -*-



##  if analysedata==False:
##    le = LabelEncoder()
##    var_mod = ['salesbin','tbin']
##    for i in var_mod:
##      train[i] = le.fit_transform(train[i])
##      pred[i] = le.fit_transform(pred[i])

 
  if analysedata:
    print train.describe()
    #print train.apply(num_missing, axis=0)
    #print train
    #print train.apply(num_missing, axis=1)


    #rr24bin -- pas concluant en terme de répartition
    #ubin -- inverse low --> CA sup
    #tbin ok sauf >20

    test=train.pivot_table(values=["Sales"],index=['year','week','dayoff'],aggfunc=np.mean)
    print test
   
   
##    test=pd.crosstab(pred["tbin"],pred["salesbin"],margins=True).apply(percConvert, axis=0)
##    print test





    
  if analysedata==False:
