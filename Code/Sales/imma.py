# -*- coding: cp1252 -*-
import pandas as pd

def load_imma():
    imma = pd.read_csv("imma.csv",";")
    imma["Date"]=imma["Date"].astype(str)

    return imma

if __name__ == '__main__':
    print load_imma()#.info()
