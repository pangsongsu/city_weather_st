import pandas as pd
from sqlalchemy import create_engine, text
import datetime, time
last_days=5
cw_db_engine = create_engine(
    (r"sqlite:///D:\\workcloud\\python_notebook\\city_weather_st\\Dbs\\city_weather_st_dbs.db"))
# 获取全部城市数据
df_city = pd.read_sql("select * from city order by country,province;", cw_db_engine)
df_city['longitude'] = df_city['longitude'].astype(float)
df_city['latitude'] = df_city['latitude'].astype(float)

df_w = pd.read_sql("select * from cw_weather;", cw_db_engine)  # 只选第1个城市
df_w['datetime'] = pd.to_datetime(df_w['datetime']).dt.date

# 计算日期的最小值
d_min = df_w.groupby('name_cn')['datetime'].min()
df_city = df_city.join(d_min, on='name_cn')
df_city.rename(columns={"datetime": "date_min"}, inplace=True)
# 计算日期的最大值
d_max = df_w.groupby('name_cn')['datetime'].max()
df_city = df_city.join(d_max, on='name_cn')
df_city.rename(columns={"datetime": "date_max"}, inplace=True)

d_m = df_w.groupby('name_cn')

# 遍历分组结果并获取每个城市的气温数据
list_city=[]
list_data=[]
for city_name, city_data in d_m:
    list_city.append(city_name)
    list_data.append(city_data['temp'].tolist()[-last_days:])

dict_last_temp=dict(zip(list_city,list_data))


# 将字典转换为列表
data_list = [{'name_cn': k, 'list_temp': v} for k,v in dict_last_temp.items()]

# 使用列表创建 DataFrame
df = pd.DataFrame(data_list)

# 显示 DataFrame
print(df)