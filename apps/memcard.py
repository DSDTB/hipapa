import streamlit as st
from apps.db_fxns import *
from datetime import *
import pandas as pd
import streamlit_antd_components as sac
import os


def app():
    #####check login or not
    # if not is_login():
    #     st.stop()

    # st sql conneciton: query->df,connection->sa_conn,reset;session,engin,driver
    st_conn = st.connection("data_db", type="sql", url="sqlite:///data.db")

    # conn = st_conn.engine.connect()
    conn = st_conn.connect()

    def get_pre():
        st.session_state["pre"] = page_num
        if st.session_state.pre != st.session_state.cmpage:
            # st.write(str(st.session_state.pre) +' ' +str(st.session_state.cmpage))
            data.to_sql("tb_card_df", con=conn, if_exists="replace", index=False)
            update_card_df(conn)


    @st.cache_data()
    def op_dict():
        rooms_df = op_room_df(conn)
        op_dict = dict(zip(rooms_df["bm"], rooms_df["mc"]))
        op_dict_vk = {v: k for k, v in op_dict.items()}
        op_rms = [k for k in op_dict.values()]
        return op_dict, op_dict_vk, op_rms

    op_dict, op_dict_vk, op_rms = op_dict()

    @st.cache_data()
    def create_data(s):
        #df = all_card_df(conn)
        df=focus_card_df(conn,s)
        if not df.empty:
            df["sdate"] = pd.to_datetime(df["sdate"])
            df["flag"] = df["flag"].astype("bool")
            df["room"] = df["room"].replace(op_dict)
        return df
    
    # @st.cache_data()
    def create_all_data():
        df = all_card_df(conn)
        #df=focus_card_df(conn,s)
        if not df.empty:
            df["sdate"] = pd.to_datetime(df["sdate"])
            df["flag"] = df["flag"].astype("bool")
            df["room"] = df["room"].replace(op_dict)
        return df

    def format_option(option):
        return f"{op_dict[option]}"

    def card_editor(df_cs, op_rms, key):
        data = st.data_editor(
            data=df_cs,
            width=1200,  # 数据表宽度
            height=300,  # 数据表高度
            use_container_width=True,  # 全宽
            hide_index=True,  # 是否隐藏索引列
            column_order=None,  # 指定列的显示顺序
            column_config={
                "bm": st.column_config.TextColumn(
                    label="物料编码",  # 别名
                    width=None,  # 宽度
                    help="物料编码",  # 帮助信息
                    disabled=True,  # 禁用列编辑
                    required=True,  # 必填
                    # default="m" + str(datetime.now().timestamp()),  # 新增行时的默认值
                ),
                "cname": st.column_config.Column(
                    label="姓名", width=None, help="学员姓名", disabled=False, required=True
                ),
                "pname": st.column_config.Column(
                    label="父母姓名", width=None, help="父母姓名", disabled=False, required=True
                ),
                "phone": st.column_config.Column(
                    label="联系方式", width=None, help="联系方式", disabled=False, required=True
                ),
                "room": st.column_config.SelectboxColumn(
                    label="库房",  # 别名
                    width=None,  # 宽度
                    help="库房",  # 帮助信息
                    disabled=False,  # 禁用列编辑
                    required=True,  # 必填
                    default="请选择...",  # 新增行时的默认值
                    options=op_rms,
                    # options=[1,2,3,4],
                ),
                "cs": st.column_config.Column(
                    label="次数", width=None, help="次数", disabled=False, required=False
                ),
                "sdate": st.column_config.DateColumn(
                    label="开始时间",  # 别名
                    width=None,  # 宽度
                    help="开始时间",  # 帮助信息
                    disabled=False,  # 禁用列编辑
                    required=True,  # 必填
                    # default=date.today(),  # 新增行时的默认值；这里暂时不能使用动态值
                    format="YYYY-MM-DD",  # 格式化
                    #             min_value=date(1980,1,1),  # 最小日期时间值
                    #             max_value=date(2024,1,1),  # 最大日期时间值
                    step=1,  # 步长
                ),
                "edate": st.column_config.Column(
                    label="结束时间",
                    width=None,
                    help="结束时间",
                    disabled=False,
                    required=False,
                ),
                "delay": st.column_config.Column(
                    label="延期时间",
                    width=None,
                    help="延期时间",
                    disabled=False,
                    required=False,
                ),
                "detimes": st.column_config.Column(
                    label="延期次数",
                    width=None,
                    help="延期次数",
                    disabled=False,
                    required=False,
                ),
                "flag": st.column_config.Column(
                    label="是否生效",
                    width=None,
                    help="是否生效",
                    disabled=False,
                    required=False,
                ),
                "url": st.column_config.Column(
                    label="网址", width=None, help="描述网址", disabled=False, required=False
                ),
            },  # 配置列的显示方式
            # num_rows="dynamic",  # 可添加和删除行
            disabled=False,  # 禁用编辑
            key=key,  #
            # on_change=card_df_tab(),  # 回调函数
        )
        return data

    def gen_bm():
        now = datetime.now()
        code_str = now.strftime("%Y%m%d%H%M%S")
        bm = "m" + code_str
        return bm

    tab1, tab2, tab3 = st.tabs(["添加", "导入", "修改"])

    with tab1:
        with st.form("add_form", clear_on_submit=True):
            col_rm1, col_rm2, col_rm3 = st.columns(3)
            bm = col_rm1.text_input("编码", value=gen_bm(), disabled=True)
            col_rm2.text_input("占位1", disabled=True, label_visibility="hidden")
            col_rm3.text_input("占位2", disabled=True, label_visibility="hidden")
            cname = col_rm1.text_input("学员姓名")
            pname = col_rm2.text_input("家长姓名")
            phone = col_rm3.text_input("手机号码", max_chars=11)
            room = col_rm1.selectbox("教室", options=op_dict, format_func=format_option)
            cs = col_rm2.number_input("次数", value=30)
            sdate = col_rm3.date_input("开始时间", value=date.today(), format="YYYY-MM-DD")
            edate = col_rm1.date_input("结束时间", value=date.today(), format="YYYY-MM-DD")

            submitted = st.form_submit_button("添加")
            if submitted:
                try:
                    add_card(bm, cname, pname, phone, room, cs, sdate, edate, conn)
                    st.info(f"你添加了学员{cname}，所选科目{op_dict[room]}，开始时间是{sdate}")

                except Exception as e:
                    st.write(e)
    with tab2:
        try:
            uploaded_file = st.file_uploader("请上传要导入的.csv文件", type="csv")
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                num_rows = df.shape[0]
                l_bm = [gen_bm()[:14] + str(i) for i in range(num_rows)]

                df.loc[:, "bm"] = l_bm
                df["sdate"] = pd.to_datetime(df["sdate"])
                df["sdate"] = df["sdate"].dt.date
                df["flag"] = df["flag"].astype("bool")
                df["phone"] = df["phone"].astype("str")
                df["room"] = df["room"].replace(op_dict)
                st.write(df)

                # data=card_editor(df,op_rms,"card1")
                ph=st.empty()
                if ph.button("保存", key="batch"):
                    df.to_sql("tb_card_df", con=conn, if_exists="replace", index=False)
                    batch_card_df(conn)
                    st.info("您的数据已导入！")
                    ph.empty()
                    #st.rerun()

        except Exception as e:
            st.error("文件不规范，请重新上传！")
    with tab3:
        
        st.empty().text("")

        cdt=st.text_input("请输入姓名或手机号")
        #if st.button("查询"):
#         df_focus=create_data(cdt)
#         data = card_editor(df_focus, op_rms, "card3")


        if "pre" not in st.session_state:
            st.session_state["pre"] = 1
        if "cmpage" not in st.session_state:
            st.session_state["cmpage"] = 1

        if "page" not in st.session_state:
            st.session_state["page"] = 1
        else:
            st.session_state["page"] = st.session_state.cmpage

        page = st.session_state.page

        page = page  # 页码数
        limit =  80 # 每页的数据量
        
        

        df = create_data(cdt)
        data_page = df[(int(page) - 1) * int(limit) : (int(page) * int(limit))]

        if not data_page.empty:
            data = card_editor(data_page, op_rms, "card2")
            data["sdate"] = data["sdate"].dt.date

            data["room"] = data["room"].replace(op_dict_vk)
            page_num = sac.pagination(
                total=len(df),
                page_size=80,
                align="end",
                jump=True,
                show_total=True,
                on_change=get_pre,
                key="cmpage",
            )
            
            if st.button("保存"):
                data.to_sql("tb_card_df", con=conn, if_exists="replace", index=False)
                update_card_df(conn)


