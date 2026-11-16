import streamlit as st


# --------------------------------------------------
# CVD-friendly colour palette
# Okabe-Ito style colours
# --------------------------------------------------

CVD_BLUE = "#0072B2"
CVD_ORANGE = "#E69F00"
CVD_GREEN = "#009E73"
CVD_VERMILLION = "#D55E00"
CVD_PURPLE = "#CC79A7"
CVD_SKY = "#56B4E9"
CVD_YELLOW = "#F0E442"
CVD_GREY = "#999999"
CVD_BLACK = "#000000"


# --------------------------------------------------
# Data refresh date
# --------------------------------------------------

LAST_DATA_REFRESH = "25 October 2026"


# --------------------------------------------------
# Shared page header
# --------------------------------------------------

def analysis_header(
    title,
    contributor,
    focus,
    description=None
):
    st.title(title)

    st.caption(
        f"Main contribution: {contributor}"
    )

    st.markdown(
        f"**Question:** {focus}"
    )

    if description:
        st.write(description)

    st.divider()


# --------------------------------------------------
# Interpretation
# --------------------------------------------------

def interpretation(text):
    st.markdown(
        f"**Interpretation:** {text}"
    )


# --------------------------------------------------
# Page takeaway
# --------------------------------------------------

def page_takeaway(text):
    st.divider()

    st.subheader("Page takeaway")

    st.markdown(text)


# --------------------------------------------------
# Limitations
# --------------------------------------------------

def limitations(items):
    st.subheader("Limitations")

    for item in items:
        st.markdown(
            f"- {item}"
        )


# --------------------------------------------------
# Source + refresh
# --------------------------------------------------

def page_footer(
    source,
    refresh=LAST_DATA_REFRESH
):
    st.divider()

    st.caption(
        f"Source: {source} | "
        f"Last data refresh: {refresh}"
    )