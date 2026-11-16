"""Is influential AI model development concentrated in fewer organisations?

Concentration over time, Epoch AI data.
Drop this file into the group app's pages/ folder (with concentration.py
beside the app root) and it runs as one page of the multipage app.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from concentration import (credit_table, entrants_by_year,
                           explode_credit, file_fingerprint, gini, lorenz,
                           metrics_by_window, resolve_columns, share_matrix,
                           split_field_by_year)

from data import RAW_DIR, load_csv
from page_style import (
    analysis_header,
    interpretation,
    limitations,
    page_footer,
    page_takeaway,
)
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"   # validated categorical slots 1-3
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e5e1"

analysis_header(
    title="Concentration Dynamics",
    contributor="Aarushi",
    focus="How does organisational concentration change over time, and how sensitive is it to counting choices?",
    description=(
        "This page tests how conclusions about concentration change with the model set, "
        "Top-N choice, time window, and parent-company roll-up."
    ),
)


# ---------- data ----------------------------------------------------------
@st.cache_data(show_spinner="Loading Epoch AI data")
def load(dataset: str) -> tuple[pd.DataFrame, str, str]:
    """Read the same committed snapshot as the other pages."""
    local = RAW_DIR / f"{dataset}_ai_models.csv"
    return (load_csv(local),
            f"data/raw/{local.name} (sha256 {file_fingerprint(local)})",
            str(local))


def base_layout(fig: go.Figure, y_title: str, y_range=None, pct=False) -> go.Figure:
    fig.update_layout(
        height=360, margin=dict(l=8, r=110, t=10, b=8),
        plot_bgcolor="#fcfcfb", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=INK, size=14), hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=0, font=dict(color=MUTED)),
    )
    fig.update_xaxes(showgrid=False, linecolor=GRID, tickfont=dict(color=MUTED), dtick=2)
    fig.update_yaxes(title=y_title, gridcolor=GRID, zeroline=False,
                     tickfont=dict(color=MUTED), range=y_range,
                     tickformat=".0%" if pct else None)
    return fig


def end_label(fig, x, y, text):
    fig.add_annotation(x=x, y=y, text=text, showarrow=False, xanchor="left",
                       xshift=8, font=dict(color=INK, size=13))


# ---------- header --------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)
dataset = c1.radio("Model set", ["frontier", "notable"], horizontal=True,
                   help="Frontier = Epoch's top-10-by-training-compute at release. "
                        "Notable = Epoch's broader significance criteria.")
top_n = c2.slider("Top N organisations", 1, 10, 3)
window = c3.slider("Window (years)", 1, 3, 2,
                   help="Frontier releases are few per year; a rolling window smooths noise.")
roll_up = c4.toggle("Roll sub-labs up to parent", value=True,
                    help="e.g. Google Brain + DeepMind + Google Research -> Alphabet")

raw, source_label, _ = load(dataset)
cols = resolve_columns(raw)
credit = explode_credit(raw, cols, roll_up)
m = metrics_by_window(credit, top_n, window)

if m.empty:
    st.warning("Not enough models in any window. Widen the window or switch to 'notable'.")
    st.stop()

first, last = m.iloc[0], m.iloc[-1]

# ---------- hero numbers --------------------------------------------------
h1, h2, h3 = st.columns(3)
h1.metric(f"Top-{top_n} share, {last['window']}", f"{last['top_n_share']:.0%}",
          f"{(last['top_n_share'] - first['top_n_share']) * 100:+.0f} pts since {first['window']}",
          delta_color="off")
h2.metric(f"Organisations shipping models, {last['window']}", int(last["distinct_orgs"]),
          f"{int(last['distinct_orgs'] - first['distinct_orgs']):+d} since {first['window']}",
          delta_color="off")
h3.metric(f"Effective number of orgs, {last['window']}", f"{last['effective_orgs']:.1f}",
          help="1 / HHI. If every org had an equal share, this many orgs would give the same concentration.")

# ---------- chart 1: the slice that matters -------------------------------
st.subheader(f"Share of {dataset} models credited to the top {top_n} organisations")
f1 = go.Figure(go.Scatter(
    x=m["year"], y=m["top_n_share"], mode="lines+markers",
    line=dict(color=BLUE, width=2), marker=dict(size=8, color=BLUE, line=dict(color="#fcfcfb", width=2)),
    name=f"Top-{top_n} share", customdata=m[["window", "top_n_orgs", "models"]],
    hovertemplate="%{customdata[0]}: %{y:.0%} of %{customdata[2]} models<br>"
                  "Top orgs: %{customdata[1]}<extra></extra>"))
base_layout(f1, "Share of model credit", [0, 1], pct=True)
end_label(f1, last["year"], last["top_n_share"], f"{last['top_n_share']:.0%}")
st.plotly_chart(f1, width="stretch")

# ---------- chart 2: the counter-reading ----------------------------------
st.subheader("…while the field itself got wider or narrower?")
f2 = go.Figure()
f2.add_scatter(x=m["year"], y=m["distinct_orgs"], mode="lines+markers", name="Organisations shipping",
               line=dict(color=ORANGE, width=2), marker=dict(size=8, color=ORANGE),
               hovertemplate="%{y:.0f} organisations<extra></extra>")
f2.add_scatter(x=m["year"], y=m["effective_orgs"], mode="lines+markers", name="Effective number (1/HHI)",
               line=dict(color=AQUA, width=2, dash="dot"), marker=dict(size=8, color=AQUA, symbol="diamond"),
               hovertemplate="%{y:.1f} effective orgs<extra></extra>")
base_layout(f2, "Number of organisations", [0, None])
end_label(f2, last["year"], last["distinct_orgs"], "shipping")
end_label(f2, last["year"], last["effective_orgs"], "effective")
st.plotly_chart(f2, width="stretch")

interpretation(
    "A rising Top-N share suggests stronger concentration, while a rising organisation count suggests broader "
    "participation. Both can happen at the same time, and parent-company roll-up choices can change the result."
)

# ---------- deeper views --------------------------------------------------
st.divider()
st.subheader("Look closer")
tab_stay, tab_shape, tab_new, tab_where = st.tabs(
    ["Do leaders stay on top?", "How unequal?", "New entrants", "Sector and country"])

latest_tbl = credit_table(credit, int(last["year"]), window)

with tab_stay:
    leaders = credit.groupby("org")["credit"].sum().nlargest(10).index.tolist()
    sm = share_matrix(credit, leaders)
    sm = sm.loc[:, [c for c in sm.columns if c >= int(first["year"]) - window + 1]]
    st.markdown("**Each organisation's share of that year's models** (1-year, not rolling). "
                "A solid horizontal band means a lab stays on top year after year; "
                "scattered cells mean leadership rotates.")
    fh = go.Figure(go.Heatmap(
        z=sm.values, x=[str(c) for c in sm.columns], y=sm.index,
        colorscale=[[0, "#fcfcfb"], [0.15, "#cde2fb"], [0.4, "#86b6ef"], [0.7, "#2a78d6"], [1, "#0d366b"]],
        zmin=0, zmax=max(0.3, float(sm.values.max())), xgap=2, ygap=2,
        colorbar=dict(title="Share", tickformat=".0%"),
        hovertemplate="%{y}, %{x}: %{z:.0%} of models<extra></extra>"))
    fh.update_layout(height=60 + 34 * len(sm), margin=dict(l=8, r=8, t=10, b=8),
                     plot_bgcolor="#fcfcfb", paper_bgcolor="rgba(0,0,0,0)", font=dict(color=INK, size=13))
    fh.update_yaxes(autorange="reversed", tickfont=dict(color=INK))
    fh.update_xaxes(tickfont=dict(color=MUTED))
    st.plotly_chart(fh, width="stretch")
    st.caption("Rows are the 10 organisations with the most credit across the whole dataset.")

with tab_shape:
    first_tbl = credit_table(credit, int(first["year"]), window)
    lz0, lz1 = lorenz(first_tbl), lorenz(latest_tbl)
    g0, g1 = gini(first_tbl), gini(latest_tbl)
    st.markdown("**Lorenz curve.** Organisations sorted smallest to largest. If every org shipped the same "
                "number of models the curve would sit on the diagonal. The further it sags, the more "
                "a few orgs account for most models.")
    fl = go.Figure()
    fl.add_scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(color="#a8a79f", width=1, dash="dash"),
                   name="Perfect equality", hoverinfo="skip")
    fl.add_scatter(x=lz0["org_share"], y=lz0["model_share"], mode="lines", line=dict(color=ORANGE, width=2),
                   name=f"{first['window']} (Gini {g0:.2f})",
                   hovertemplate="Bottom %{x:.0%} of orgs made %{y:.0%} of models<extra></extra>")
    fl.add_scatter(x=lz1["org_share"], y=lz1["model_share"], mode="lines", line=dict(color=BLUE, width=2),
                   name=f"{last['window']} (Gini {g1:.2f})",
                   hovertemplate="Bottom %{x:.0%} of orgs made %{y:.0%} of models<extra></extra>")
    base_layout(fl, "Cumulative share of models", [0, 1], pct=True)
    fl.update_layout(height=420, margin=dict(l=8, r=8, t=10, b=8), hovermode="closest")
    fl.update_xaxes(title="Cumulative share of organisations", tickformat=".0%", dtick=0.2, range=[0, 1])
    st.plotly_chart(fl, width="stretch")
    st.caption("Gini: 0 = perfectly equal, 1 = one organisation made everything. "
               "Caveat: Gini ignores how many orgs there are, so read it next to chart 2.")

with tab_new:
    ent = entrants_by_year(credit)
    ent = ent[ent["year"] >= int(first["year"]) - window + 1]
    st.markdown("**Organisations shipping their first model in this dataset each year** versus ones that "
                "already had one. A steady stream of newcomers argues against a closed club.")
    fe = go.Figure()
    fe.add_bar(x=ent["year"], y=ent["returning"], name="Returning", marker=dict(color=BLUE),
               hovertemplate="%{y} returning orgs<extra></extra>")
    fe.add_bar(x=ent["year"], y=ent["new"], name="First model", marker=dict(color=AQUA),
               hovertemplate="%{y} first-time orgs<extra></extra>")
    base_layout(fe, "Organisations")
    fe.update_layout(barmode="stack", bargap=0.3)
    fe.update_traces(marker_line=dict(color="#fcfcfb", width=2))
    st.plotly_chart(fe, width="stretch")
    st.caption("'First' means first in Epoch's database, so the earliest years over-count newcomers.")

with tab_where:
    sector = split_field_by_year(raw, cols, "sector", keep=["Industry", "Academia"])
    country = split_field_by_year(raw, cols, "country", top_k=3)
    palette = [BLUE, ORANGE, AQUA, "#eda100"]

    def share_lines(long: pd.DataFrame, title: str):
        long = long[long["year"] >= int(first["year"]) - window + 1]
        groups = sorted(g for g in long["group"].unique() if g != "Other") + \
            (["Other"] if "Other" in set(long["group"]) else [])
        f = go.Figure()
        for i, g in enumerate(groups):
            d = long[long["group"] == g]
            col = "#a8a79f" if g == "Other" else palette[i % len(palette)]
            f.add_scatter(x=d["year"], y=d["share"], mode="lines+markers", name=g,
                          line=dict(color=col, width=2), marker=dict(size=8, color=col),
                          hovertemplate=f"{g}: %{{y:.0%}}<extra></extra>")
            end_label(f, d["year"].iloc[-1], d["share"].iloc[-1], g[:18])
        base_layout(f, "Share of models", [0, 1], pct=True)
        st.markdown(title)
        st.plotly_chart(f, width="stretch")

    if sector.empty and country.empty:
        st.info("This Epoch file has no sector or country columns.")
    if not sector.empty:
        share_lines(sector, "**Industry vs academia.** Share of models by organisation type "
                            "(1-year, fractional credit for mixed teams).")
    if not country.empty:
        share_lines(country, "**Country of the developing organisation.** Top 3 countries, rest grouped.")

# ---------- trace panel ---------------------------------------------------
st.divider()
st.subheader("Trace a number back to the source")
st.caption(f"Source file: `{source_label}`  ·  Epoch AI, *Data on AI Models*, CC BY 4.0")

pick = st.selectbox("Window to trace", m["window"].tolist(), index=len(m) - 1)
row = m[m["window"] == pick].iloc[0]
end_year = int(row["year"])
t = credit_table(credit, end_year, window)
models_in = credit[(credit["year"] > end_year - window) & (credit["year"] <= end_year)]

s1, s2 = st.columns([3, 2])
with s1:
    st.markdown("**Step 1. Raw rows from the CSV in this window** (`Organization` column untouched)")
    st.dataframe(models_in.drop_duplicates("model")[["model", "org_raw", "year"]]
                 .rename(columns={"model": "Model", "org_raw": "Organization (raw)", "year": "Year"}),
                 hide_index=True, width="stretch", height=300)
with s2:
    st.markdown("**Step 2. Credit per organisation** (1/k for a model with k orgs)")
    st.dataframe(t.assign(share=lambda d: (d["share"] * 100).round(1))
                 .rename(columns={"org": "Organisation", "credit": "Credit", "share": "Share %"}),
                 hide_index=True, width="stretch", height=300)

top = t.head(top_n)
st.markdown(
    f"**Step 3. Arithmetic.** Top {top_n} credit = "
    + " + ".join(f"{c:.2f}" for c in top["credit"])
    + f" = **{top['credit'].sum():.2f}**  ÷  total credit **{t['credit'].sum():.2f}** "
    f"(= {row['models']} models)  =  **{row['top_n_share']:.1%}**, the value plotted for {pick}.")

with st.expander("Method notes and choices that change the answer"):
    st.markdown(f"""
- **Dataset:** `{dataset}`. Epoch's frontier flag marks models in the top 10 by training compute at release.
- **Collaborations:** a model by *k* organisations gives each 1/k credit, so totals equal model counts.
- **Roll-up:** {'on' if roll_up else 'off'}. Mapping lives in `concentration.PARENT_MAP` and is a judgement call.
- **Window:** {window}-year rolling, ending at the labelled year. Windows with fewer than 5 models are dropped.
- **HHI** on a 0 to 10,000 scale (the competition-policy convention). Latest: {last['hhi']:,.0f}.
- Models with no publication date or organisation are excluded.
""")


page_takeaway(
    "Concentration depends on both the time period and the counting choices. The latest frontier can appear highly "
    "concentrated even when the wider field is broadening."
)

limitations([
    "Results change depending on whether sub-labs are rolled up to parent companies.",
    "Short rolling windows can be noisy because frontier model releases are relatively rare.",
    "Different concentration measures capture different aspects of the same distribution.",
])

page_footer("Epoch AI Frontier Models and Epoch AI Notable Models")
