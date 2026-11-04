"""Plain-language summary of a result.

Always works offline with a template. If ANTHROPIC_API_KEY is set, the app can
ask Claude to write it instead.
"""
import os


def inr(x):
    if x >= 1e7:
        return f"₹{x / 1e7:.2f} Cr"
    if x >= 1e5:
        return f"₹{x / 1e5:.2f} L"
    return f"₹{x:,.0f}"


def template_explanation(goal, alloc, prob, p10, p50, p90, invested):
    target = goal.future_target()
    text = (
        f"For '{goal.name}' you would put in about {inr(invested)} over {goal.years} years. "
        f"In a typical outcome you end up with around {inr(p50)}, which is "
        f"{'above' if p50 >= target else 'below'} the {inr(target)} you need. "
        f"In a bad run (1 in 10) you would have {inr(p10)} or less, and in a good one "
        f"{inr(p90)} or more. About {prob * 100:.0f}% of the simulated futures reach the target."
    )
    if alloc[0] >= 50:
        text += " The mix is equity-heavy, so the range is wide; 2008 alone lost over half."
    else:
        text += " The mix is on the cautious side, so results are steadier but growth is slower."
    return text


def llm_explanation(facts):
    """Ask Claude for a short explanation. Returns None if it can't."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=key)
        msg = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
            max_tokens=400,
            messages=[{
                "role": "user",
                "content": (
                    "Explain this investment simulation result to a first-time investor in "
                    "under 120 words. Plain language, no hype, no buy/sell advice, and say "
                    "that simulations are not guarantees.\n\n" + facts
                ),
            }],
        )
        return msg.content[0].text
    except Exception:
        return None
