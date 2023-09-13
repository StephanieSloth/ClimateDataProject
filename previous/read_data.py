import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
"""
把对应字段的数据提取出来
"""

data = pd.read_csv('../GSOD/data/2020/climatedata_china_2020-01-01.csv', sep=',')
precipitation = data[data['datatype']=='PRCP']
maxtemp = data[data['datatype']=='TMAX']
mintemp = data[data['datatype']=='TMIN']
avgtemp = data[data['datatype']=='TAVG']
snow = data[data['datatype']=='SNWD']
print(data)
