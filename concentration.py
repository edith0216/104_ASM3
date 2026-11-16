"""Concentration metrics for Epoch AI model data.

Pure functions, no Streamlit. Every number the page shows comes from here,
so the trace panel and the charts can never disagree.

Unit of analysis: one model = one unit of credit. A model built by k
organisations gives each of them 1/k (fractional credit), after names are
optionally rolled up to a corporate parent.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pandas as pd

EPOCH_URLS = {
    "frontier": "https://epoch.ai/data/frontier_ai_models.csv",
    "notable": "https://epoch.ai/data/notable_ai_models.csv",
}

# Rolls sub-labs up to the company that funds and controls them.
# Every entry is a judgement call, which is why the page exposes it as a toggle.
PARENT_MAP = {
    r"^google\b.*|^deepmind$|^google deepmind$|^google brain$|^google research$": "Alphabet (Google)",
    r"^meta\b.*|^facebook\b.*": "Meta",
    r"^microsoft\b.*": "Microsoft",
    r"^amazon\b.*|^aws\b.*": "Amazon",
    r"^nvidia\b.*": "NVIDIA",
    r"^alibaba\b.*": "Alibaba",
    r"^baidu\b.*": "Baidu",
    r"^tencent\b.*": "Tencent",
    r"^openai\b.*": "OpenAI",
    r"^anthropic\b.*": "Anthropic",
}

# Epoch has renamed headers over time; match on meaning, not exact text.
COLUMN_CANDIDATES = {
    "model": ["Model", "System"],
    "org": ["Organization", "Organisation", "Organization(s)"],
    "date": ["Publication date", "Publication Date", "Date"],
    "country": ["Country (of organization)", "Country (from Organization)", "Country"],
    "sector": ["Organization categorization", "Organization categorization (from Organization)",
               "Organization type"],
}


def resolve_columns(df: pd.DataFrame) -> dict[str, str]:
    lower = {c.lower().strip(): c for c in df.columns}
    out = {}
    for key, options in COLUMN_CANDIDATES.items():
        for opt in options:
            if opt.lower() in lower:
                out[key] = lower[opt.lower()]
                break
    missing = {"model", "org", "date"} - out.keys()
    if missing:
        raise KeyError(f"Epoch CSV is missing expected columns: {sorted(missing)}. "
                       f"Found: {list(df.columns)}")
    return out


def file_fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def to_parent(name: str) -> str:
    n = name.strip()
    for pattern, parent in PARENT_MAP.items():
        if re.match(pattern, n, flags=re.IGNORECASE):
            return parent
    return n


def explode_credit(df: pd.DataFrame, cols: dict, roll_up: bool) -> pd.DataFrame:
    """One row per (model, organisation) with fractional credit 1/k."""
    base = df[[cols["model"], cols["org"], cols["date"]]].copy()
    base.columns = ["model", "org_raw", "date"]
    base["date"] = pd.to_datetime(base["date"], errors="coerce")
    base = base.dropna(subset=["date", "org_raw"])
    base["year"] = base["date"].dt.year

    rows = []
    for r in base.itertuples(index=False):
        names = [o.strip() for o in str(r.org_raw).split(",") if o.strip()]
        if roll_up:
            names = [to_parent(o) for o in names]
        names = list(dict.fromkeys(names))  # dedupe after roll-up, keep order
        for o in names:
            rows.append((r.model, r.org_raw, o, r.year, 1 / len(names)))
    return pd.DataFrame(rows, columns=["model", "org_raw", "org", "year", "credit"])


def window_label(end_year: int, window: int) -> str:
    return str(end_year) if window == 1 else f"{end_year - window + 1}-{end_year}"


def credit_table(credit: pd.DataFrame, end_year: int, window: int) -> pd.DataFrame:
    """Per-organisation credit and share for one window. Used by the trace panel."""
    sl = credit[(credit["year"] > end_year - window) & (credit["year"] <= end_year)]
    t = sl.groupby("org", as_index=False)["credit"].sum()
    t["share"] = t["credit"] / t["credit"].sum()
    return t.sort_values("credit", ascending=False).reset_index(drop=True)


def metrics_by_window(credit: pd.DataFrame, top_n: int, window: int,
                      min_models: int = 5) -> pd.DataFrame:
    out = []
    years = sorted(credit["year"].unique())
    for y in years:
        t = credit_table(credit, y, window)
        n_models = credit[(credit["year"] > y - window) & (credit["year"] <= y)]["model"].nunique()
        if n_models < min_models:
            continue
        hhi = float((t["share"] ** 2).sum())
        out.append({
            "year": int(y),
            "window": window_label(int(y), window),
            "models": n_models,
            "distinct_orgs": len(t),
            "top_n_share": float(t["share"].head(top_n).sum()),
            "top_n_orgs": ", ".join(t["org"].head(top_n)),
            "hhi": hhi * 10_000,              # antitrust convention, 0-10,000
            "effective_orgs": 1 / hhi,        # "equivalent number of equal-sized orgs"
        })
    return pd.DataFrame(out)


# ---------- extra views ---------------------------------------------------

def share_matrix(credit: pd.DataFrame, orgs: list[str]) -> pd.DataFrame:
    """Rows = orgs, columns = year, value = that org's share of the year's credit."""
    yearly = credit.groupby(["year", "org"])["credit"].sum()
    totals = credit.groupby("year")["credit"].sum()
    share = (yearly / totals).unstack("year").fillna(0.0)
    return share.reindex(orgs).fillna(0.0)


def lorenz(credit_tbl: pd.DataFrame) -> pd.DataFrame:
    """Cumulative share of models vs cumulative share of orgs, smallest orgs first.
    Perfect equality is the diagonal; the further the curve sags, the more concentrated."""
    c = credit_tbl.sort_values("credit")["credit"].to_numpy()
    n = len(c)
    xs = [0.0] + [(i + 1) / n for i in range(n)]
    ys = [0.0] + list((c.cumsum() / c.sum()))
    return pd.DataFrame({"org_share": xs, "model_share": ys})


def gini(credit_tbl: pd.DataFrame) -> float:
    lz = lorenz(credit_tbl)
    x, y = lz["org_share"].to_numpy(), lz["model_share"].to_numpy()
    area = float(((x[1:] - x[:-1]) * (y[1:] + y[:-1]) / 2).sum())
    return 1 - 2 * area


def entrants_by_year(credit: pd.DataFrame) -> pd.DataFrame:
    """Orgs shipping their first model in the dataset that year vs returning orgs."""
    first = credit.groupby("org")["year"].min()
    per_year = credit.groupby("year")["org"].unique()
    rows = []
    for y, orgs in per_year.items():
        new = sum(first[o] == y for o in orgs)
        rows.append({"year": int(y), "new": int(new), "returning": int(len(orgs) - new)})
    return pd.DataFrame(rows)


def split_field_by_year(df: pd.DataFrame, cols: dict, field: str, keep: list[str] | None = None,
                        top_k: int = 3) -> pd.DataFrame:
    """Share of models by a comma-separated attribute (sector or country), 1/k credit.
    Long format: year, group, share. Anything outside the top_k groups -> 'Other'."""
    if field not in cols:
        return pd.DataFrame(columns=["year", "group", "share"])
    d = df[[cols["date"], cols[field]]].copy()
    d.columns = ["date", "val"]
    d["year"] = pd.to_datetime(d["date"], errors="coerce").dt.year
    d = d.dropna(subset=["year", "val"])
    rows = []
    for r in d.itertuples(index=False):
        vals = list(dict.fromkeys(v.strip() for v in str(r.val).split(",") if v.strip()))
        for v in vals:
            rows.append((int(r.year), v, 1 / len(vals)))
    long = pd.DataFrame(rows, columns=["year", "group", "credit"])
    if keep is None:
        keep = long.groupby("group")["credit"].sum().nlargest(top_k).index.tolist()
    long["group"] = long["group"].where(long["group"].isin(keep), "Other")
    g = long.groupby(["year", "group"], as_index=False)["credit"].sum()
    g["share"] = g["credit"] / g.groupby("year")["credit"].transform("sum")
    return g[["year", "group", "share"]]
