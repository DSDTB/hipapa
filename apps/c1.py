import streamlit as st
from apps.db_fxns import *
from datetime import *
import pandas as pd
from apps import *

#####check login or not
# if not is_login():
#     st.stop()
# conn = sqlite3.connect('data.db') #user sqlite3 Engine
# user SQLAlchemy Engine
# df = all_card_df(conn.engine)

conn = st.connection("data_db", type="sql", url="sqlite:///data.db")

def test_fun(_c):
    df=_c.query("select * from tb_card")
    return df   

def do_test():
    message=test_fun(conn)
    st.info(message)
    
do_test()

# rooms_df = op_room_df(conn)
# op_dict = dict(zip(rooms_df["bm"], rooms_df["mc"]))
# # op_dict=create_dict()
# op_dict_vk = {v: k for k, v in op_dict.items()}
# 
# op_rms = [k for k in op_dict.values()]
# op_bm = [k for k in op_dict.keys()]
# st.write(op_rms, op_bm)
# 
# 
# df = all_card_df(conn)
# df["sdate"] = pd.to_datetime(df["sdate"])
# df["flag"] = df["flag"].astype("bool")
# df["room"] = df["room"].replace(op_dict)
# def gen_data():
#     
#     df=test_fun(conn)
#     df["sdate"] = pd.to_datetime(df["sdate"])
#     df["flag"] = df["flag"].astype("bool")
# 
#     df["room"] = df["room"].replace(op_dict)
# 
# #df=gen_data()
# data = st.data_editor(
#     data=df,
#     width=1200,  # 数据表宽度
#     height=200,  # 数据表高度
#     use_container_width=True,  # 全宽
#     hide_index=True,  # 是否隐藏索引列
#     column_order=None,  # 指定列的显示顺序
#     column_config={
#         "bm": st.column_config.TextColumn(
#             label="物料编码",  # 别名
#             width="medium",  # 宽度
#             help="物料编码",  # 帮助信息
#             disabled=True,  # 禁用列编辑
#             required=True,  # 必填
#             default="m" + str(datetime.now().timestamp()),  # 新增行时的默认值
#         ),
#         "cname": st.column_config.Column(
#             label="姓名", width=None, help="学员姓名", disabled=False, required=True
#         ),
#         "pname": st.column_config.Column(
#             label="父母姓名", width=None, help="父母姓名", disabled=False, required=True
#         ),
#         "phone": st.column_config.Column(
#             label="联系方式", width=None, help="联系方式", disabled=False, required=True
#         ),
#         "room": st.column_config.SelectboxColumn(
#             label="库房",  # 别名
#             width="medium",  # 宽度
#             help="库房",  # 帮助信息
#             disabled=False,  # 禁用列编辑
#             required=True,  # 必填
#             default="请选择...",  # 新增行时的默认值
#             options=op_rms,
#         ),
#         "cs": st.column_config.Column(
#             label="次数", width=None, help="次数", disabled=False, required=True
#         ),
#         "sdate": st.column_config.DateColumn(
#             label="开始时间",  # 别名
#             width="medium",  # 宽度
#             help="开始时间",  # 帮助信息
#             disabled=False,  # 禁用列编辑
#             required=True,  # 必填
#             default=date.today(),  # 新增行时的默认值；这里暂时不能使用动态值
#             format="YYYY-MM-DD",  # 格式化
#             #             min_value=date(1980,1,1),  # 最小日期时间值
#             #             max_value=date(2024,1,1),  # 最大日期时间值
#             step=1,  # 步长
#         ),
#         "edate": st.column_config.Column(
#             label="结束时间", width=None, help="结束时间", disabled=False, required=True
#         ),
#         "delay": st.column_config.Column(
#             label="延期时间", width=None, help="延期时间", disabled=False, required=False
#         ),
#         "detimes": st.column_config.Column(
#             label="延期次数", width="small", help="延期次数", disabled=False, required=False
#         ),
#         "flag": st.column_config.Column(
#             label="是否生效", width="small", help="是否生效", disabled=False, required=True
#         ),
#         "url": st.column_config.Column(
#             label="网址", width=None, help="描述网址", disabled=False, required=False
#         ),
#     },  # 配置列的显示方式
#     num_rows="dynamic",  # 可添加和删除行
#     disabled=False,  # 禁用编辑
#     key="card",  #
#     #on_change=test_onChange,  # 回调函数
# )
# st.write(st.session_state.card)
# st.write(data["room"].replace(op_dict_vk))

