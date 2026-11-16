from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent

# Support both data and Data
DATA_DIR = BASE_DIR / "data"

if not DATA_DIR.exists():
    DATA_DIR = BASE_DIR / "Data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


@st.cache_data
def load_csv(path):
    return pd.read_csv(path)


def load_frontier_data():
    return load_csv(RAW_DIR / "frontier_ai_models.csv")


def load_notable_data():
    return load_csv(RAW_DIR / "notable_ai_models.csv")
    