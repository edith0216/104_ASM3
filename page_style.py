import streamlit as st


def analysis_header(title, contributor, focus):
    st.set_page_config(page_title=title, layout="wide", page_icon="🤖")
    st.title(title)
    st.caption(f"Primary contributor: {contributor}")
    st.divider()
    st.markdown(f"**Research focus:** {focus}")
