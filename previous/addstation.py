import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
"""
把站点信息加入到data中
"""

stations = pd.read_csv('../GSOD/data/stations_info_china.csv', sep=',')
data = pd.read_csv('data\climatedata_china2020-01-01.csv', sep=',')
dict_station = stations.set_index('id').T.to_dict()
# 左连接两个表格
df_merged = data.merge(stations, left_on='station', right_on='id', how='left')
# 删除冗余列
df_merged.drop(columns=['id','attributes','elevationUnit','datacoverage','mindate','maxdate','elevation'], inplace=True)
# 指定新的列顺序
new_order = ['date', 'station', 'name', 'latitude','longitude','datatype','value']
# 调整列顺序
df_reordered = df_merged.reindex(columns=new_order)
print(df_reordered)
