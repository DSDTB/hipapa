import streamlit as st

# from st_pages import show_pages_from_config, add_page_title, hide_pages, add_indentation
from apps.db_fxns import *
import streamlit_book as stb


def menu_logined():
    # Streamit book properties
    stb.set_book_config(
        menu_title="电网调度111",
        menu_icon="info-square",
        options=["登录", "维护变电站","维护物料卡", "关于"],
        paths=["apps/login.py", "apps/classroom.py", "apps/memcard.py","apps/trial.py"],
        icons=[
            "code",
            "bank",
            "bank2",
            "robot",
        ],
    )


def is_login():
    if "username" not in st.session_state:
        st.warning("请先登录")
        # menu_login()
        return False
    elif st.session_state.username == "":
        st.warning("请先登录")
        # menu_login()
        return False
    else:
        return True


def dm_login(c):
    st.title("电网调度优化策略应用")

    st.subheader("登录应用")
    if "username" in st.session_state:
        if st.session_state.username:
            st.success(f"您已登录{st.session_state.username}")
            st.stop()
    #     placeholder = st.sidebar.empty()
    placeholder = st.empty()
    ct1 = placeholder.container()
    frm = ct1.form("login")

    username = frm.text_input("用户名")
    password = frm.text_input("密码", type="password")

    if frm.form_submit_button("登录"):
        create_usertable(c)
        result = login_user(username, password, c)

        if result:
            st.session_state.username = username
            st.success("{} 登录系统！欢迎您！ ".format(username))
            placeholder.empty()

            # menu_logined()

        else:
            st.session_state.username = ""
            st.warning("用户名或者密码错误！")
            # placeholder.empty()
            # menu_login()
