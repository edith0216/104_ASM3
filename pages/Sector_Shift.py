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
    title="Sector Shift",
    contributor="Adarsh Kumbhar",
    focus="Has notable AI model development shifted from academia towards industry?",
    description=(
        "This page compares the changing roles of academia and industry in notable "
        "AI model development, including high-compute models."
    ),
)

SECTOR_ORDER = ["Industry", "Industry–academia collaboration", "Academia", "Other"]
SECTOR_COLOURS = ["#0072B2", "#CC79A7", "#E69F00", "#999999"]


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
    df = load_notable_data().copy()
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
    long = shares.reset_index().melt(id_vars="Year", var_name="Sector", value_name="Share_percent")
    count_long = counts.reset_index().melt(id_vars="Year", var_name="Sector", value_name="Models")
    long["Models"] = count_long["Models"]
    long["Total"] = long["Year"].map(totals)
    long["Rank"] = long["Sector"].map(SECTOR_ORDER.index)
    return long, counts, totals


df = load_data()
shares, counts, totals = sector_shares(df)

ind_2014 = counts.loc[2014, "Industry"] / totals.loc[2014] * 100
ind_2024 = counts.loc[2024, "Industry"] / totals.loc[2024] * 100
aca_2024 = counts.loc[2024, "Academia"] / totals.loc[2024] * 100

c1, c2, c3 = st.columns(3)
c1.metric("Industry-only share, 2014", f"{ind_2014:.1f}%")
c2.metric("Industry-only share, 2024", f"{ind_2024:.1f}%", f"{ind_2024 - ind_2014:+.1f} pts")
c3.metric("Academia-only share, 2024", f"{aca_2024:.1f}%")

st.divider()
st.subheader("1. Has notable AI development shifted towards industry?")
st.caption("Share of notable AI models by sector of the developing organisation(s), 2014–2024.")

start, end = st.slider("Select year range", 2014, 2024, (2014, 2024))
view = shares[shares["Year"].between(start, end)].copy()

if view.empty:
    st.info("No data are available for the selected period.")
else:
    bars = (
        alt.Chart(view)
        .mark_bar()
        .encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Models:Q", stack="normalize", title="Share of notable AI models", axis=alt.Axis(format="%")),
            color=alt.Color(
                "Sector:N",
                sort=SECTOR_ORDER,
                scale=alt.Scale(domain=SECTOR_ORDER, range=SECTOR_COLOURS),
                legend=alt.Legend(orient="bottom", title=None),
            ),
            order=alt.Order("Rank:Q"),
            tooltip=[
                "Year",
                "Sector",
                "Models",
                "Total",
                alt.Tooltip("Share_percent:Q", title="Share (%)", format=".1f"),
            ],
        )
        .properties(height=380)
    )
    st.altair_chart(bars, width="stretch")

interpretation(
    f"In 2014, universities working alone produced most notable models. By 2024, "
    f"industry working alone produced about {ind_2024:.0f}% of them, while academia "
    f"alone accounted for about {aca_2024:.0f}%."
)

st.divider()
st.subheader("2. Who can afford the highest levels of compute?")
st.caption("Training compute of each notable model. Models without a published compute estimate are excluded.")

threshold_label = st.selectbox("High-compute threshold", ["1e22 FLOP", "1e23 FLOP", "1e24 FLOP"], index=1)
threshold = float(threshold_label.split()[0])

pts = df.dropna(subset=["Training compute (FLOP)"]).copy()
pts = pts[pts["Training compute (FLOP)"] > 0]
above = pts[pts["Training compute (FLOP)"] >= threshold]
ind_above = (above["Sector"] == "Industry").mean() * 100 if len(above) else 0
aca_above = int((above["Sector"] == "Academia").sum())

m1, m2, m3 = st.columns(3)
m1.metric(f"Models ≥ {threshold_label}", len(above))
m2.metric("Industry-only share", f"{ind_above:.1f}%")
m3.metric("Academia-only models", aca_above)

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
            legend=alt.Legend(orient="bottom", title=None),
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
rule = alt.Chart(pd.DataFrame({"y": [threshold]})).mark_rule(strokeDash=[6, 4]).encode(y="y:Q")
st.altair_chart((scatter + rule).properties(height=420), width="stretch")

interpretation(
    "At high compute levels, most notable models are built by industry organisations. "
    "This suggests that concentration is also visible in which sector can access very large computing resources."
)

st.divider()
with st.expander("Trace a number back to the source"):
    year = st.selectbox("Year", list(range(2024, 2013, -1)), key="sector_year")
    sector = st.selectbox("Sector", SECTOR_ORDER, key="sector_type")
    year_rows = df[df["Year"] == year]
    rows = year_rows[year_rows["Sector"] == sector]
    pct = len(rows) / max(len(year_rows), 1) * 100
    st.write(f"{len(rows)} of {len(year_rows)} notable models in {year} → {pct:.1f}%")
    show = rows.copy()
    show["Publication date"] = show["Publication date"].dt.date
    st.dataframe(
        show[["Model", "Organization", "Publication date", "Organization categorization", "Training compute (FLOP)"]]
        .sort_values("Publication date"),
        width="stretch",
        hide_index=True,
    )

with st.expander("Data and method"):
    st.markdown(
        "- **Source:** Epoch AI, *Notable AI Models* (`notable_ai_models.csv`).\n"
        "- **Sector:** from `Organization categorization`. Industry = all listed developers are industry; "
        "Academia = all listed developers are academic; collaboration = both appear; Other = remaining categories.\n"
        "- **Years:** 2014–2024, based on `Publication date`.\n"
        "- **Compute:** `Training compute (FLOP)`; missing compute estimates are excluded from section 2 only."
    )

page_takeaway(
    "Notable AI model development has shifted strongly towards industry. Industry-only models now make up "
    "a much larger share than they did in 2014, especially among high-compute models."
)

limitations([
    "Sector concentration does not necessarily mean fewer individual organisations are participating.",
    "Models without published training-compute estimates are excluded from the compute analysis.",
    "The result depends on the sector categories recorded in the Epoch AI dataset.",
])

page_footer("Epoch AI Notable Models")
