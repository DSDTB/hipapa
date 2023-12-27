
import streamlit as st
from streamlit_option_menu import option_menu
from apps import login,classroom,memcard,memfx

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = [
    {"func": login.app, "title": "登录", "icon": "house"},
    {"func": classroom.app, "title": "维护变电站", "icon": "map"},
    {"func": memcard.app, "title": "维护卡片", "icon": "cloud-upload"},
    {"func": memfx.app, "title": "数据分析", "icon": "cloud-upload"},
    {"func": login.app, "title": "关于", "icon": "cloud"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "电网调度",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("关于")
    st.sidebar.info(
        """
        共筑智能坚强电网
    """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break




