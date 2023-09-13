import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
"""
取中国境内所有站点的数据，并存储
"""

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

    # 获取地区数据
    # data_fips = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/locations/FIPS:CH", params, api_token)

    # 获取站点数据
    params = {"locationid": "FIPS:CH",
              "limit": 1000,
              "offset":0
              }
    data_stations = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/stations?", params, api_token)
    params_front = {"locationid": "FIPS:CH",
              "limit": 100,
              "offset": 0  # 从第5个开始
              }
    params_back = {"locationid": "FIPS:CH",
                    "limit": 100,
                    "offset": 101  # 从第5个开始
                    }
    data_stations_front = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/stations?", params_front, api_token)
    data_stations_back = get_data_from_api("https://www.ncei.noaa.gov/cdo-web/api/v2/stations?", params_back, api_token)


    df_stations = pd.DataFrame(data_stations["results"])
    df_stations.to_csv('data\stations_info_china.csv', index=False)
    df = pd.read_csv('data\stations_info_china.csv', sep='\n')

