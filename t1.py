import streamlit as st
import pandas as pd
import numpy as np
import random
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import Kline
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import matplotlib.pyplot as plt

# import numpy as np

import random


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


random_color()  # (120, 200, 80)
