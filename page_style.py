import streamlit as st

# Okabe-Ito / colour-vision-deficiency-friendly palette
CVD_BLUE = "#0072B2"
CVD_ORANGE = "#E69F00"
CVD_GREEN = "#009E73"
CVD_VERMILLION = "#D55E00"
CVD_PURPLE = "#CC79A7"
CVD_SKY = "#56B4E9"
CVD_YELLOW = "#F0E442"
CVD_GREY = "#999999"
CVD_BLACK = "#000000"

# This is the date documented in the shared Epoch snapshot used by the app.
# Update this constant if the committed source snapshots are refreshed again.
LAST_DATA_REFRESH = "25 October 2026"


def analysis_header(title, contributor, focus, description=None):
    st.title(title)
    st.caption(f"Main contribution: {contributor}")
    st.markdown(f"**Question:** {focus}")
    if description:
        st.write(description)
    st.divider()


def interpretation(text):
    st.markdown(f"**Interpretation:** {text}")


def page_takeaway(text):
    st.divider()
    st.subheader("Page takeaway")
    st.markdown(text)


def limitations(items):
    st.subheader("Limitations")
    for item in items:
        st.markdown(f"- {item}")


def page_footer(source, refresh=LAST_DATA_REFRESH):
    st.divider()
    st.caption(f"Source: {source} | Last data refresh: {refresh}")
