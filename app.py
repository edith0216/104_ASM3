import streamlit as st

st.set_page_config(
    page_title="AI Concentration Explorer",
    page_icon="🤖",
    layout="wide")

# Title
st.title("AI Concentration Explorer")

st.markdown(
    """
    An interactive data narrative exploring where influential AI developmentis becoming concentrated.
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
    - **Menghan** — Organisation concentration
    - **Aarushi** — Latest frontier concentration
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
    AI development is becoming concentrated across organisations, sectors,
    and model access.
    """)

st.divider()


# 5. Three Analytical Lenses

st.subheader("Three ways to examine concentration")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 1. Organisation")
    st.write("Are a small number of organisations responsible for a large share of frontier AI model development?")
    
    st.caption("Long-term organisation concentration and the latest frontier picture.")

with col2:
    st.markdown("### 2. Sector")
    st.write("Has notable AI model development shifted from academia towards industry?")
    st.caption("Compares the changing roles of industry and academia.")

with col3:
    st.markdown("### 3. Access")
    st.write("Is access to influential AI models becoming more concentrated behind company APIs and hosted services?")
    st.caption("Compares open-weight and closed forms of model access.")

st.divider()


# Overall Answer

st.subheader("Overall answer")

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

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Latest frontier Top-3 share",
        value="88%"
    )
    st.caption(
        "Top three organisations accounted for 7 of 8 frontier models "
        "in the latest 2025–2026 window."
    )

with col2:
    st.metric(
        label="Industry-only share in 2024",
        value="83%"
    )
    st.caption(
        "Industry-only notable models increased from about 15% in 2014 "
        "to 83% in 2024."
    )

with col3:
    st.metric(
        label="Closed/API share in 2024",
        value="44%"
    )
    st.caption(
        "Closed API or hosted access increased from 0% in 2019 "
        "to 44% in 2024."
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
    **Last data refresh:** November 2026
    """
)
