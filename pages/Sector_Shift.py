import altair as alt
import pandas as pd
import streamlit as st

from data import load_notable_data
from page_style import (
    CVD_BLUE,
    CVD_GREY,
    CVD_ORANGE,
    CVD_PURPLE,
    CVD_VERMILLION,
    analysis_header,
    interpretation,
    limitations,
    page_footer,
    page_takeaway,
)

analysis_header(
    "Sector Shift",
    "Adarsh Kumbhar",
    "Has notable model development shifted from academia towards industry?",
    "This page compares the changing roles of academia and industry in notable AI model development.",
)

SECTOR_ORDER = ["Industry", "Industry–academia collaboration", "Academia", "Other"]
SECTOR_COLOURS = [CVD_BLUE, CVD_PURPLE, CVD_ORANGE, CVD_GREY]


def classify(raw):
    labels = {x.strip() for x in str(raw).split(",") if x.strip() and x.strip() != "nan"}
    if labels == {"Industry"}:
        return "Industry"
    if labels == {"Academia"}:
        return "Academia"
    if {"Industry", "Academia"} <= labels:
        return "Industry–academia collaboration"
    return "Other"


@st.cache_data
def load_data():
    df = load_notable_data()
    df["Publication date"] = pd.to_datetime(df["Publication date"], errors="coerce")
    df = df.dropna(subset=["Publication date"])
    df["Year"] = df["Publication date"].dt.year
    df["Sector"] = df["Organization categorization"].apply(classify)
    df["Training compute (FLOP)"] = pd.to_numeric(df["Training compute (FLOP)"], errors="coerce")
    return df[(df["Year"] >= 2014) & (df["Year"] <= 2024)].copy()


def sector_shares(df):
    counts = (
        df.groupby(["Year", "Sector"]).size().unstack(fill_value=0)
        .reindex(columns=SECTOR_ORDER, fill_value=0)
    )
    totals = counts.sum(axis=1)
    shares = counts.div(totals, axis=0).mul(100)
    long = shares.reset_index().melt(id_vars="Year", var_name="Sector", value_name="Share (%)")
    count_long = counts.reset_index().melt(id_vars="Year", var_name="Sector", value_name="Models")
    long["Models"] = count_long["Models"].values
    long["Total"] = long["Year"].map(totals)
    long["Rank"] = long["Sector"].map(SECTOR_ORDER.index)
    return long, counts, totals


df = load_data()
shares, counts, totals = sector_shares(df)

ind_2014 = counts.loc[2014, "Industry"] / totals.loc[2014] * 100
ind_2024 = counts.loc[2024, "Industry"] / totals.loc[2024] * 100
aca_2024 = counts.loc[2024, "Academia"] / totals.loc[2024] * 100

c1, c2, c3 = st.columns(3)
c1.metric("Industry-only share of notable models, 2014", f"{ind_2014:.1f}%")
c2.metric("Industry-only share of notable models, 2024", f"{ind_2024:.1f}%", f"{ind_2024 - ind_2014:+.1f} pts")
c3.metric("Academia-only share of notable models, 2024", f"{aca_2024:.1f}%")

st.divider()
st.subheader("1. Who produces notable AI models each year?")
st.caption("Share of notable AI models by sector of the developing organisation(s), 2014–2024.")

start, end = st.slider("Year range", 2014, 2024, (2014, 2024))
view = shares[(shares["Year"] >= start) & (shares["Year"] <= end)].copy()

if view.empty:
    st.info("No sector data are available for the selected year range.")
else:
    bars = (
        alt.Chart(view)
        .mark_bar()
        .encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Models:Q", stack="normalize", title="Share of notable models", axis=alt.Axis(format="%")),
            color=alt.Color(
                "Sector:N",
                sort=SECTOR_ORDER,
                scale=alt.Scale(domain=SECTOR_ORDER, range=SECTOR_COLOURS),
                legend=alt.Legend(orient="bottom", title="Sector"),
            ),
            order=alt.Order("Rank:Q"),
            tooltip=["Year", "Sector", "Models", "Total", alt.Tooltip("Share (%):Q", format=".1f")],
        )
        .properties(height=380)
    )
    st.altair_chart(bars, width="stretch")

    # Visible table ensures exact values can be read without hovering.
    table = view[["Year", "Sector", "Models", "Share (%)"]].copy()
    table["Share (%)"] = table["Share (%)"].round(1)
    st.dataframe(table, width="stretch", hide_index=True, height=230)

interpretation(
    f"In 2014, universities working alone produced most notable models. By 2024, "
    f"companies working alone produced {ind_2024:.0f}% of them, while academia alone "
    f"accounted for {aca_2024:.0f}%."
)

st.divider()
st.subheader("2. Who can afford the compute?")
st.caption("Training compute of each notable model (FLOP, logarithmic scale). Models without a published compute estimate are excluded.")

threshold_label = st.selectbox("High-compute threshold", ["1e22 FLOP", "1e23 FLOP", "1e24 FLOP"], index=1)
threshold = float(threshold_label.split()[0])

pts = df.dropna(subset=["Training compute (FLOP)"]).copy()
pts = pts[pts["Training compute (FLOP)"] > 0]
above = pts[pts["Training compute (FLOP)"] >= threshold]
ind_above = (above["Sector"] == "Industry").mean() * 100 if len(above) else 0
aca_above = (above["Sector"] == "Academia").sum()

d1, d2, d3 = st.columns(3)
d1.metric(f"Models at or above {threshold_label}", f"{len(above)}")
d2.metric("Industry-only share", f"{ind_above:.1f}%")
d3.metric("Academia-only models", int(aca_above))

if pts.empty:
    st.info("No models with published positive training-compute estimates are available.")
else:
    scatter = (
        alt.Chart(pts)
        .mark_circle(size=55, opacity=0.75)
        .encode(
            x=alt.X("Publication date:T", title="Publication date"),
            y=alt.Y("Training compute (FLOP):Q", scale=alt.Scale(type="log"), title="Training compute (FLOP, log scale)"),
            color=alt.Color(
                "Sector:N",
                sort=SECTOR_ORDER,
                scale=alt.Scale(domain=SECTOR_ORDER, range=SECTOR_COLOURS),
                legend=alt.Legend(orient="bottom", title="Sector"),
            ),
            tooltip=[
                "Model",
                "Organization",
                "Sector",
                alt.Tooltip("Publication date:T", format="%b %Y"),
                alt.Tooltip("Training compute (FLOP):Q", format=".2e"),
            ],
        )
    )
    rule = (
        alt.Chart(pd.DataFrame({"y": [threshold]}))
        .mark_rule(strokeDash=[6, 4], color=CVD_VERMILLION)
        .encode(y="y:Q")
    )
    st.altair_chart((scatter + rule).properties(height=420), width="stretch")

    # Exact scatter values are also available without hover.
    compute_table = pts[["Model", "Organization", "Sector", "Publication date", "Training compute (FLOP)"]].copy()
    compute_table["Publication date"] = compute_table["Publication date"].dt.date
    compute_table = compute_table.sort_values("Training compute (FLOP)", ascending=False)
    st.dataframe(compute_table, width="stretch", hide_index=True, height=260)

interpretation(
    "At high compute levels, most notable models are built by industry organisations. "
    "This suggests that concentration also has a sector dimension: access to very large computing resources is unevenly distributed."
)

st.divider()
with st.expander("Trace a number back to the source"):
    year = st.selectbox("Year", list(range(2024, 2013, -1)))
    sector = st.selectbox("Sector", SECTOR_ORDER)
    rows = df[(df["Year"] == year) & (df["Sector"] == sector)]
    total_year = len(df[df["Year"] == year])
    st.write(f"{len(rows)} of {total_year} notable models in {year} → {len(rows) / max(total_year, 1) * 100:.1f}%")
    rows = rows.assign(**{"Publication date": rows["Publication date"].dt.date})
    st.dataframe(
        rows[["Model", "Organization", "Publication date", "Organization categorization", "Training compute (FLOP)"]].sort_values("Publication date"),
        width="stretch",
        hide_index=True,
    )

with st.expander("Data and method"):
    st.markdown(
        "- **Source:** Epoch AI, *Notable AI Models* dataset (`notable_ai_models.csv`), downloaded 25 October 2026 from epoch.ai/data/ai-models.\n"
        "- **Sector:** from the `Organization categorization` column. A model is *Industry* if every listed developer is industry, "
        "*Academia* if every developer is academic, *collaboration* if both appear, and *Other* for government, research collectives or blanks.\n"
        "- **Years:** 2014–2024, by `Publication date`.\n"
        "- **Compute:** `Training compute (FLOP)`; models without an estimate are excluded from section 2 only."
    )

page_takeaway(
    "Notable AI model development has shifted strongly towards industry. Industry-only models now make up a much larger share than in 2014, especially among high-compute models."
)

limitations([
    "Sector concentration does not necessarily mean fewer individual organisations are participating.",
    "Models without published training-compute estimates are excluded from the compute analysis.",
    "The sector result depends on the organisation categories recorded in the Epoch AI dataset.",
])

page_footer("Epoch AI Notable Models")
