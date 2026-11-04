import pandas as pd
import streamlit as st

from planner.allocation import allocation
from planner.charts import fan_chart
from planner.data import calendar_year_returns, fetch_nav, load_bundled_equity, search_schemes
from planner.explain import inr, llm_explanation, template_explanation
from planner.simulation import (Goal, ReturnModel, percentiles, simulate, sip_needed,
                                success_probability, total_invested)

st.set_page_config(page_title="Goal Planner", layout="wide")
st.title("Goal Planner")
st.caption("Pick a goal, see how likely your plan is to get there. Simulation only, not financial advice.")

# ---------- sidebar: settings that apply to every goal ----------
with st.sidebar:
    st.header("Settings")
    risk = st.radio("Risk appetite", ["low", "medium", "high"], index=1, horizontal=True)
    mode_label = st.selectbox("Equity return model", ["Historical bootstrap", "Normal (12% / 16%)"])
    haircut = st.slider("Equity haircut (percentage points)", 0.0, 8.0, 3.0, 0.5,
                        help="The 2006-2024 average is flattered by the 2006-2009 run, so this knocks a bit off.")
    runs = st.select_slider("Simulation runs", [500, 1000, 2000, 5000], value=2000)

    equity_history = load_bundled_equity()
    source = "Nifty 50 TRI, 2006-2024 (bundled CSV)"

    with st.expander("Use a different fund's history (mfapi.in)"):
        query = st.text_input("Search funds", placeholder="e.g. nifty 50 index direct growth")
        if query:
            try:
                found = search_schemes(query)
                label = st.selectbox("Fund", [f"{s['schemeCode']} - {s['schemeName']}" for s in found]) if found else None
                if label and st.button("Load history"):
                    rets = calendar_year_returns(fetch_nav(label.split(" - ")[0]))
                    if len(rets) >= 8:
                        st.session_state["hist"] = (rets, label)
                    else:
                        st.warning("That fund has fewer than 8 full years of data, keeping the default.")
            except Exception as e:
                st.warning(f"Couldn't reach mfapi.in ({type(e).__name__}). Using the bundled data.")
        if "hist" in st.session_state:
            equity_history, source = st.session_state["hist"][0], st.session_state["hist"][1]
    st.caption(f"Equity history: {source}")

model = ReturnModel(
    mode="bootstrap" if mode_label.startswith("Hist") else "normal",
    equity_history=equity_history,
    haircut=haircut / 100,
)

# ---------- goals table ----------
st.subheader("Your goals")
default = pd.DataFrame([
    {"name": "House down payment", "target": 2_500_000, "years": 8, "sip": 25000,
     "savings": 100000, "step_up_pct": 5.0, "inflate": True},
    {"name": "Higher studies", "target": 4_000_000, "years": 5, "sip": 30000,
     "savings": 50000, "step_up_pct": 5.0, "inflate": True},
])
table = st.data_editor(default, num_rows="dynamic", width='stretch', hide_index=True,
                       column_config={
                           "target": st.column_config.NumberColumn("target (today's Rs)", min_value=0, step=50000),
                           "years": st.column_config.NumberColumn(min_value=1, max_value=30, step=1),
                           "sip": st.column_config.NumberColumn("monthly SIP", min_value=0, step=500),
                           "savings": st.column_config.NumberColumn("current savings", min_value=0, step=10000),
                           "step_up_pct": st.column_config.NumberColumn("yearly step-up %", min_value=0, max_value=20),
                           "inflate": st.column_config.CheckboxColumn("adjust for 6% inflation"),
                       })
table = table.dropna(subset=["name", "target", "years", "sip"])
if table.empty:
    st.info("Add at least one goal above.")
    st.stop()


def row_to_goal(r):
    return Goal(str(r["name"]), float(r["target"]), int(r["years"]), float(r["sip"]),
                float(r.get("savings") or 0), float(r.get("step_up_pct") or 0) / 100,
                bool(r.get("inflate", True)))


goals = [row_to_goal(r) for _, r in table.iterrows()]

# ---------- comparison ----------
rows = []
for g in goals:
    al = allocation(g.years, risk)
    final, _ = simulate(g, al, model, runs)
    rows.append({"goal": g.name, "target (future)": inr(g.future_target()), "years": g.years,
                 "mix E/D/G": "/".join(map(str, al)),
                 "chance": f"{success_probability(final, g.future_target()) * 100:.0f}%",
                 "median": inr(percentiles(final)[50])})
st.subheader("Comparison")
st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)

# ---------- detail for one goal ----------
st.subheader("Details")
pick = st.selectbox("Goal", [g.name for g in goals])
goal = goals[[g.name for g in goals].index(pick)]
alloc = allocation(goal.years, risk)
target = goal.future_target()

final, paths = simulate(goal, alloc, model, runs, keep_paths=True)
prob = success_probability(final, target)
pc = percentiles(final)
invested = total_invested(goal)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Chance of reaching it", f"{prob * 100:.0f}%")
c2.metric("Median outcome", inr(pc[50]))
c3.metric("Bad case (10th pct)", inr(pc[10]))
c4.metric("You invest", inr(invested))

if prob >= 0.8:
    st.success("On track. Keep a buffer anyway, markets can be rough.")
else:
    need = sip_needed(goal, alloc, model, 0.8, runs)
    if need:
        st.warning(f"A SIP of about Rs {need:,.0f} a month would get you to an 80% chance "
                   f"(you plan Rs {goal.sip:,.0f}).")
    else:
        st.error("Even a very large SIP doesn't reach 80% on this timeline. Consider a longer horizon or a lower target.")

st.pyplot(fan_chart(paths, target, goal.years))
st.caption(f"Allocation: {alloc[0]}% equity, {alloc[1]}% debt, {alloc[2]}% gold. "
           f"Target in {goal.years} years: {inr(target)}.")

st.subheader("In plain words")
facts = (f"Goal '{goal.name}', target {inr(target)} in {goal.years} years, SIP Rs {goal.sip:,.0f}/month, "
         f"allocation {alloc} (equity/debt/gold %), chance of success {prob * 100:.0f}%, "
         f"median {inr(pc[50])}, 10th percentile {inr(pc[10])}, 90th percentile {inr(pc[90])}, "
         f"total invested {inr(invested)}.")
text = llm_explanation(facts) if st.toggle("Write it with Claude (needs ANTHROPIC_API_KEY)") else None
st.write(text or template_explanation(goal, alloc, prob, pc[10], pc[50], pc[90], invested))

with st.expander("Assumptions"):
    st.markdown(
        "- Equity: actual calendar-year returns drawn at random (or a normal distribution), minus the haircut.\n"
        "- Debt 7% +/- 2.5% and gold 8% +/- 13% are assumptions, not historical data.\n"
        "- The three asset classes are treated as independent, and the mix is rebalanced yearly.\n"
        "- No taxes, fund costs or exit loads. Past returns do not predict future returns."
    )
