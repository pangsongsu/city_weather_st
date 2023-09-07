# when we import hydralit, we automatically get all of Streamlit
import pandas as pd
import streamlit as st
# import sqlite3
from sqlalchemy import create_engine, text
import datetime
import time

import os
import win32gui, win32print, win32con, win32api

from pyecharts.charts import Line
from pyecharts.charts import Geo
# from pyecharts.charts import Kline
# from pyecharts.charts import Bar
# from streamlit_echarts import st_pyecharts

from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType

from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ChartType
from pyecharts.faker import Faker
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components  # 将要展示的 弄成html
# when we import hydralit, we automatically get all of Streamlit
import hydralit as hy

cw_db_engine = create_engine(
    (r"sqlite:///D:\\workcloud\\python_notebook\\city_weather_st\\Dbs\\city_weather_st_dbs.db"))
# # 获取全部城市数据
# df_city = pd.read_sql("select * from city order by country,province;",cw_db_engine)
# df_city['longitude'] = df_city['longitude'].astype(float)
# df_city['latitude'] = df_city['latitude'].astype(float)

# 获取全部气象指标名称（含中英文）
# df_w = pd.read_sql("select * from cw_weather;", cw_db_engine)  # 只选第1个城市
# df_w['datetime'] = pd.to_datetime(df_w['datetime']).dt.date
# df_w.set_index('datetime', inplace=True)

# # 获取全部气象指标名称（含中英文）
# df_term = pd.read_sql("select * from term;", cw_db_engine)
cw_data_website = "https://www.visualcrossing.com/weather-data"

# current_path = os.path.dirname(os.path.abspath(__file__))
current_path = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件所在目录的绝对路径


# project_path = os.path.abspath(os.path.join(current_path, ".."))  # 获取当前项目的绝对路径


# 获取当前时间
def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


###获取缩放后的分辨率
def get_screen_size():
    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)
    return {"width": width, "height": height}


# 获取真实的分辨率
def get_real_screen_resolution():
    hDC = win32gui.GetDC(0)
    width = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    height = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return {"width": width, "height": height}


def color_cycle(colors):
    while True:
        for color in colors:
            yield color


colors = color_cycle(['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'black', 'white', 'gray', 'cyan', 'brown',
                      'gold', 'silver', 'pink', 'lime', 'magenta', 'teal', 'indigo'])


# for i in range(10):
#     print(next(colors))


def create_line_chart(df_w, city_seled, term_seled_en, term_seled_cn):
    # 初始化图表
    line = Line(init_opts=opts.InitOpts(width="1200px", height="700px"))
    # 添加x轴数据
    line.add_xaxis(df_w.index.tolist())
    # 根据需要动态添加y轴数据
    data_series = []
    for cs in city_seled:
        data_series.append((cs, df_w[cs].tolist()))

    for name, data in data_series:
        line.add_yaxis(name, data,
                       yaxis_index=0,
                       label_opts=opts.LabelOpts(is_show=False),
                       is_smooth=True,
                       itemstyle_opts=opts.ItemStyleOpts(color=next(colors), opacity=1.95)
                       )

        # 设置全局选项并渲染图表
    line.set_global_opts(title_opts=opts.TitleOpts(title=term_seled_cn + "[" + term_seled_en + "]对比"),
                         datazoom_opts=opts.DataZoomOpts(is_show=True, is_realtime=True, type_="inside",
                                                         range_start=0,
                                                         range_end=100),  # 缩放模块
                         legend_opts=opts.LegendOpts(is_show=True),
                         toolbox_opts=opts.ToolboxOpts(is_show=True),
                         tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"))

    # line.render()
    return line


screen_width = get_screen_size()["width"]
screen_height = get_screen_size()["height"]

chart_width = str(int(((screen_width * 5) / 6) - 300)) + "px"
chart_height = str(int(screen_height - 300)) + "px"

app = hy.HydraApp(title='城市气象分析App')


@app.addapp(is_home=True)
def my_home():
    hy.info('欢迎使用城市气象数据分析系统!')
    st.balloons()  # 庆祝气球
    st.toast('By fanjs. 2023')
    st.toast("今天是" + datetime.date.today().strftime("%Y-%m-%d"))
    # st.write(current_path)
    # st.write(project_path)


@app.addapp(title='城市气象数据对比', icon="🏘")
def app2():
    # 获取全部城市数据
    df_city = pd.read_sql("select * from city order by country,province;", cw_db_engine)
    df_city['longitude'] = df_city['longitude'].astype(float)
    df_city['latitude'] = df_city['latitude'].astype(float)
    # 获取全部气象指标名称（含中英文）
    df_term = pd.read_sql("select * from term;", cw_db_engine)

    city_seled = st.sidebar.multiselect("请选择被选城市:", df_city['name_cn'])
    term_seled = st.sidebar.selectbox("请选择气象指标:", df_term['term_en'] + "|" + df_term['term_cn'])

    st.sidebar.write("被选城市(按省排序):", city_seled)
    st.sidebar.write("气象指标:", term_seled)

    if len(city_seled) >= 1 and len(term_seled) >= 1:
        generate_button = st.sidebar.button("📊展示气象数据图表", disabled=False)

    else:
        generate_button = st.sidebar.button("📊展示气象数据图表", disabled=True)

    saved_chart_html_path = st.sidebar.text_input('图表html保存路径:', current_path + "\\cw_weather_chart.html")

    if generate_button:  # 按下按钮
        term_seled_en = term_seled[0:term_seled.find('|')]
        term_seled_cn = term_seled[term_seled.find('|') + 1:]

        df_w = pd.read_sql("select datetime," + term_seled_en + " from cw_weather where name_cn ='" +
                           city_seled[0] + "';", cw_db_engine)  # 只选第1个城市

        df_w.rename(columns={term_seled_en: city_seled[0]}, inplace=True)
        df_w['datetime'] = pd.to_datetime(df_w['datetime']).dt.date
        df_w.set_index('datetime', inplace=True)
        df_w.sort_index(inplace=True)

        if len(city_seled) >= 1:  # 如果选择的城市多于1个，将后续的城市数据连接到表后面
            city_tmp = city_seled[1:].copy()
            for ci in city_tmp:
                df_tmp = pd.read_sql("select datetime," + term_seled_en + " from cw_weather where name_cn ='" +
                                     ci + "';", cw_db_engine)
                df_tmp.rename(columns={term_seled_en: ci}, inplace=True)
                df_tmp['datetime'] = pd.to_datetime(df_tmp['datetime']).dt.date
                df_tmp.set_index('datetime', inplace=True)
                df_tmp.sort_index(inplace=True)
                df_w = df_w.join(df_tmp, how='left')
                del df_tmp
            # 创建折线图
            line_chart = create_line_chart(df_w, city_seled, term_seled_en, term_seled_cn)
            line2Html = line_chart.render_embed()  # 将折线组件转换成html文本
            line_chart.render(saved_chart_html_path)

            st.toast("图表已保存为" + saved_chart_html_path)
            components.html(line2Html, height=2000, width=3000)  # 在主页面用streamlit静态组件的方式渲染pyecharts


@app.addapp(title='城市信息', icon="🏙️")
def app3():
    # 获取全部城市数据
    df_city = pd.read_sql("select * from city order by country,province;", cw_db_engine)
    df_city['longitude'] = df_city['longitude'].astype(float)
    df_city['latitude'] = df_city['latitude'].astype(float)
    # 获取当前国家数和城市数
    country_sum = str(len(df_city['country'].unique().tolist()))
    city_sum = str(len(df_city['name_cn'].unique().tolist()))
    st.toast("当前共计 " + str(country_sum) + "个国家，" + str(city_sum) + "个城市")

    st.warning("如要修改已存在气象数据城市的名称，则必须修改数据表中相关数据行的城市名，确保名称相同。SQL语句：UPDATE cw_weather SET "
               "name_cn='XX' WHERE name_cn='XXXX'", icon="⚠️")

    st.data_editor(df_city,
                   column_config={
                       "name_cn": st.column_config.Column(
                           "城市名(中文)",
                           width="small",
                           required=True,
                       ),
                       "name_en": st.column_config.Column(
                           "城市名(英文)",
                           width="small",
                           required=True,
                       ),
                       "latitude": st.column_config.Column(
                           "纬度",
                           width="small",
                           required=True,
                       ),
                       "longitude": st.column_config.Column(
                           "经度",
                           width="small",
                           required=True,
                       ),
                       "altitude": st.column_config.Column(
                           "海拔",
                           width="small",
                           required=True,
                       ),
                       "province": st.column_config.Column(
                           "省份",
                           width="small",
                           required=True
                       ),
                       "country": st.column_config.Column(
                           "国家",
                           width="small",
                           required=True
                       ),
                       "remarks": st.column_config.Column(
                           "备注",
                           width="small",
                           required=False
                       ),
                       "position": st.column_config.Column(
                           "纬经度",
                           width="small",
                           required=True
                       ),
                       "flag": st.column_config.Column(
                           "标志",
                           width="small",
                           required=True
                       )
                   },
                   hide_index=True,
                   num_rows="dynamic",
                   key='my_data_editor',
                   use_container_width=True)

    if st.session_state['my_data_editor']:
        save_button = st.button("💾保存更新数据", disabled=False)

        if save_button:
            if st.session_state['my_data_editor']['edited_rows']:
                for row_index, row_data in st.session_state['my_data_editor'][
                    'edited_rows'].items():  # 通过edited_rows索引，遍历所修改过的行
                    for col_name, col_value in row_data.items():  # 每行发生修改的数据，根据修改项目注意给原dataframe更新赋值
                        df_city.at[int(row_index), col_name] = col_value

            df_city.drop(index=st.session_state['my_data_editor']['deleted_rows'], inplace=True)  # 删除指定数据行
            df_add = pd.DataFrame(st.session_state['my_data_editor']['added_rows'])  # 增加数据的行
            df = pd.concat([df_city, df_add], ignore_index=False)

            df.reset_index(inplace=True, drop=True)  # 重置索引，并删除原索引
            df = df[['name_cn', 'name_en', 'latitude', 'longitude', 'altitude', 'province', 'country', 'remarks',
                     'position', 'flag']]
            cw_db_engine.connect().execute(text("DROP TABLE city;"))  # 先删除书库中的表city
            df.to_sql("city", cw_db_engine, if_exists='replace', chunksize=10000)
            st.toast("数据更新成功.")
    else:
        save_button = st.button("💾保存更新数据", disabled=True)


@app.addapp(title='数据补充', icon="💽")
def app4():
    last_days = 30
    hy.info('数据源 https://www.visualcrossing.com/ 🥰  下载路径(CSV)：' + current_path + "\data_csv")

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
    list_city = []
    list_data = []
    for city_name, city_data in d_m:
        list_city.append(city_name)
        list_data.append(city_data['temp'].tolist()[-last_days:])

    dict_last_temp = dict(zip(list_city, list_data))

    # 将字典转换为列表
    data_list = [{'name_cn': k, 'list_temp': v} for k, v in dict_last_temp.items()]
    # 使用列表创建 DataFrame
    df_last_temp = pd.DataFrame(data_list)
    df_last_temp.set_index('name_cn', inplace=True)
    df_last_temp.sort_index(inplace=True)

    df_city.drop(['name_en', 'remarks', 'flag'], axis=1, inplace=True)
    df_city.set_index('name_cn', inplace=True)
    df_city.sort_index(inplace=True)

    df_city = pd.concat([df_city, df_last_temp], axis=1)
    # 给df_city按国家和省份排序
    df_city.sort_values(by=['country', 'province'], ascending=True, inplace=True)

    st.dataframe(df_city,
                 column_config={
                     "index": st.column_config.Column(
                         "索引",
                         width="small",
                         required=True,
                     ),
                     "name_cn": st.column_config.Column(
                         "城市名(中文)",
                         width="small",
                         required=True,
                     ),
                     "latitude": st.column_config.Column(
                         "纬度",
                         width="small",
                         required=True,
                     ),
                     "longitude": st.column_config.Column(
                         "经度",
                         width="small",
                         required=True,
                     ),
                     "altitude": st.column_config.ProgressColumn(
                         "海拔",
                         width="small",
                         help="海报高度",
                         format="%f",
                         min_value=0,
                         max_value=2000,
                     ),
                     "province": st.column_config.Column(
                         "省份",
                         width="small",
                         required=True
                     ),
                     "country": st.column_config.Column(
                         "国家",
                         width="small",
                         required=True
                     ),
                     "date_min": st.column_config.Column(
                         "最早",
                         width="small",
                         required=True
                     ),
                     "date_max": st.column_config.Column(
                         "最晚",
                         width="small",
                         required=True
                     ),
                     "list_temp": st.column_config.LineChartColumn(
                         "最后" + str(last_days) + "天平均气温", y_min=-20, y_max=45
                     )

                 },
                 hide_index=False,
                 height=300,
                 )

    st.write("请先到数据源下载具体城市相关日期的数据csv文件,保存csv文件到以下路径,选择后导入数据。")
    f_n_csv = st.selectbox(current_path + "\data_csv\\", os.listdir(current_path + "\\data_csv\\")[-5:])

    input_data_button = st.button("🛅导入气象数据", disabled=False)

    if input_data_button:
        fn = f_n_csv
        df_t = df_city[(df_city["position"] == fn[0:16])]
        if len(df_t) <= 0:
            st.error("没有找到该城市数据，请在city表新增后再上传文件", icon="🚨")
            st.toast('没有找到该城市数据，请在city表新增后再上传文件', icon="🚨")
            return
        else:
            d_o1 = df_t["date_min"][0]
            d_o2 = df_t["date_max"][0]
            d_n1 = datetime.datetime.strptime(fn[17:27], "%Y-%m-%d").date()
            d_n2 = datetime.datetime.strptime(fn[31:41], "%Y-%m-%d").date()

            if d_o1 <= d_n1 <= d_o2:
                st.error('日期在已有数据范围内,请重新下载', icon="🚨")
                st.toast('日期在已有数据范围内,请重新下载', icon="🚨")
                return
            elif d_o1 <= d_n2 <= d_o2:
                st.error('日期在已有数据范围内,请重新下载', icon="🚨")
                st.toast('日期在已有数据范围内,请重新下载', icon="🚨")
                return

        df1 = df_city[(df_city['position'] == fn[0:16])]
        city_name = df1.index[0]
        st.toast("正在读入[" + city_name + "]数据...")
        st.info("正在读入[" + city_name + "] " + fn[17:27] + " 至 " + fn[31:41] + " 数据...")
        df_tmp = pd.read_csv(current_path + "\\data_csv\\" + f_n_csv, parse_dates=['datetime'], index_col="datetime")
        df_tmp.sort_index(inplace=True)
        df_tmp['name_cn'] = city_name

        df_tmp.to_sql("cw_weather", cw_db_engine, index=True, if_exists='append', chunksize=10000)
        st.toast("导入[" + city_name + "] " + fn[17:27] + " 至 " + fn[31:41] + " 数据完毕...")
        st.info("导入[" + city_name + "] " + fn[17:27] + " 至 " + fn[31:41] + " 数据完毕...")
        return

@app.addapp(title='地图查询', icon="🌏")
def app5():
    # 获取全部城市数据
    df_city = pd.read_sql("select * from city order by country,province;", cw_db_engine)
    df_city['longitude'] = df_city['longitude'].astype(float)
    df_city['latitude'] = df_city['latitude'].astype(float)
    df_city['altitude'] = df_city['altitude'].astype(float)

    location_list = df_city[['name_cn', 'longitude', 'latitude']].values.tolist()
    altitude_list = df_city[['name_cn','altitude']].values.tolist()
    # 创建一个 Geo 图表
    geo = Geo(init_opts=opts.InitOpts(width="1900px", height="700px"))
    # 添加地图类型
    geo.add_schema(maptype="world",center=[100.7830, 22],zoom=2)  # 西双版纳为中心视角

    # 遍历经纬度数据框，并将经纬度添加到地图上
    for name,longitude,latitude in location_list:
        geo.add_coordinate(name,longitude,latitude)

    # 遍历海报数据框，并将经纬度添加到地图上
    da_geo = []
    for name,altitude in altitude_list:
        da_geo.append((name,altitude))

    # # 添加坐标点
    # geo.add_coordinate("北京", 116.46, 39.92)
    # geo.add_coordinate("上海", 121.46, 31.22)
    # geo.add_coordinate("长春", 125.2532,43.8674)
    #
    # 添加数据
    # data_pair = [("北京", 1), ("上海", 31),("长春", 31)]
    data_pair = da_geo
    # 绘制散点图
    geo.add("", data_pair, type_=ChartType.EFFECT_SCATTER, symbol_size=10)
    # 设置全局配置项
    geo.set_global_opts(title_opts=opts.TitleOpts(title="城市(海拔)-散点图"))
    # 渲染图表
    # geo.render()
    Map22Html = geo.render_embed()  # 将折线组件转换成html文本
    # c.render(saved_map_html_path)

    components.html(Map22Html, height=2000, width=5000)  # 在主页面用streamlit静态组件的方式渲染pyecharts






# Run the whole lot, we get navbar, state management and app isolation, all with this tiny amount of work.
app.run()
