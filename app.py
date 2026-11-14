import streamlit as st

st.set_page_config(
    page_title="AI Concentration Explorer",
    page_icon="🤖",
    layout="wide")

st.title("AI Concentration Explorer")

st.markdown("""
## Research question

**Is influential AI model development concentrated in fewer organisations?**

## Persona

**Technology Policy Analyst**

This app explores AI concentration from three perspectives:

- **Organisation concentration** — who builds influential AI models?
- **Sector shift** — has model development moved from academia to industry?
- **Access concentration** — is access increasingly controlled through company APIs?
""")

st.divider()

st.subheader("Overall answer")

st.markdown("""
Influential AI development shows several forms of concentration.

A relatively small group of organisations often accounts for a large share of frontier model development, while notable model development has shifted strongly towards industry.

At the same time, closed API access has become more common, although open-weight models remain important at the high-compute frontier.

Overall, concentration is important, but it does not increase in the same way across every year, sector, or access model.
""")

st.divider()

st.caption(
    "Sources: Epoch AI and Stanford AI Index 2025 | "
    "Data last refreshed: November 2026")
