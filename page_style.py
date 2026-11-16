import streamlit as st


def analysis_header(title, contributor, focus, description=None):
    """Shared header used by all analysis pages."""
    st.title(title)
    st.caption(f"Main contribution: {contributor}")
    st.markdown(f"**Question:** {focus}")

    if description:
        st.write(description)

    st.divider()


def interpretation(text):
    """Consistent interpretation text below charts."""
    st.markdown(f"**Interpretation:** {text}")


def page_takeaway(text):
    """Consistent takeaway section near the bottom of each page."""
    st.divider()
    st.subheader("Page takeaway")
    st.markdown(text)


def limitations(items):
    """Render a short list of page-specific limitations."""
    st.subheader("Limitations")
    for item in items:
        st.markdown(f"- {item}")


def page_footer(source, refresh="November 2026"):
    """Shared source and refresh footer."""
    st.divider()
    st.caption(f"Source: {source} | Last data refresh: {refresh}")
