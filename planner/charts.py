import matplotlib.pyplot as plt
import numpy as np


def fan_chart(paths, target, years):
    months = np.arange(paths.shape[0]) / 12
    p10, p25, p50, p75, p90 = np.percentile(paths, [10, 25, 50, 75, 90], axis=1)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(months, p10, p90, alpha=0.15, color="tab:green", label="10-90%")
    ax.fill_between(months, p25, p75, alpha=0.3, color="tab:green", label="25-75%")
    ax.plot(months, p50, color="tab:green", lw=2, label="median")
    ax.axhline(target, color="tab:red", ls="--", lw=1.2, label="target")
    ax.set_xlabel("years")
    ax.set_ylabel("portfolio value (Rs)")
    ax.set_xlim(0, years)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v / 1e5:.0f}L" if v < 1e7 else f"{v / 1e7:.1f}Cr")
    ax.legend(loc="upper left", frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig
