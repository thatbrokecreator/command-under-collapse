"""
01_bond_liquidity_regime.py
Generates Figure 1: Hypothetical Overhang Curves and U.S. Monetary Context, 1939-1944.
Matches Appendix A.0 and Section 3.1 of v21.
"""

import numpy as np
import matplotlib.pyplot as plt


def run_macro_context(save_path="fig1_macro_overhang_context.png"):
    k = np.arange(0, 36)
    overhang_unbuf = 100.0 + 3.4 * k + 6.5 * np.sin(k / 3.2)
    overhang_vol = 100.0 + 2.1 * k + 4.2 * np.sin(k / 3.2)
    overhang_mix = 100.0 + 0.72 * k + 1.8 * np.sin(k / 4.0)

    years = np.array([1939, 1940, 1941, 1942, 1943, 1944])
    m1_billions = np.array([34.15, 39.65, 46.52, 55.36, 72.24, 85.34])
    gnp_billions = np.array([90.5, 99.7, 124.5, 157.9, 191.6, 210.1])

    m1_index = (m1_billions / m1_billions[0]) * 100.0
    m1_gnp_pct = (m1_billions / gnp_billions) * 100.0

    plt.rcParams.update({
        "font.family": "sans-serif",
        "axes.spines.top": True,
        "axes.spines.right": True,
    })

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.2), dpi=300)
    fig.suptitle(
        "Hypothetical Overhang Curves and U.S. Monetary Context, 1939–1944",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    # Panel A
    ax = axes[0]
    ax.plot(k, overhang_unbuf, color="#1F5FA8", lw=2.2, label="Hypothetical unbuffered")
    ax.plot(k, overhang_vol, color="#E06D16", lw=2.2, ls="--", label="Hypothetical framing-only")
    ax.plot(k, overhang_mix, color="#2E7D32", lw=2.2, label="Hypothetical combined policy")
    ax.set_title("A. Hypothetical overhang curves", fontsize=11.5)
    ax.set_xlabel("Index k (0–35)", fontsize=10.5)
    ax.set_ylabel("Hypothetical index (base = 100)", fontsize=10.5)
    ax.set_ylim(95, 222)
    ax.grid(True, linestyle="-", alpha=0.35)
    ax.legend(loc="upper left", frameon=True, fontsize=9)

    # Panel B
    ax = axes[1]
    ax.plot(years, m1_index, color="#1F5FA8", lw=2.2, marker="o", markersize=6.5)
    for yr, val in zip(years, m1_index):
        ax.annotate(
            f"{val:.1f}",
            (yr, val),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
        )
    ax.set_title("B. U.S. M1 index (1939 = 100)", fontsize=11.5)
    ax.set_xlabel("Year", fontsize=10.5)
    ax.set_ylabel("Index (1939 = 100)", fontsize=10.5)
    ax.set_xticks(years)
    ax.set_ylim(80, 275)
    ax.grid(True, linestyle="-", alpha=0.35)

    # Panel C
    ax = axes[2]
    ax.plot(years, m1_gnp_pct, color="#1F5FA8", lw=2.2, marker="s", markersize=6)
    for yr, val in zip(years, m1_gnp_pct):
        offset_y = -14 if yr == 1942 else 8
        ax.annotate(
            f"{val:.1f}",
            (yr, val),
            textcoords="offset points",
            xytext=(0, offset_y),
            ha="center",
            fontsize=9,
        )
    ax.set_title("C. M1 as a share of nominal GNP", fontsize=11.5)
    ax.set_xlabel("Year", fontsize=10.5)
    ax.set_ylabel("Percent (%)", fontsize=10.5)
    ax.set_xticks(years)
    ax.set_ylim(32, 44.5)
    ax.grid(True, linestyle="-", alpha=0.35)

    fig.text(
        0.5,
        0.01,
        "M1: Historical Statistics of the United States. Nominal GNP: Economic Report of the President, 1975.",
        ha="center",
        fontsize=8.5,
        color="#374151",
    )

    plt.tight_layout(rect=[0, 0.035, 1, 0.92])
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.close(fig)
    return {
        "years": years,
        "m1_index": np.round(m1_index, 1),
        "m1_gnp_pct": np.round(m1_gnp_pct, 1),
    }


if __name__ == "__main__":
    res = run_macro_context()
    print("M1 Index (1939=100):", res["m1_index"])
    print("M1 / GNP (%):", res["m1_gnp_pct"])
