# Goal Planner

A small Streamlit app that answers one question: *if I put this much away every month, how likely am I to reach my goal?*

You give it a goal (target amount, years, monthly SIP, savings so far, risk appetite). It picks an equity/debt/gold split, runs a few thousand simulated futures, and tells you the chance of getting there, plus what a bad, typical and good outcome look like. If your odds are below 80% it works out roughly what SIP would get you there.

I built this for a problem statement on investment planning for first-time investors. It is a learning project. It is not advice and it does not touch real money.

## Run it

```bash
git clone <your-repo-url>
cd goal-planner
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

That starts the Streamlit version. There is also a custom web frontend (FastAPI backend, plain HTML/JS, no build step):

```bash
uvicorn api:app --reload
```

then open http://localhost:8000. You write your goal as a sentence, and the chart, the "X in 100" dots and the suggested SIP update as you type.

Run the tests with `pytest`.

## How it works

- `planner/allocation.py` - equity share depends on the goal's horizon (10% under 2 years, up to 70% past 10), shifted by risk appetite. Gold is capped at 10%, debt takes the rest.
- `planner/simulation.py` - the Monte Carlo engine. Each run draws one return per year for each asset class, converts it to a monthly rate, and compounds the SIP month by month. Optional yearly step-up and inflation adjustment on the target.
- `planner/data.py` - loads the bundled Nifty 50 TRI calendar-year returns, and can pull another fund's NAV history from [mfapi.in](https://www.mfapi.in/).
- `planner/explain.py` - plain-language summary. A template by default, or Claude if `ANTHROPIC_API_KEY` is set.
- `api.py` and `static/index.html` - the web frontend. `/api/simulate` runs the engine, the page draws everything.
- `app.py` - the Streamlit UI. Goals live in an editable table, so you can compare several side by side.

## Where the numbers come from

- **Equity**: Nifty 50 total-return calendar-year returns for 2006-2024, in `data/nifty50_tri_calendar_returns.csv`. I read these off a Baroda BNP Paribas MF factsheet (Feb 2025), so they are rounded. Please check them against niftyindices.com before relying on them. By default each simulated year picks one of these real years at random, so a 2008-style crash (-51%) can happen.
- **Haircut**: the 2006-2024 average is about 16.8% a year, which is high because of 2006-2009. The app subtracts 3 points by default. Change it in the sidebar.
- **Debt (7% +/- 2.5%) and gold (8% +/- 13%)**: assumptions. I did not have a sourced history for them.

## What it gets wrong

- 19 years is a small sample, and one bull run in it dominates the average.
- Asset classes are treated as independent. In real crashes they often aren't.
- Returns are applied yearly and spread evenly across months, so there is no within-year volatility.
- No tax, expense ratios, exit loads, or rebalancing costs.
- The allocation rules are my own and are simply a starting point.

## Checking the maths

`tests/test_simulation.py` compares the engine against the closed-form SIP future-value formula and against an independent loop for the step-up case, and checks things like "more SIP never lowers the odds" and "same seed, same answer".

## Not tested

The mfapi.in lookup and the Claude explanation need network access or an API key and are not covered by the tests. If either fails, the app falls back to the bundled data and the template text.

## License

MIT
