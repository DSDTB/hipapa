import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
from streamlit.source_util import get_pages

# add_page_title()

st.write("This is just a sample page!trial")

if "trial" not in st.session_state:
    st.session_state.trial='just for try!'

st.write(st.session_state)
