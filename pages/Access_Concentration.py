import altair as alt
import pandas as pd
import streamlit as st

from data import load_notable_data
from page_style import analysis_header

analysis_header("Access Concentration", "Akash",
                "Is access to influential AI models concentrating behind company APIs?")

ACCESS_ORDER = ["Open weights", "Closed (API / hosted)", "Unreleased"]
ACCESS_COLOURS = ["#2da44e", "#d1242f", "#9aa0a6"]
START, END = 2019, 2024  # before 2019 most rows have no accessibility label


def classify(raw):
    raw = str(raw)
    if raw.startswith("Open weights"):
        return "Open weights"
    if raw in ("API access", "Hosted access (no API)"):
        return "Closed (API / hosted)"
    if raw == "Unreleased":
        return "Unreleased"
    return None  # blank / unknown


@st.cache_data
def load_data():
    df = load_notable_data()
    df["Publication date"] = pd.to_datetime(df["Publication date"], errors="coerce")
    df = df.dropna(subset=["Publication date"])
    df["Year"] = df["Publication date"].dt.year
    df["Access"] = df["Model accessibility"].apply(classify)
    df["Training compute (FLOP)"] = pd.to_numeric(df["Training compute (FLOP)"], errors="coerce")
    df = df[(df["Year"] >= START) & (df["Year"] <= END)]
    return df.dropna(subset=["Access"])


def access_shares(df):
    counts = df.groupby(["Year", "Access"]).size().unstack(fill_value=0).reindex(columns=ACCESS_ORDER, fill_value=0)
    totals = counts.sum(axis=1)
    long = counts.reset_index().melt(id_vars="Year", var_name="Access", value_name="Models")
    long["Total"] = long["Year"].map(totals)
    long["Share (%)"] = long["Models"] / long["Total"] * 100
    long["Rank"] = long["Access"].map(ACCESS_ORDER.index)
    return long, counts, totals


df = load_data()

frontier = st.toggle("Frontier models only (training compute ≥ 1e23 FLOP)", value=False)
view = df[df["Training compute (FLOP)"] >= 1e23] if frontier else df
shares, counts, totals = access_shares(view)

closed_last = counts.loc[END, "Closed (API / hosted)"] / totals.loc[END] * 100
open_last = counts.loc[END, "Open weights"] / totals.loc[END] * 100

m1, m2, m3 = st.columns(3)
first_year = int(totals.index.min())
first_closed = counts.loc[first_year, "Closed (API / hosted)"] / totals.loc[first_year] * 100
m1.metric(f"Closed (API/hosted) share, {first_year}", f"{first_closed:.0f}%")
m2.metric(f"Closed (API/hosted) share, {END}", f"{closed_last:.0f}%", f"{closed_last - first_closed:+.0f} pts",
          delta_color="inverse")
m3.metric(f"Open-weights share, {END}", f"{open_last:.0f}%")

st.divider()
st.subheader("1. How are notable models released each year?")
st.caption("Share of notable models by access type, by publication year. Models with no accessibility label are excluded.")

bars = (
    alt.Chart(shares)
    .mark_bar()
    .encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Models:Q", stack="normalize", title="Share of notable models", axis=alt.Axis(format="%")),
        color=alt.Color("Access:N", sort=ACCESS_ORDER, scale=alt.Scale(domain=ACCESS_ORDER, range=ACCESS_COLOURS),
                        legend=alt.Legend(orient="bottom", title=None)),
        order=alt.Order("Rank:Q"),
        tooltip=["Year", "Access", "Models", "Total", alt.Tooltip("Share (%):Q", format=".1f")],
    )
    .properties(height=380)
)
st.altair_chart(bars, width="stretch")

st.subheader("2. How many models in each category?")
st.caption("Raw counts behind the shares, so small years are visible.")
lines = (
    alt.Chart(shares)
    .mark_line(point=True, strokeWidth=3)
    .encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Models:Q", title="Number of notable models"),
        color=alt.Color("Access:N", sort=ACCESS_ORDER, scale=alt.Scale(domain=ACCESS_ORDER, range=ACCESS_COLOURS),
                        legend=alt.Legend(orient="bottom", title=None)),
        tooltip=["Year", "Access", "Models"],
    )
    .properties(height=300)
)
st.altair_chart(lines, width="stretch")

st.markdown(
    "**Reading:** across all notable models, the closed share climbs steeply. More capability now sits behind "
    "a company's API. But switch on *frontier only*: at the top end, open-weights releases grew from none in "
    "2021 to the majority in 2024. Access is concentrating in the middle of the field, not at the frontier."
)

st.divider()
with st.expander("Trace a number back to the source"):
    year = st.selectbox("Year", list(range(END, START - 1, -1)))
    access = st.selectbox("Access type", ACCESS_ORDER)
    year_rows = view[view["Year"] == year]
    rows = year_rows[year_rows["Access"] == access]
    st.write(f"{len(rows)} of {len(year_rows)} labelled notable models in {year} → "
             f"{len(rows) / max(len(year_rows), 1) * 100:.1f}%")
    st.dataframe(
        rows[["Model", "Organization", "Model accessibility", "Training compute (FLOP)"]].sort_values("Model"),
        width="stretch", hide_index=True,
    )

with st.expander("Data and method"):
    st.markdown(
        "- **Source:** Epoch AI, *Notable AI Models* (`notable_ai_models.csv`), the same file the other sections use.\n"
        "- **Access type:** from the `Model accessibility` column. *Open weights* = any 'Open weights' label "
        "(unrestricted, non-commercial or restricted use). *Closed* = 'API access' or 'Hosted access (no API)'. "
        "*Unreleased* = 'Unreleased'. Blank labels are excluded.\n"
        f"- **Years:** {START}–{END}. Before 2019 most models have no accessibility label, so earlier shares would mislead.\n"
        "- **Frontier:** `Training compute (FLOP)` ≥ 1e23; models without a compute estimate are excluded from that view.\n"
        "- **Limitation:** 'open weights' includes restrictive licences; frontier counts in 2019–2021 are very small."
    )
