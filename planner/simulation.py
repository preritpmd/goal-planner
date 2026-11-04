"""Monte Carlo engine.

Each simulated future is a sequence of yearly portfolio returns. Inside a year
the return is spread evenly over 12 months and the SIP goes in at the start of
every month. The SIP can step up once a year.

Equity returns are either bootstrapped from real calendar-year history or drawn
from a normal distribution. Debt and gold are always normal, and the three are
treated as independent. That is a simplification, see the README.
"""
from dataclasses import dataclass, field

import numpy as np

INFLATION = 0.06


@dataclass
class Goal:
    name: str
    target: float          # in today's rupees
    years: int
    sip: float             # monthly
    savings: float = 0.0   # already set aside for this goal
    step_up: float = 0.0   # yearly SIP increase, 0.05 = 5%
    inflate: bool = True

    def future_target(self):
        if self.inflate:
            return self.target * (1 + INFLATION) ** self.years
        return self.target


@dataclass
class ReturnModel:
    mode: str = "bootstrap"                    # bootstrap | normal | fixed
    equity_history: np.ndarray = field(default_factory=lambda: np.array([0.10]))
    haircut: float = 0.03                      # knocked off equity returns
    equity_mean: float = 0.12
    equity_sd: float = 0.16
    debt_mean: float = 0.07
    debt_sd: float = 0.025
    gold_mean: float = 0.08
    gold_sd: float = 0.13


def simulate(goal, alloc, model, runs=2000, seed=42, keep_paths=False):
    """Run the simulation. Returns (final_values, paths).

    paths has shape (months + 1, runs) when keep_paths is True, else None.
    """
    w_eq, w_db, w_gd = (a / 100 for a in alloc)
    rng = np.random.default_rng(seed)
    years = int(goal.years)

    hist = np.asarray(model.equity_history, dtype=float)
    pick = rng.integers(0, len(hist), size=(runs, years))
    z_eq = rng.standard_normal((runs, years))
    z_db = rng.standard_normal((runs, years))
    z_gd = rng.standard_normal((runs, years))

    value = np.full(runs, float(goal.savings))
    sip = float(goal.sip)
    paths = None
    if keep_paths:
        paths = np.empty((years * 12 + 1, runs))
        paths[0] = value

    for y in range(years):
        if y > 0:
            sip *= 1 + goal.step_up

        if model.mode == "bootstrap":
            eq = hist[pick[:, y]] - model.haircut
        elif model.mode == "normal":
            eq = model.equity_mean - model.haircut + model.equity_sd * z_eq[:, y]
        else:  # fixed, no randomness at all, used for testing
            eq = np.full(runs, model.equity_mean - model.haircut)

        if model.mode == "fixed":
            db = np.full(runs, model.debt_mean)
            gd = np.full(runs, model.gold_mean)
        else:
            db = model.debt_mean + model.debt_sd * z_db[:, y]
            gd = model.gold_mean + model.gold_sd * z_gd[:, y]

        g = np.maximum(w_eq * eq + w_db * db + w_gd * gd, -0.95)
        monthly = (1 + g) ** (1 / 12) - 1

        for m in range(12):
            value = (value + sip) * (1 + monthly)
            if paths is not None:
                paths[y * 12 + m + 1] = value

    return value, paths


def success_probability(final, target):
    return float(np.mean(final >= target))


def percentiles(final, qs=(10, 50, 90)):
    return {q: float(np.percentile(final, q)) for q in qs}


def total_invested(goal):
    total, sip = float(goal.savings), float(goal.sip)
    for y in range(int(goal.years)):
        if y > 0:
            sip *= 1 + goal.step_up
        total += sip * 12
    return total


def sip_needed(goal, alloc, model, wanted=0.8, runs=2000, seed=42):
    """Smallest monthly SIP (rounded up to 500) that reaches `wanted` probability.

    Plain bisection. Returns None if even a very large SIP can't get there.
    """
    target = goal.future_target()

    def p(sip):
        g = Goal(goal.name, goal.target, goal.years, sip, goal.savings,
                 goal.step_up, goal.inflate)
        final, _ = simulate(g, alloc, model, runs, seed)
        return success_probability(final, target)

    lo, hi = goal.sip, 1_000_000.0
    if p(hi) < wanted:
        return None
    for _ in range(25):
        mid = (lo + hi) / 2
        if p(mid) >= wanted:
            hi = mid
        else:
            lo = mid
    return float(np.ceil(hi / 500) * 500)
