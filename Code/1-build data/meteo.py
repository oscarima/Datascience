import pandas as pd
import numpy as np
import urllib2 as u
import gzip
import os
import glob
import datetime as dt
import optparse

def loadMeteo(file,full=True):
    meteo = pd.read_csv(file,sep=";")
    meteo=meteo.loc[:,['numer_sta','date','t','u','rr3']]
    #print meteo
    #convert data
    #filter only France
    meteo=meteo[meteo.numer_sta<8000]

    #convert to date only
    meteo.date=pd.to_datetime(meteo['date'], format='%Y%m%d%H0000',errors='coerce')
    #select only 12h
    if (full==False):
        meteo=meteo[(meteo.date.dt.hour>8) & (meteo.date.dt.hour<=18)]    
    meteo.date = (meteo["date"]).dt.strftime("%Y%m%d")
    #selected value
    meteo['t']=pd.to_numeric(meteo['t'], errors='coerce')-273.15
    meteo['u']=pd.to_numeric(meteo['u'], errors='coerce')
    meteo['rrsum']=pd.to_numeric(meteo['rr3'], errors='coerce')
    #clean null value
    meteo=meteo[meteo.t.isnull()==False]
    meteo=meteo[meteo.u.isnull()==False]
    meteo=meteo[meteo.rrsum.isnull()==False]
    mean= meteo[['date','t','u']].groupby(['date'],as_index=False).mean()
    rr=meteo[['date','rrsum']].groupby(['date'],as_index=False).sum() 
    result = pd.merge(mean,rr)
    return result


def loadMeteoBySta(file,num_sta):
    meteo = pd.read_csv(file,sep=";")
    meteo=meteo.loc[:,['numer_sta','date','t','u','rr3']]
    #print meteo
    #convert data
    #filter only France
    meteo.numer_sta=meteo.numer_sta.astype(str)
    meteo=meteo[meteo.numer_sta==num_sta]

    #convert to date only
    meteo.date=pd.to_datetime(meteo['date'], format='%Y%m%d%H0000',errors='coerce')
    #select only 12h
    meteo=meteo[(meteo.date.dt.hour>8) & (meteo.date.dt.hour<=18)]    
    meteo.date = (meteo["date"]).dt.strftime("%Y%m%d")
    #selected value
    meteo['t']=pd.to_numeric(meteo['t'], errors='coerce')-273.15
    meteo['u']=pd.to_numeric(meteo['u'], errors='coerce')
    meteo['rrsum']=pd.to_numeric(meteo['rr3'], errors='coerce')
    #clean null value
    meteo=meteo[meteo.t.isnull()==False]
    meteo=meteo[meteo.u.isnull()==False]
    meteo=meteo[meteo.rrsum.isnull()==False]
    mean= meteo[['date','t','u']].groupby(['date'],as_index=False).mean()
    rr=meteo[['date','rrsum']].groupby(['date'],as_index=False).sum() 
    result = pd.merge(mean,rr)
    return result

def getMeteo(dt):
    uri="https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop.{0}.csv.gz".format(dt)
    response = u.urlopen(uri)
    file = open("../sources/meteo/synop.{0}.csv.gz".format(dt), "wb")
    file.write(response.read())
    file.close()
    print "****Dowload {0} ****".format(uri)
    with gzip.open("../sources/meteo/synop.{0}.csv.gz".format(dt), 'rb') as f:
        file = open("../sources/meteo/synop.{0}.csv".format(dt), "wb")
        file.write(f.read())
        file.close()
    os.remove("../sources/meteo/synop.{0}.csv.gz".format(dt))

def buildMeteo(filename,full=False):
    frames = []
    for fi in  glob.glob("../sources/meteo/synop.*"):
        print "****Load {0} ****".format(fi)
        frames.append(loadMeteo(fi,full))
    result=pd.concat(frames)
    result.to_csv(filename,index=False)

def buildMeteoBySta(filename,num_sta):
    frames = []
    for fi in  glob.glob("../sources/meteo/synop.*"):
        print "****Load {0} ****".format(fi)
        frames.append(loadMeteoBySta(fi,num_sta))
    result=pd.concat(frames)
    result.to_csv(filename,index=False)

def loadAllMeteo(begin,end):
    dates = pd.date_range(start=begin,end=end,freq='M')
    for dt in dates:
        getMeteo(dt.strftime("%Y%m"))

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-l","--load",action="store",dest="load",help="load meteo yyyymm")
    parser.add_option("-b","--begin",action="store",dest="begin",help="load meteo yyyymm")
    parser.add_option("-e","--end",action="store",dest="end",help="load meteo yyyymm")
    (options,args)=parser.parse_args()
    if options.load:
        getMeteo(options.load)
        buildMeteo("../sources/meteo.csv")
        buildMeteo("../sources/meteoFull.csv",True)

    if options.begin:
        loadAllMeteo(options.begin,options.end)
