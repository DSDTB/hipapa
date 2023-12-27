import streamlit as st
from apps.db_fxns import *
from datetime import *
import pandas as pd

# import pygwalker as pyg
import streamlit.components.v1 as components
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html


def app():
    #####check login or not
    # if not is_login():
    #     st.stop()

    # st sql conneciton: query->df,connection->sa_conn,reset;session,engin,driver
    st_conn = st.connection("data_db", type="sql", url="sqlite:///data.db")

    # conn = st_conn.engine.connect()
    conn = st_conn.connect()

    # vis_spec = r"""{"config":[{"config":{"defaultAggregated":true,"geoms":["bar"],"coordSystem":"generic","limit":-1},"encodings":{"dimensions":[{"dragId":"gw_rWJn","fid":"cname","name":"cname","basename":"cname","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_DP3B","fid":"pname","name":"pname","basename":"pname","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_M973","fid":"phone","name":"phone","basename":"phone","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_CT2T","fid":"room","name":"room","basename":"room","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_zUAZ","fid":"sdate","name":"sdate","basename":"sdate","semanticType":"temporal","analyticType":"dimension"},{"dragId":"gw_NFEO","fid":"edate","name":"edate","basename":"edate","semanticType":"temporal","analyticType":"dimension"},{"dragId":"gw_u6Sg","fid":"delay","name":"delay","basename":"delay","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_d55C","fid":"detimes","name":"detimes","basename":"detimes","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_Fnwa","fid":"flag","name":"flag","basename":"flag","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_6VFf","fid":"url","name":"url","basename":"url","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_mea_key_fid","fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"}],"measures":[{"dragId":"gw_8vx5","fid":"cs","name":"cs","basename":"cs","semanticType":"quantitative","analyticType":"measure"},{"dragId":"gw_d4h2","fid":"bm","name":"bm","basename":"bm","semanticType":"nominal","analyticType":"measure"},{"dragId":"gw_count_fid","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"dragId":"gw_mea_val_fid","fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"dragId":"gw_uuAD","fid":"bm","name":"bm","basename":"bm","semanticType":"nominal","analyticType":"measure","aggName":"count"}],"columns":[{"dragId":"gw_Mbh9","fid":"room","name":"room","basename":"room","semanticType":"nominal","analyticType":"dimension"}],"color":[{"dragId":"gw_EZ1p","fid":"room","name":"room","basename":"room","semanticType":"nominal","analyticType":"dimension"}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":true,"zeroScale":true,"size":{"mode":"fixed","width":404,"height":297},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_5Ztq","name":"Chart 1"}],"chart_map":{},"workflow_list":[{"workflow":[{"type":"view","query":[{"op":"aggregate","groupBy":["room"],"measures":[{"field":"bm","agg":"count","asFieldKey":"bm_count"}]}]}]}],"timezoneOffsetSeconds":28800,"version":"0.3.17"}"""

    @st.cache_data()
    def op_dict():
        rooms_df = op_room_df(conn)
        op_dict = dict(zip(rooms_df["bm"], rooms_df["mc"]))
        op_dict_vk = {v: k for k, v in op_dict.items()}
        op_rms = [k for k in op_dict.values()]
        return op_dict, op_dict_vk, op_rms

    op_dict, op_dict_vk, op_rms = op_dict()

    #@st.cache_data()
    #@st.cache_resource()
    def create_data():
        df = all_card_df(conn)
        if not df.empty:
            df["sdate"] = pd.to_datetime(df["sdate"])
            df["sdate"] = df["sdate"].dt.date
            df["edate"] = pd.to_datetime(df["edate"])
            df["edate"] = df["edate"].dt.date
            df["flag"] = df["flag"].astype("bool")
            df["room"] = df["room"].replace(op_dict)
        return df

    vis_spec = r"""{"config":[{"config":{"defaultAggregated":true,"geoms":["bar"],"coordSystem":"generic","limit":-1},"encodings":{"dimensions":[{"dragId":"gw_2qim","fid":"cname","name":"cname","basename":"cname","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_NN3h","fid":"pname","name":"pname","basename":"pname","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_Ohh9","fid":"phone","name":"phone","basename":"phone","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_qb_d","fid":"room","name":"room","basename":"room","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_lPhD","fid":"cs","name":"cs","basename":"cs","semanticType":"quantitative","analyticType":"dimension"},{"dragId":"gw_143F","fid":"sdate","name":"sdate","basename":"sdate","semanticType":"temporal","analyticType":"dimension"},{"dragId":"gw_5h5y","fid":"edate","name":"edate","basename":"edate","semanticType":"temporal","analyticType":"dimension"},{"dragId":"gw_aYJE","fid":"delay","name":"delay","basename":"delay","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_CnVB","fid":"detimes","name":"detimes","basename":"detimes","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_oMYe","fid":"flag","name":"flag","basename":"flag","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_Kl7r","fid":"url","name":"url","basename":"url","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_mea_key_fid","fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"}],"measures":[{"dragId":"gw_U78X","fid":"bm","name":"bm","basename":"bm","semanticType":"nominal","analyticType":"measure"},{"dragId":"gw_count_fid","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"dragId":"gw_mea_val_fid","fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"dragId":"gw_M6uf","fid":"bm","name":"bm","basename":"bm","semanticType":"nominal","analyticType":"measure","aggName":"count"}],"columns":[{"dragId":"gw_a-We","fid":"room","name":"room","basename":"room","semanticType":"nominal","analyticType":"dimension"}],"color":[{"dragId":"gw_Ot5u","fid":"room","name":"room","basename":"room","semanticType":"nominal","analyticType":"dimension"}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"fixed","width":415,"height":385},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_sAwh","name":"Chart 1"}],"chart_map":{},"workflow_list":[{"workflow":[{"type":"view","query":[{"op":"aggregate","groupBy":["room"],"measures":[{"field":"bm","agg":"count","asFieldKey":"bm_count"}]}]}]}],"timezoneOffsetSeconds":28800,"version":"0.3.17"}"""

    # 初始化pygwalker通信
    init_streamlit_comm()

    # 当使用`use_kernel_calc=True`时，应该缓存pygwalker的html代码，以防止内存溢出。
    @st.cache_resource
    def get_pyg_html(df: pd.DataFrame) -> str:
        # 当你需要发布你的应用程序时，设置`debug=False`，防止其他用户更改配置文件。
        # 如果想使用保存图表配置的功能，将`debug=True`
        html = get_streamlit_html(df, spec=vis_spec, use_kernel_calc=True, debug=False)
        return html

    #     @st.cache_data
    #     def get_df() -> pd.DataFrame:
    #         return pd.read_csv("/bike_sharing_dc.csv")

    df = create_data()

    components.html(get_pyg_html(df), width=1300, height=1000, scrolling=True)
