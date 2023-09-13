import requests
import datetime
from dateutil.relativedelta import relativedelta
"""
最初版本的获取数据的代码
"""
# 接收URL和API token作为参数
def get_data_from_api(api_url, api_token):
    try:
        # 在请求头中添加 'token' 字段，值为我的API令牌
        headers = {
            'token': api_token
        }
        response = requests.get(api_url, headers=headers)
        print(response.request.headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("请求失败，状态码：", response.status_code)
    except requests.exceptions.RequestException as e:
        print("请求异常：", e)


# 接收URL和API token作为参数
def get_data_from_api_new(api_url, params, api_token):
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
    # 使用示例
    datasetid = "GHCND"
    startdate = datetime.date(1980, 1, 1)
    enddate = datetime.date(1952, 1, 1)
    new_date = startdate + datetime.timedelta(days=1)
    new_date = startdate + relativedelta(months=1)
    now_date = new_date.strftime("%Y-%m-%d")
    units = "metric"
    # 和offset有关
    endpoint = f"data?datasetid={datasetid}&stationid=GHCND:CHM00053898&units={units}&startdate={startdate}&enddate={enddate}"
    api_url = f"https://www.ncei.noaa.gov/cdo-web/api/v2/{endpoint}"
    api_token = 'GfLCJbkEAGBBgPNTEsOmaBjBzZaoqcMC'  # api令牌，身份认证

    data = get_data_from_api(api_url, api_token)


    """ 把参数写到了params里面 """
    params = {"datasetid": "GHCND",
              "datatypeid": "TAVG",
              "stationid": "GHCND:CHM00053898",
              "startdate": datetime.date(1980, 1, 1),
              "enddate": datetime.date(1980, 1, 1),
              "units": "metric",
              "limit": 1000
              }
    data = get_data_from_api_new("https://www.ncei.noaa.gov/cdo-web/api/v2/data?", params, api_token)
    print(data)

"""
TODO:  
1. 确定所有站点序列
2. 获取站点的经纬度
3. 获取对应的温度、降水数据
"""
