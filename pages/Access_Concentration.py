import altair as alt
import pandas as pd
import streamlit as st

from data import load_notable_data
from page_style import (
    analysis_header,
    interpretation,
    limitations,
    page_footer,
    page_takeaway,
)

analysis_header(
    title="Access Concentration",
    contributor="Akash",
    focus="Is access to influential AI models concentrating behind company APIs?",
    description=(
        "This page compares open-weight releases with closed API and hosted forms of model access."
    ),
)

ACCESS_ORDER = ["Open weights", "Closed (API / hosted)", "Unreleased"]
ACCESS_COLOURS = ["#009E73", "#D55E00", "#999999"]
START, END = 2019, 2024


def classify(raw):
    raw = str(raw)
    if raw.startswith("Open weights"):
        return "Open weights"
    if raw in ("API access", "Hosted access (no API)"):
        return "Closed (API / hosted)"
    if raw == "Unreleased":
        return "Unreleased"
    return None


@st.cache_data
def load_data():
    df = load_notable_data().copy()
    df["Publication date"] = pd.to_datetime(df["Publication date"], errors="coerce")
    df = df.dropna(subset=["Publication date"])
    df["Year"] = df["Publication date"].dt.year
    df["Access"] = df["Model accessibility"].apply(classify)
    df["Training compute (FLOP)"] = pd.to_numeric(df["Training compute (FLOP)"], errors="coerce")
    df = df[(df["Year"] >= START) & (df["Year"] <= END)]
    return df.dropna(subset=["Access"]).copy()


def access_shares(df):
    counts = (
        df.groupby(["Year", "Access"]).size().unstack(fill_value=0)
        .reindex(columns=ACCESS_ORDER, fill_value=0)
    )
    totals = counts.sum(axis=1)
    long = counts.reset_index().melt(id_vars="Year", var_name="Access", value_name="Models")
    long["Total"] = long["Year"].map(totals)
    long["Share_percent"] = long["Models"] / long["Total"] * 100
    long["Rank"] = long["Access"].map(ACCESS_ORDER.index)
    return long, counts, totals


df = load_data()

frontier = st.toggle("High-compute models only (training compute ≥ 1e23 FLOP)", value=False)
view = df[df["Training compute (FLOP)"] >= 1e23].copy() if frontier else df.copy()

if view.empty:
    st.info("No models are available for this selection.")
    st.stop()

shares, counts, totals = access_shares(view)
last_year = int(totals.index.max())
first_year = int(totals.index.min())

closed_last = counts.loc[last_year, "Closed (API / hosted)"] / totals.loc[last_year] * 100
open_last = counts.loc[last_year, "Open weights"] / totals.loc[last_year] * 100
first_closed = counts.loc[first_year, "Closed (API / hosted)"] / totals.loc[first_year] * 100

m1, m2, m3 = st.columns(3)
m1.metric(f"Closed share, {first_year}", f"{first_closed:.0f}%")
m2.metric(f"Closed share, {last_year}", f"{closed_last:.0f}%", f"{closed_last - first_closed:+.0f} pts")
m3.metric(f"Open-weights share, {last_year}", f"{open_last:.0f}%")

st.divider()
st.subheader("1. Has closed access become more common over time?")
st.caption("Share of notable AI models by access type and publication year. Models without an accessibility label are excluded.")

bars = (
    alt.Chart(shares)
    .mark_bar()
    .encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Models:Q", stack="normalize", title="Share of notable AI models", axis=alt.Axis(format="%")),
        color=alt.Color(
            "Access:N",
            sort=ACCESS_ORDER,
            scale=alt.Scale(domain=ACCESS_ORDER, range=ACCESS_COLOURS),
            legend=alt.Legend(orient="bottom", title=None),
        ),
        order=alt.Order("Rank:Q"),
        tooltip=[
            "Year",
            "Access",
            "Models",
            "Total",
            alt.Tooltip("Share_percent:Q", title="Share (%)", format=".1f"),
        ],
    )
    .properties(height=380)
)
st.altair_chart(bars, width="stretch")

interpretation(
    "Closed API and hosted access became much more common between 2019 and 2024, although open-weight releases "
    "still represented a substantial share of notable models."
)

st.divider()
st.subheader("2. How many models are in each access category?")
st.caption("Raw model counts behind the percentages, so years with small samples are visible.")

lines = (
    alt.Chart(shares)
    .mark_line(point=True, strokeWidth=3)
    .encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Models:Q", title="Number of notable AI models"),
        color=alt.Color(
            "Access:N",
            sort=ACCESS_ORDER,
            scale=alt.Scale(domain=ACCESS_ORDER, range=ACCESS_COLOURS),
            legend=alt.Legend(orient="bottom", title=None),
        ),
        tooltip=["Year", "Access", "Models"],
    )
    .properties(height=300)
)
st.altair_chart(lines, width="stretch")

if frontier:
    interpretation(
        "Among high-compute models, open weights remain important. Increasing closed access across notable models "
        "does not mean the high-compute frontier is entirely closed."
    )
else:
    interpretation(
        "Across all notable models, closed access increased substantially. The raw counts also show that the number "
        "of labelled models changes from year to year."
    )

st.divider()
with st.expander("Trace a number back to the source"):
    year = st.selectbox("Year", list(range(last_year, first_year - 1, -1)), key="access_year")
    access = st.selectbox("Access type", ACCESS_ORDER, key="access_type")
    year_rows = view[view["Year"] == year]
    rows = year_rows[year_rows["Access"] == access]
    pct = len(rows) / max(len(year_rows), 1) * 100
    st.write(f"{len(rows)} of {len(year_rows)} labelled notable models in {year} → {pct:.1f}%")
    st.dataframe(
        rows[["Model", "Organization", "Model accessibility", "Training compute (FLOP)"]].sort_values("Model"),
        width="stretch",
        hide_index=True,
    )

with st.expander("Data and method"):
    st.markdown(
        "- **Source:** Epoch AI, *Notable AI Models* (`notable_ai_models.csv`).\n"
        "- **Access type:** from `Model accessibility`. Open weights includes all labels beginning with 'Open weights'; "
        "Closed = API access or hosted access without an API; Unreleased = unreleased models. Blank labels are excluded.\n"
        f"- **Years:** {START}–{END}. Earlier accessibility labels are too incomplete for reliable comparison.\n"
        "- **High-compute view:** `Training compute (FLOP)` ≥ 1e23. Missing compute estimates are excluded from this view."
    )

page_takeaway(
    "Closed API and hosted access have become more common, but the picture is not uniform. Open-weight models "
    "still represent an important part of the high-compute frontier."
)

limitations([
    "Open weights does not always mean unrestricted open-source use; some releases have restrictive licences.",
    "Models with missing accessibility labels are excluded.",
    "Before 2019, accessibility information is too incomplete for reliable comparison.",
    "Closed access does not necessarily mean model development itself is concentrated among fewer organisations.",
])

page_footer("Epoch AI Notable Models")
