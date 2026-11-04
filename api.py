"""FastAPI backend for the web frontend. Run with: uvicorn api:app --reload"""
from pathlib import Path
from typing import Literal

import numpy as np
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from planner.allocation import allocation
from planner.data import load_bundled_equity
from planner.explain import llm_explanation, template_explanation
from planner.simulation import (Goal, ReturnModel, percentiles, simulate, sip_needed,
                                success_probability, total_invested)

app = FastAPI(title="Goal Planner")
HISTORY = load_bundled_equity()


class GoalIn(BaseModel):
    name: str = "My goal"
    target: float = Field(ge=0)
    years: int = Field(ge=1, le=30)
    sip: float = Field(ge=0)
    savings: float = Field(0, ge=0)
    step_up: float = Field(0, ge=0, le=0.2)
    inflate: bool = True


class SimRequest(BaseModel):
    goal: GoalIn
    others: list[GoalIn] = []
    risk: Literal["low", "medium", "high"] = "medium"
    mode: Literal["bootstrap", "normal"] = "bootstrap"
    haircut: float = Field(0.03, ge=0, le=0.1)
    use_ai: bool = False


def _model(req):
    return ReturnModel(mode=req.mode, equity_history=HISTORY, haircut=req.haircut)


@app.post("/api/simulate")
def run(req: SimRequest):
    model = _model(req)
    goal = Goal(**req.goal.model_dump())
    alloc = allocation(goal.years, req.risk)
    target = goal.future_target()

    final, paths = simulate(goal, alloc, model, keep_paths=True)
    prob = success_probability(final, target)
    pc = percentiles(final)
    invested = total_invested(goal)
    need = None if prob >= 0.8 else sip_needed(goal, alloc, model)

    text = None
    if req.use_ai:
        text = llm_explanation(
            f"Goal '{goal.name}', target Rs {target:,.0f} in {goal.years} years, SIP Rs {goal.sip:,.0f}/month, "
            f"allocation {alloc} (equity/debt/gold %), chance {prob * 100:.0f}%, median Rs {pc[50]:,.0f}, "
            f"10th percentile Rs {pc[10]:,.0f}, 90th Rs {pc[90]:,.0f}.")
    if not text:
        text = template_explanation(goal, alloc, prob, pc[10], pc[50], pc[90], invested)

    others = []
    for o in req.others:
        g = Goal(**o.model_dump())
        f, _ = simulate(g, allocation(g.years, req.risk), model)
        others.append({"prob": success_probability(f, g.future_target())})

    return {
        "prob": prob, "target": target, "invested": invested, "alloc": alloc,
        "p10": pc[10], "p50": pc[50], "p90": pc[90], "need": need,
        "bands": np.percentile(paths, [10, 25, 50, 75, 90], axis=1).round(0).tolist(),
        "explanation": text, "others": others,
    }


app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")
