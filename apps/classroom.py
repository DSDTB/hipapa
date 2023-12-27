import streamlit as st
from apps.dm_fxns import *
from streamlit_modal import Modal

def app():

    conn = st.connection("data_db", type="sql", url="sqlite:///data.db")
    # 定义modal
    my_modal = Modal(title="删除确认", key="modal_key", max_width=200)

    # 使用session_state来判断modal里的确定按钮是否被点击
    if "confirm" not in st.session_state:
        st.session_state["confirm"] = False


    # 回调函数，将session_state置为True
    def del_btn_click():
        st.session_state["confirm"] = True


    if not is_login():
        st.stop()

    tab1, tab2 = st.tabs(["添加", "修改或删除"])

    with tab1:
        st.header("A cat")
        with st.form("add_form", clear_on_submit=True):
            col_rm1, col_rm2 = st.columns(2)
            bm = col_rm1.text_input("编码")
            mc = col_rm2.text_input("教室名称")
            qy = col_rm1.text_input("教室区域")
            rs = col_rm2.number_input("容纳人数", value=10)
            bz = col_rm1.text_input("教室设施")
            submitted = st.form_submit_button("添加")
            if submitted:
                if not bm.strip():
                    st.warning("编码不能为空！")
                else:
                    try:
                        with conn.session as c:
                            create_room(c)
                            add_room(bm, mc, qy, rs, bz, c)

                    except Exception as e:
                        st.write(e)

    with tab2:
        st.header("A dog")
        col_bm1, col_bm2 = st.columns(2)

        try:
            with conn.session as c:
                all_room1 = all_room(c)

                options = [op[0] for op in all_room1]
                bm = col_bm1.selectbox("教室编码", options)

                record = qry_room(bm, c)

                mc = col_bm2.text_input("教室名称", record[0][1])
                qy = col_bm1.text_input("教室区域", record[0][2])
                rs = col_bm2.number_input("容纳人数", value=record[0][3])
                bz = col_bm1.text_input("教室设施", record[0][4])
        except Exception as e:
            st.write(e)

        cc1, cc2 = col_bm1.columns(2)
        change = cc1.button("更改")
        delete = cc2.button("删除", key="del_btn")
        if change:
            list1 = [mc, qy, rs, bz]
            list2 = [record[0][1], record[0][2], record[0][3], record[0][4]]
            if list1 == list2:
                st.info("内容没有改变")
                st.stop()
            try:
                with conn.session as c:
                    change_room(bm, mc, qy, rs, bz, c)
                    st.warning(f"编码为{bm}的教室已更新保存！")
            except Exception as e:
                st.write(e)
            # st.experimental_rerun() # 重刷页面

        # 如果删除按钮被点击，就进行弹窗
        if delete:
            with my_modal.container():
                st.markdown("确定删除此内容？")
                # 定义一个确定按钮，注意key值为指定的session_state，on_click调用回调函数改session_state的值
                st.button("确定", key="confirm", on_click=del_btn_click)

        # 这里通过session_state判断弹窗里的确定按钮被点击了，就进行你想要的逻辑操作。
        if st.session_state["confirm"]:
            # 删除内容
            try:
                with conn.session as c:
                    delete_room(bm, c)
                    st.warning(f"已删除编码为{bm}的教室！")
            except Exception as e:
                st.write(e)
            st.session_state["confirm"] = False  # 恢复session_state为False
            st.experimental_rerun()  # 重刷页面
