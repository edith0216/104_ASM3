import streamlit as st
import pandas as pd
from concentration import explode_credit, metrics_by_window, resolve_columns
from data import load_frontier_data, load_notable_data

st.set_page_config(
    page_title="AI Concentration Explorer",
    page_icon="🤖",
    layout="wide")

# Title
st.title("AI Concentration Explorer")

st.markdown(
    """
    An interactive data narrative exploring concentration in influential AI development.
    """)

st.divider()


# Research Question
st.subheader("Research question")

st.markdown(
    """
    **Is influential AI model development concentrated in fewer organisations?**
    """)

st.divider()


# Group Members
st.subheader("Group members")

st.markdown(
    """
    - **Menghan Sun** — Organisation concentration
    - **Aarushi** — Concentration dynamics
    - **Adarsh Kumbhar** — Academia to industry shift
    - **Akash** — Access concentration
    """)

st.divider()


# Persona
st.subheader("Persona")

st.markdown(
    """
    **Technology Policy Analyst**

    This app helps a technology policy analyst understand whether influential
    AI development is becoming concentrated across organisations, sectors, and model access.
    """)

st.divider()


# Four Analytical Lenses

st.subheader("Four ways to examine concentration")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 1. Organisation")
    st.write("Are a small number of organisations responsible for a large share of frontier AI model development?")
    
    st.caption("Primary contributor: Menghan")
    st.page_link("pages/Organisation_Concentration.py", label="Explore organisation")

with col2:
    st.markdown("### 2. Sector")
    st.write("Has notable AI model development shifted from academia towards industry?")
    st.caption("Primary contributor: Adarsh Kumbhar")
    st.page_link("pages/Sector_Shift.py", label="Explore sector")

with col3:
    st.markdown("### 3. Access")
    st.write("Is access to influential AI models becoming more concentrated behind company APIs and hosted services?")
    st.caption("Primary contributor: Akash")
    st.page_link("pages/Access_Concentration.py", label="Explore access")

with col4:
    st.markdown("### 4. Dynamics")
    st.write("How does organisational concentration change with time and counting choices?")
    st.caption("Primary contributor: Aarushi")
    st.page_link("pages/Concentration_Dynamics.py", label="Explore dynamics")

st.divider()


# Overall

st.subheader("Overall")

st.markdown(
    """
    Influential AI development shows several forms of concentration.

    A small group of organisations often accounts for a large share of frontier
    model development, while notable AI model development has shifted strongly
    towards industry.

    Closed API access has also become more common, although open-weight models
    remain important at the high-compute frontier.

    **Overall, influential AI development is increasingly centred around industry
    and a relatively small group of leading organisations, but concentration does
    not increase in the same way across every year or access model.**
    """
)

st.divider()


# Key Findings
st.subheader("Key findings")

@st.cache_data
def key_findings():
    frontier = load_frontier_data()
    notable = load_notable_data()

    # Frontier Top-3 share: 2-year window, parent roll-up, fractional credit
    cols = resolve_columns(frontier)
    credit = explode_credit(frontier, cols, roll_up=True)
    latest = metrics_by_window(credit, top_n=3, window=2).iloc[-1]

    notable = notable.copy()
    notable["Year"] = pd.to_datetime(notable["Publication date"], errors="coerce").dt.year

    def industry_only(raw):
        labels = {x.strip() for x in str(raw).split(",") if x.strip() and x.strip() != "nan"}
        return labels == {"Industry"}

    ind_2014 = notable.loc[notable["Year"] == 2014, "Organization categorization"].apply(industry_only)
    ind_2024 = notable.loc[notable["Year"] == 2024, "Organization categorization"].apply(industry_only)

    access = notable.loc[notable["Year"] == 2024, "Model accessibility"].astype(str)
    labelled = access.str.startswith("Open weights") | access.isin(
        ["API access", "Hosted access (no API)", "Unreleased"])
    closed = access.isin(["API access", "Hosted access (no API)"])[labelled]

    return {
        "window": latest["window"],
        "top3_share": latest["top_n_share"],
        "top3_credit": latest["top_n_share"] * latest["models"],
        "frontier_models": int(latest["models"]),
        "ind_2014": ind_2014.mean(),
        "ind_2024": ind_2024.mean(),
        "ind_n": int(ind_2024.sum()),
        "n_2024": len(ind_2024),
        "closed_2024": closed.mean(),
        "closed_n": int(closed.sum()),
        "labelled_n": int(labelled.sum()),
    }


k = key_findings()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Latest frontier Top-3 share",
        value=f"{k['top3_share']:.1%}"
    )
    st.caption(
        f"Top three organisations received {k['top3_credit']:.0f} of {k['frontier_models']} "
        f"model-credit units in the {k['window']} window (fractional attribution, parent roll-up)."
    )

with col2:
    st.metric(
        label="Industry-only share in 2024",
        value=f"{k['ind_2024']:.1%}"
    )
    st.caption(
        f"Industry-only notable models increased from {k['ind_2014']:.1%} in 2014 "
        f"to {k['ind_2024']:.1%} in 2024 ({k['ind_n']} of {k['n_2024']} models)."
    )

with col3:
    st.metric(
        label="Closed/API share in 2024",
        value=f"{k['closed_2024']:.1%}"
    )
    st.caption(
        f"Closed API or hosted access increased from 0.0% in 2019 "
        f"to {k['closed_2024']:.1%} in 2024 ({k['closed_n']} of {k['labelled_n']} labelled models)."
    )

st.divider()


# 8. Important Nuance / Limitations
st.subheader("Important nuance")

st.info(
    """
    These analyses measure different aspects of concentration.

    Organisation concentration shows **who builds the models**.

    Sector analysis shows **whether development is mainly happening in
    industry or academia**.

    Access analysis shows **how models are made available to users**.

    Concentration dynamics shows **how concentration changes across time and measurement choices**.

    These measures are related, but they are not the same thing.
    """
)

st.markdown(
    """
    **Limitations**

    - Model counts do not directly measure capability, market power, revenue,
      or research quality.
    - A higher industry share does not necessarily mean fewer organisations
      are participating.
    - More closed API access does not necessarily mean model development itself
      is more concentrated.
    - The organisation analysis and the ≥1e23 FLOP analysis use different
      definitions of the AI frontier.
    """
)

st.divider()


# Sources + Refresh
st.caption(
    """
    **Sources:** Epoch AI Frontier Models, Epoch AI Notable Models,
    and Stanford AI Index 2025  
    **Data:** Committed local snapshots in the project repository  
    **Last data refresh:** 25 October 2026
    """
)
