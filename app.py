import streamlit as st
from urls import download_video_based_on_url

st.set_page_config(layout="wide") # Optional: use wide layout

pages = [
    st.Page("pages/download_url.py", title="Download from URL", icon='⬇️'),
    st.Page("pages/supported_sites.py", title="Supported Sites", icon='🔗'),
    #st.Page("pages/bilibili.py", title="Bilibili", icon='📺'),
    #st.Page("pages/youtube.py", title="Youtube", icon='▶️'),
]

pg = st.navigation(pages, position="top") # Position the navbar at the top
pg.run()
