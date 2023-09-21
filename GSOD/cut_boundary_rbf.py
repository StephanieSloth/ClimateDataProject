import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.interpolate import Rbf
from shapely.geometry import Point
import matplotlib.pyplot as plt
"""
为了确认插值RBF方法中的基函数效果
可视化函数能够输出省级边界
"""

# 统一插值，再划分
def calculate_unify(x_mesh, y_mesh, provinces,rbf):
    z_mesh = rbf(x_mesh, y_mesh)
    visiual(z_mesh,provinces)
    # 提取省名属性列
    province_names = provinces["省"]

    # 创建几何对象，将数据转换为 Point
    row_xmesh = len(x_mesh)
    col_xmesh = len(x_mesh[0])
    geometry = [Point(x_mesh[i][j], y_mesh[i][j]) for i in range(row_xmesh) for j in range(col_xmesh)]

    # 创建包含插值数值和省名的新 DataFrame，同时包括几何信息
    data = {'value': [z_mesh[i][j] for i in range(len(z_mesh)) for j in range(len(z_mesh[0]))]}
    gdf = gpd.GeoDataFrame(data, geometry=geometry)

    # 转换坐标参考系统 (CRS)
    # Left CRS: None
    # Right CRS: EPSG:4326 （WGS84）
    gdf = gdf.to_crs(provinces.crs)

    # 切分省份
    # 匹配右侧 GeoDataFrame 中所有包含左侧 GeoDataFrame 中的点（left）的省份
    # 我们希望找到在省份边界内的每个点，因此使用 "within"。
    gdf = gpd.sjoin(gdf, provinces, how="left", predicate="within")
    # 计算每个省份的平均值
    avg_values = gdf.groupby("省")["value"].mean()
    return avg_values


# 可视化插值结果
def visiual(z_mesh,provinces):
    plt.imshow(z_mesh, extent=[x_min, x_max, y_min, y_max], origin='lower',
               cmap='jet', alpha=0.7)
    plt.scatter(site_x, site_y, c=data_values,
                cmap='jet', edgecolor='k')
    plt.colorbar(label='average temperature（°C）')
    # 创建一个坐标轴对象
    ax = plt.gca()
    # 绘制 Shapefile 边界
    provinces.plot(ax=ax, edgecolor='black', facecolor='none')

    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.title('2020/08/31 interpolated results')
    plt.show()


if __name__ == '__main__':
    # 读取中国边界的矢量数据
    china_boundary = gpd.read_file('boundary/国界/国家矢量.shp')

    # 读取省份边界shp文件
    provinces = gpd.read_file('boundary/2020年省级/省级.shp')

    # 读取表格数据
    data = pd.read_csv('data/2020/climatedata_china_2020-08-31.csv', sep=',')
    precipitation = data[data['datatype'] == 'PRCP']
    maxtemp = data[data['datatype'] == 'TMAX']
    mintemp = data[data['datatype'] == 'TMIN']
    avgtemp = data[data['datatype'] == 'TAVG']
    snow = data[data['datatype'] == 'SNWD']

    # 站点坐标和对应的数值数据
    site_x = avgtemp['longitude']  # 替换为站点坐标的经度
    site_y = avgtemp['latitude']  # 替换为站点坐标的纬度
    data_values = avgtemp['value']  # 替换为对应站点的实际数值

    # 设置插值网格的范围和分辨率
    x_min, y_min, x_max, y_max = china_boundary.total_bounds  # 获取经纬度的最大值和最小值
    resolution = 0.1  # 替换为所需的实际分辨率
    # 创建插值网格的坐标点
    x_mesh, y_mesh = np.meshgrid(np.arange(x_min, x_max, resolution),
                                 np.arange(y_min, y_max, resolution))

    # RBF法插值
    # function = 'multiquadric'默认,'inverse','gaussian' ,'linear' ,'cubic' ,'quintic' , 'thin_plate'
    rbf = Rbf(site_x, site_y, data_values, function='linear')
    TAVG_province_unify = calculate_unify(x_mesh, y_mesh, provinces,rbf)

    # 设定省名
    check_data = pd.read_excel('data\TAVG_20200831.xlsx')
    rmse_table = pd.DataFrame(columns=['省', '参考数据', '插值数据', 'RMSE'])
    r = 0
    for prov in check_data['省']:
        # 提取对应省份的数据
        if prov == '澳门特别行政区':
            predicted = 0
        else:
            predicted = TAVG_province_unify[prov]
        actualdata = check_data[check_data['省'] == prov]['平均气温'].values
        actual, = actualdata # 提取数据
        # print(actual)
        rmse = np.sqrt(np.mean((predicted - actual) ** 2))
        rmse_table.loc[r] = [prov, actual, predicted, rmse]
        r += 1
    # # 构造文件路径
    # dir = "data" + '\\' + "rmse_table_RBF_thin_plate" + ".csv"
    # rmse_table.to_csv(dir, index=False, encoding='GBK')

