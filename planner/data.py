"""Historical data helpers.

The bundled CSV is what the app uses by default. The functions further down
talk to mfapi.in so you can swap in a different fund's history if you want.
They need an internet connection and the app falls back to the CSV if they fail.
"""
from pathlib import Path

import pandas as pd
import requests

BUNDLED = Path(__file__).resolve().parent.parent / "data" / "nifty50_tri_calendar_returns.csv"
MFAPI = "https://api.mfapi.in/mf"


def load_bundled_equity():
    """Nifty 50 TRI calendar-year returns as fractions (0.10 means 10%)."""
    df = pd.read_csv(BUNDLED)
    return df["return_pct"].to_numpy() / 100.0


def search_schemes(query, limit=15):
    r = requests.get(f"{MFAPI}/search", params={"q": query}, timeout=10)
    r.raise_for_status()
    return r.json()[:limit]  # list of {schemeCode, schemeName}


def fetch_nav(scheme_code):
    r = requests.get(f"{MFAPI}/{scheme_code}", timeout=15)
    r.raise_for_status()
    rows = r.json()["data"]
    nav = pd.Series(
        [float(x["nav"]) for x in rows],
        index=pd.to_datetime([x["date"] for x in rows], format="%d-%m-%Y"),
    ).sort_index()
    return nav


def calendar_year_returns(nav):
    """Turn a NAV series into full calendar-year returns.

    The first year is dropped (no earlier year-end to compare against) and so
    is the current year if it isn't over yet.
    """
    year_end = nav.groupby(nav.index.year).last()
    rets = year_end.pct_change().dropna()
    if len(rets) and rets.index[-1] == pd.Timestamp.today().year:
        rets = rets.iloc[:-1]
    return rets.to_numpy(dtype=float)
