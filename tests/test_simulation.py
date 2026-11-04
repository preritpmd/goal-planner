import numpy as np
import pytest

from planner.allocation import allocation
from planner.simulation import (Goal, ReturnModel, simulate, success_probability,
                                sip_needed, total_invested)

ALLOC = (55, 35, 10)


def fixed_model():
    return ReturnModel(mode="fixed", haircut=0.0)


def monthly_rate():
    g = 0.55 * 0.12 + 0.35 * 0.07 + 0.10 * 0.08
    return (1 + g) ** (1 / 12) - 1


def test_matches_closed_form_sip_formula():
    goal = Goal("t", 1, years=8, sip=15000, savings=100000, step_up=0.0, inflate=False)
    final, _ = simulate(goal, ALLOC, fixed_model(), runs=10)
    m, n = monthly_rate(), 96
    expected = 100000 * (1 + m) ** n + 15000 * ((1 + m) ** n - 1) / m * (1 + m)
    assert final[0] == pytest.approx(expected, rel=1e-9)


def test_step_up_matches_plain_loop():
    goal = Goal("t", 1, years=8, sip=15000, savings=100000, step_up=0.05, inflate=False)
    final, _ = simulate(goal, ALLOC, fixed_model(), runs=10)
    m, v, sip = monthly_rate(), 100000.0, 15000.0
    for y in range(8):
        if y > 0:
            sip *= 1.05
        for _ in range(12):
            v = (v + sip) * (1 + m)
    assert final[0] == pytest.approx(v, rel=1e-9)


def test_no_money_stays_zero():
    goal = Goal("t", 1, years=5, sip=0, savings=0)
    final, _ = simulate(goal, ALLOC, ReturnModel(mode="normal"), runs=50)
    assert np.all(final == 0)


def test_same_seed_same_answer():
    goal = Goal("t", 1, years=6, sip=10000)
    model = ReturnModel(mode="normal")
    a, _ = simulate(goal, ALLOC, model, runs=200, seed=7)
    b, _ = simulate(goal, ALLOC, model, runs=200, seed=7)
    assert np.array_equal(a, b)


def test_more_sip_never_lowers_the_odds():
    model = ReturnModel(mode="bootstrap", equity_history=np.array([0.4, -0.3, 0.1, 0.2, 0.05]))
    probs = []
    for sip in (10000, 20000, 30000):
        goal = Goal("t", 2_000_000, years=8, sip=sip)
        final, _ = simulate(goal, ALLOC, model)
        probs.append(success_probability(final, goal.future_target()))
    assert probs == sorted(probs)


def test_path_ends_at_final_value():
    goal = Goal("t", 1, years=4, sip=5000, savings=1000)
    final, paths = simulate(goal, ALLOC, ReturnModel(mode="normal"), runs=100, keep_paths=True)
    assert paths.shape == (49, 100)
    assert np.allclose(paths[-1], final)


def test_total_invested():
    goal = Goal("t", 1, years=2, sip=1000, savings=500, step_up=0.10)
    assert total_invested(goal) == pytest.approx(500 + 12000 + 13200)


def test_sip_needed_reaches_the_goal():
    model = ReturnModel(mode="normal")
    goal = Goal("t", 2_000_000, years=8, sip=5000)
    need = sip_needed(goal, ALLOC, model, wanted=0.8)
    assert need is not None and need > 5000
    better = Goal("t", 2_000_000, years=8, sip=need)
    final, _ = simulate(better, ALLOC, model)
    assert success_probability(final, better.future_target()) >= 0.8


@pytest.mark.parametrize("years", [1, 3, 8, 15])
@pytest.mark.parametrize("risk", ["low", "medium", "high"])
def test_allocation_adds_to_100(years, risk):
    eq, db, gd = allocation(years, risk)
    assert eq + db + gd == 100
    assert min(eq, db, gd) >= 0
