# -*- coding: cp1252 -*-
import pandas as pd
import numpy as np
import datetime as dt




dates = pd.date_range('20180801',end='20180827')
calendar = pd.DataFrame({'date':dates})
calendar["weekday"]=calendar.apply(lambda row: row.date.weekday(),axis=1)
calendar["datetoapply"]=calendar.apply(lambda row: row.date-dt.timedelta(days=1),axis=1)
print calendar
