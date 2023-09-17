import os
from time import sleep

import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

"""
一天一天获取数据，直接取的是全中国的站点
problem: 
1. 目前的全中国站点的数据超过1000个，需要分两次取数
2. 按天存储数据对于后续处理不太方便
STATUS:
2023/9/3    代码写完了
"""


def update_params(params):
    params["startdate"] += datetime.timedelta(days=1)
    params["enddate"] = params["startdate"]
    return params

def add_station_info(data):
    stations = pd.read_csv('data\stations_info_china.csv', sep=',')
    # 左连接两个表格
    df_merged = data.merge(stations, left_on='station', right_on='id', how='left')
    # 删除冗余列
    df_merged.drop(columns=['id', 'attributes', 'elevationUnit', 'datacoverage', 'mindate', 'maxdate', 'elevation'],
                   inplace=True)
    # 指定新的列顺序
    new_order = ['date', 'station', 'name', 'latitude', 'longitude', 'datatype', 'value']
    # 调整列顺序
    df_reordered = df_merged.reindex(columns=new_order)
    return df_reordered

# 从api接口获取数据
def get_data_from_api(api_url, params, api_token, offset, max_retries=3, retry_delay=0.5):
    retries = 0
    while retries < max_retries:
        try:
            # 在请求头中添加 'token' 字段，值为我的API令牌
            headers = {
                'token': api_token
            }
            response = requests.get(api_url, params=params, headers=headers)
            # print(response.request.headers)
            alldata = []  # 所有数据
            if response.status_code == 200:
                data = response.json()  # 字典格式
                alldata.extend(data["results"])
                if data["metadata"]["resultset"]["count"] > offset:
                    params["offset"] = offset + 1
                    headers = {'token': api_token}
                    response_back = requests.get(api_url, params=params, headers=headers)
                    data_back = response_back.json()
                    alldata.extend(data_back["results"])
                return alldata
            else:
                retries += 1
                sleep(retry_delay)
                print("请求失败，状态码：", response.status_code)

        except requests.exceptions.RequestException as e:
            print("请求异常：", e)


if __name__ == '__main__':
    # 初始化参数
    api_token = 'GfLCJbkEAGBBgPNTEsOmaBjBzZaoqcMC'  # api令牌，身份认证，我的邮箱对应的
    params = {}


    # 获取具体数据
    # 一天一天获取数据，直接取的是全中国的站点
    # df = pd.DataFrame()
    date_list = []
    lastdate = datetime.date(2020, 1, 1)  # 结束日期（不包含）
    offset = 1000   # 最多为1000
    params = {"datasetid": "GHCND",
              "locationid": "FIPS:CH",
              "startdate": datetime.date(2019, 1, 1),
              "enddate": datetime.date(2019, 1, 1),
              "units": "metric",
              "limit": offset
              }
    while (params["enddate"] < lastdate):
        # 当前日期
        print(params["enddate"])
        date_list.append(params["enddate"])
        # 获取数据
        data = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/data?", params, api_token,offset)
        df = pd.DataFrame(data)
        df_with_station_info = add_station_info(df)

        # 当前日期写入表格
        writedate = params["enddate"]
        writedate_str = writedate.strftime("%Y-%m-%d")
        year_str = writedate.strftime("%Y")
        # 检查年份对应的文件夹是否存在，如果不存在则创建
        year_folder = os.path.join('data', year_str)
        if not os.path.exists(year_folder):
            os.mkdir(year_folder)
        # 构造文件路径
        dir = "data"+'\\'+year_str+"\climatedata_china_" + writedate_str + ".csv"
        df_with_station_info.to_csv(dir, index=False)
        # 更新参数
        params = update_params(params)


