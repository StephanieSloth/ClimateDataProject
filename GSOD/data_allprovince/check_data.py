import pandas as pd
import datetime



if __name__ == '__main__':
    # 读取 Excel 文件为 DataFrame
    df = pd.read_excel('avgtemp_daily_allprovince_1951_to_2020.xlsx')
    # 创建一个 datetime 对象表示 2020-01-01
    date_to_filter = datetime.datetime(2020, 1, 1)
    # 筛选 date 列中所有等于 date_to_filter 的行
    result = df[df['日期'] == date_to_filter]

    # 把数据按照每个省份为一行，每列对应日期
    df_pivot = df.pivot(index='省', columns='日期', values='降水量')

    print(df)