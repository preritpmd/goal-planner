
"""Plain-language explanation of financial simulation results.

Uses Gemini when GEMINI_API_KEY is configured.
Falls back to the offline template if Gemini is unavailable.
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
    """Ask Gemini to explain simulation results. Returns None if unavailable."""

    key = os.environ.get("GEMINI_API_KEY")

    if not key:
        return None

    try:
        from google import genai

        client = genai.Client(api_key=key)

        response = client.models.generate_content(
            model=os.environ.get("GEMINI_MODEL", "gemini-flash-latest"),
            contents=(
                "Explain this investment simulation result to a first-time investor "
                "in under 120 words. Use simple language. No hype and no buy/sell advice. "
                "Clearly mention that simulations are not guarantees.\n\n"
                + facts
            ),
        )

        return response.text.strip() if response.text else None

    except Exception as e:
        print(f"Gemini explanation unavailable: {e}")
        return None
