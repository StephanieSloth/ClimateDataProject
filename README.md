# ClimateDataProject
从NOAA上获取站点气候数据，对中国境内226个站点数据进行插值，依据2020年行政区划统计各区县的气候数据

## 文件说明
**实际操作中先运行get_data_by_day，再运行cut_boundart_county**

1. get_all_stations.py
  用于获取中国境内的所有站点信息，包括站点编号、名称、地点、经度、纬度

2. get_data_by_day.py
  用于获取每日数据，以年为循环。
  设置初始日期为2020-01-01，结束日期为2021-01-01，表示获取2020年的所有数据

3.cut_boundary_rbf.py
  用于测试插值方法
  
4.cut_boundary_county.py
   用于对已获取的每日数据进行插值，并按区县统计 
