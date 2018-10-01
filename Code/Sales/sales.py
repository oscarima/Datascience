import pandas as pd
import numpy as np
import datetime as dt
import optparse
import glob


def workday(row):
  if row.dayoff==False:
    return 1
  else:
    return 0


def load_holidays():
  holiday=pd.read_csv("jours_feries_alsace_moselle.csv",sep=",")
  holiday.date=pd.to_datetime(holiday['date'], format='%Y-%m-%d',errors='coerce')
  return holiday

def loadDatas(salesfile,start,end):
  sales = pd.read_csv(salesfile,sep=",")  
  dates = pd.date_range(start=start,end=end)
  ##selection date
  calendar = pd.DataFrame({'date':dates})
  
  holidays=load_holidays()  
  datas=calendar.set_index('date').join(holidays.set_index('date'))
  datas["date"]=datas.index
  datas["weekday"]=datas.apply(lambda row: row.date.weekday(),axis=1)
  datas["week"]=datas.apply(lambda row: int(row.date.strftime("%U")),axis=1)
  datas["dayoff"]=datas.apply(lambda row: row.weekday==5 or row.weekday==6 or row.est_jour_ferie==True,axis=1)
  datas["workday"]=datas.apply(lambda row: workday(row),axis=1)  
  datas["month"]=datas.apply(lambda row: row.date.month,axis=1)
  datas["year"]=datas.apply(lambda row: row.date.year,axis=1)  
  sales.SalesDate=sales.SalesDate.astype(str)
  #join data
  datas=datas.set_index('date').join(sales.set_index('SalesDate'))  
  return datas

def buildSales(path,filename):
    frames = []
    print path,filename
    for fi in  glob.glob(path+"\sales*.*"):
        print "****Load {0} ****".format(fi)
        frames.append(pd.read_table(fi))
    result=pd.concat(frames)
    result.to_csv(filename,index=False)
    
def buildSalesByGroupFam(path,filename,grp):
    frames = []
    print path,filename
    for fi in  glob.glob(path+"\sales*.*"):
        print "****Load {0} ****".format(fi)
        frames.append(pd.read_table(fi))
    result=pd.concat(frames)
    result=result[result.ProductGroupFamilyId==int(grp)]
    result.to_csv(filename,index=False)
    
def exportdatas(salesfile,meteofile,start,end):
  datas=loadDatas(salesfile,meteofile,start,end)
  cleanDatas(datas)
  datas.to_csv("datas_{0}_{1}.csv".format(start,end),index=False)



if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option("-b","--build",action="store",dest="build",help="path")
    parser.add_option("-o","--output",action="store",dest="output",help="")
    parser.add_option("-g","--group",action="store",dest="group",help="group")
    (options,args)=parser.parse_args()
    if options.build and options.output:
      if (options.group!=None):
        buildSalesByGroupFam(options.build,options.output,options.group)
      else:
        buildSales(options.build,options.output)

    #train=loadDatas("sales.csv","meteo.csv","20150101","20171231")
  #exportdatas("sales.csv","meteo.csv","20140101","20180831",0)
