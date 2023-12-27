import streamlit as st
from apps.dm_fxns import *

def app():

    # Create the SQL connection to data_db as specified in your secrets file.
    conn = st.connection('data_db', type='sql',url = "sqlite:///data.db")
    with conn.session as c:
            dm_login(c)



