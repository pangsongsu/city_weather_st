import random
import pandas as pd
import streamlit as st
import openpyxl

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)

a=df['views_history'][0]
print(a)
print(type(df['views_history'][0]))


# print(df)
# df.to_excel("test.xlsx", index=False)
# st.dataframe(
#     df,
#     column_config={
#         "name": "App name",
#         "stars": st.column_config.NumberColumn(
#             "Github Stars",
#             help="Number of stars on GitHub",
#             format="%d ⭐",
#         ),
#         "url": st.column_config.LinkColumn("App URL"),
#         "views_history": st.column_config.LineChartColumn(
#             "Views (past 30 days)", y_min=0, y_max=5000
#         ),
#     },
#     hide_index=True,
# )