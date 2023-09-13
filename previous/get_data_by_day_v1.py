import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

"""
一天一天获取数据，直接取的是全中国的站点
problem: 
1. 目前的全中国站点的数据超过1000个，需要分两次取数——已解决
2. 按天存储数据对于后续处理不太方便
"""


def update_params(params):
    params["startdate"] += datetime.timedelta(days=1)
    params["enddate"] = params["startdate"]
    return params


# 从api接口获取数据
def get_data_from_api(api_url, params, api_token,offset):
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
                params["offset"] = offset+1
                headers = {'token': api_token}
                response_back = requests.get(api_url, params=params, headers=headers)
                data_back = response_back.json()
                alldata.extend(data_back["results"])
            return alldata
        else:
            print("请求失败，状态码：", response.status_code)
    except requests.exceptions.RequestException as e:
        print("请求异常：", e)


if __name__ == '__main__':
    # 初始化参数
    api_token = 'GfLCJbkEAGBBgPNTEsOmaBjBzZaoqcMC'  # api令牌，身份认证，我的邮箱对应的
    params = {}

    # 获取地区数据
    # data_fips = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/locations/FIPS:CH", params, api_token)

    # 获取站点数据
    # params = {"locationid": "FIPS:CH",
    #           "limit": 1000}
    # data_stations = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/stations?", params, api_token)
    # df_stations = pd.DataFrame(data_stations["results"])
    # df_stations.to_csv('data\stations_info_china.csv', index=False)
    # df = pd.read_csv('data\Place-Place1-To-Satellite-Satellite6_AER.csv', sep='\n')

    # 获取具体数据
    # 一天一天获取数据，直接取的是全中国的站点
    # df = pd.DataFrame()
    date_list = []
    lastdate = datetime.date(2020, 1, 2)  # 结束日期（不包含）
    params = {"datasetid": "GHCND",
              "locationid": "FIPS:CH",
              "startdate": datetime.date(2020, 1, 1),
              "enddate": datetime.date(2020, 1, 1),
              "units": "metric",
              "limit": 500
              }

    while (params["enddate"] < lastdate):
        date_list.append(params["enddate"])
        data = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/data?", params, api_token,500)
        params2 = {"datasetid": "GHCND",
                  "locationid": "FIPS:CH",
                  "startdate": datetime.date(2020, 1, 1),
                  "enddate": datetime.date(2020, 1, 1),
                  "units": "metric",
                  "limit": 1000
                  }
        data2 = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/data?", params2, api_token,1000)
        print("begin!")
        params = update_params(params)
        # 用于检验这种方式对不对
        # for i in range(len(data)):
        #     if (data[i] != data2[i]):
        #         print(i)


    print(date_list)
