import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

"""
按照站点分别取数
STATUS:
2023/9/3    代码未修改，时间范围是一个月
"""

def update_params(params, beginflag):

    if beginflag == 1:
        params["enddate"] = params["startdate"] + datetime.timedelta(days=1)  # 加一天
        # params["enddate"] = params["startdate"] + relativedelta(months=1) - datetime.timedelta(days=1)
        beginflag = 0
    else:
        params["startdate"] += relativedelta(months=1)
        params["enddate"] = params["startdate"] + relativedelta(months=1) - datetime.timedelta(days=1)
    return params, beginflag


# 从api接口获取数据
def get_data_from_api(api_url, params, api_token):
    try:
        # 在请求头中添加 'token' 字段，值为我的API令牌
        headers = {
            'token': api_token
        }
        response = requests.get(api_url, params=params, headers=headers)
        print(response.request.headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("请求失败，状态码：", response.status_code)
    except requests.exceptions.RequestException as e:
        print("请求异常：", e)


if __name__ == '__main__':
    # 初始化参数
    api_token = 'GfLCJbkEAGBBgPNTEsOmaBjBzZaoqcMC'  # api令牌，身份认证，我的邮箱对应的
    params = {}

    # 获取具体数据
    beginflag = 1
    # df = pd.DataFrame()
    date_list = []
    lastdate = datetime.date(2020, 1, 2)
    params = {"datasetid": "GHCND",
              "locationid": "FIPS:CH",
              # "stationid": "GHCND:CHM00053898",
              "startdate": datetime.date(2020, 1, 1),
              "enddate": datetime.date(2020, 1, 1),
              "units": "metric",
              "limit": 1000
              }

    while (params["enddate"] < lastdate):
        params, beginflag = update_params(params, beginflag)
        # date_list.append(params["enddate"])
        # print(date_list)
        data = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/data?", params, api_token)
        # print(data)
        date_list.append(data["results"])

