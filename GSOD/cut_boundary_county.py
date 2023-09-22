import datetime
import os

import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.interpolate import Rbf
from shapely.geometry import Point
import matplotlib.pyplot as plt

"""
实际处理县级数据
"""


# 统一插值，再划分
def calculate_unify(x_mesh, y_mesh, provinces, rbf):
    z_mesh = rbf(x_mesh, y_mesh)
    # 创建几何对象，将数据转换为 Point
    row_xmesh = len(x_mesh)
    col_xmesh = len(x_mesh[0])
    geometry = [Point(x_mesh[i][j], y_mesh[i][j]) for i in range(row_xmesh) for j in range(col_xmesh)]

    # 创建包含插值数值和省名的新 DataFrame，同时包括几何信息
    data = {'value': [z_mesh[i][j] for i in range(len(z_mesh)) for j in range(len(z_mesh[0]))]}
    gdf = gpd.GeoDataFrame(data, geometry=geometry)
    # 切分省份
    # 匹配右侧 GeoDataFrame 中所有包含左侧 GeoDataFrame 中的点（left）的省份
    # 我们希望找到在省份边界内的每个点，因此使用 "within"。
    gdf.crs = "EPSG:4326"
    gdf = gpd.sjoin(gdf, provinces, how="right", predicate="within")

    # 计算每个省份的平均值
    avg_values = gdf.groupby("县级")["value"].mean()  # series
    grouped_data = gdf.groupby(["省级","省级码","地级", "地级码","县级", "县级码"])["value"].mean().reset_index()
    sorted_data = grouped_data.sort_values(by='省级')  # 按省级排序
    return sorted_data


# 获得插值结果
def interpolate_data(station_data):
    data_values = station_data['value']  # 替换为对应站点的实际数值

    # 站点坐标和对应的数值数据
    site_x = station_data['longitude']  # 替换为站点坐标的经度
    site_y = station_data['latitude']  # 替换为站点坐标的纬度

    # 设置插值网格的范围和分辨率
    x_min, y_min, x_max, y_max = china_boundary.total_bounds  # 获取经纬度的最大值和最小值
    resolution = 0.03  # 替换为所需的实际分辨率
    # 创建插值网格的坐标点
    x_mesh, y_mesh = np.meshgrid(np.arange(x_min, x_max, resolution),
                                 np.arange(y_min, y_max, resolution))

    # RBF法插值
    # 插值平均气温
    rbf = Rbf(site_x, site_y, data_values, function='linear')
    county_data = calculate_unify(x_mesh, y_mesh, provinces, rbf)
    return county_data


if __name__ == '__main__':
    # 读取中国边界的矢量数据
    china_boundary = gpd.read_file('boundary/国界/国家矢量.shp')
    x_min, y_min, x_max, y_max = china_boundary.total_bounds
    # 读取省份边界shp文件
    provinces = gpd.read_file('boundary/2020年县级/县级.shp')
    provinces = provinces.sort_values(by='省级码')  # 按省级排序
    x_min1, y_min1, x_max1, y_max1 = provinces.total_bounds
    curdata = datetime.date(1980, 1, 1)  # 当前日期
    lastdate = datetime.date(1980, 1, 2)  # 结束日期（不包含）
    while (curdata < lastdate):
        # 读取表格数据
        year_str = curdata.strftime("%Y")  # 文件夹
        date_str = curdata.strftime("%Y-%m-%d")  # 日期文件
        read_dir = "data/" + year_str + "/climatedata_china_" + date_str + ".csv"
        data = pd.read_csv(read_dir, sep=',')

        precipitation = data[data['datatype'] == 'PRCP']  # 降水量
        maxtemp = data[data['datatype'] == 'TMAX']  # 最高气温
        mintemp = data[data['datatype'] == 'TMIN']  # 最低气温
        avgtemp = data[data['datatype'] == 'TAVG']  # 平均气温
        # snow = data[data['datatype'] == 'SNWD']

        # 插值数据
        county_PRCP = interpolate_data(precipitation)
        county_TMAX = interpolate_data(maxtemp)
        county_TMIN = interpolate_data(mintemp)
        county_TAVG = interpolate_data(avgtemp)

        # 合并数据
        merged_df = pd.merge(county_PRCP, county_TMAX,on=["省级","省级码","地级", "地级码","县级", "县级码"], how='outer',suffixes=('_A', '_B'))
        merged_df.columns = ["省级","省级码","地级", "地级码","县级", "县级码",'降水量（mm）','最高温度（C）']
        merged_df = pd.merge(merged_df, county_TMIN, on=["省级","省级码","地级", "地级码","县级", "县级码"], how='outer')
        merged_df.columns = ["省级","省级码","地级", "地级码","县级", "县级码", '降水量（mm）', '最高气温（C）', '最低气温（C）']
        merged_df = pd.merge(merged_df, county_TAVG, on=["省级","省级码","地级", "地级码","县级", "县级码"], how='outer')
        merged_df.columns = ["省级","省级码","地级", "地级码","县级", "县级码", '降水量（mm）', '最高气温（C）', '最低气温（C）', '平均气温（C）']
         # 将没有数据的地方填充为 NaN
        merged_df = merged_df.replace('', np.nan)

        # 构造文件路径
        # 检查年份对应的文件夹是否存在，如果不存在则创建
        year_folder = os.path.join('results', year_str)
        if not os.path.exists(year_folder):
            os.mkdir(year_folder)
        dir = "results/" + year_str + "/县级数据_" + date_str +".csv"
        merged_df.to_csv(dir, index=False, encoding='GBK')

        # 这一天完成
        print(date_str + " done!")
        # 加一天
        curdata += datetime.timedelta(days=1)
