"""
03_institutional_authority_network.py
Generates Figure 3 (Ordered Channel Gains & Supermodularity, Table 2, and Role-Differentiated Check)
and Figure 4 (Authority, Operational Capacity & Transmission Topology).
Matches Appendix A.2 and Sections 2.3 & 3.3 of:
"Mobility Friction, Compliance, and Wartime Staffing: Administrative Roles in World War II"
"""

import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


def simulate_compliance_panel(
    n_draws=600,
    n_agents=800,
    seed=909,
    ch_strength=0.018,
    synergy_const=0.20,
    overlap_const=0.50,
    shock_scale=0.08,
):
    rng = np.random.default_rng(seed)
    steps = 35
    specs = ["Additive Linear", "Saturating (ceiling)", "Supermodular Synergy", "Substitutive Overlap"]
    subsets = list(itertools.product([0, 1], repeat=3))
    perms = list(itertools.permutations([0, 1, 2]))

    step_gains = {s: np.zeros((n_draws, 3)) for s in specs}
    supermod = {s: np.zeros(n_draws) for s in specs}
    y_zero = np.zeros(n_draws)
    y_full = {s: np.zeros(n_draws) for s in specs}
    role_drops = np.zeros((n_draws, 3))
    role_full = np.zeros(n_draws)

    t_arr = np.arange(1, steps + 1)
    base_profile = np.where(t_arr < 6, 0.002, shock_scale * np.exp(-0.05 * (t_arr - 6)) + 0.002)

    for d in range(n_draws):
        c0 = np.clip(rng.normal(0.70, 0.06, size=n_agents), 0.35, 0.90)
        eps = rng.normal(0.0, 0.020, size=(steps, n_agents))
        w = rng.uniform(0.05, 0.30, size=3)
        shock_mult = rng.uniform(0.08, 0.24)
        k_peer = rng.uniform(0.05, 0.16)

        # Role-specific draw parameters
        tau = rng.uniform(0.78, 0.92, size=3)
        k_c = rng.uniform(0.0, 0.12)
        k_int = rng.uniform(0.0, 0.15)

        sh_base_t = np.where(t_arr < 6, 0.002, shock_scale * shock_mult * np.exp(-0.05 * (t_arr - 6)) + 0.002)

        for spec in specs:
            outcomes = {}
            for sub in subsets:
                e = np.array([w[m] if sub[m] else 0.0 for m in range(3)])
                n_act = sum(sub)
                e_sum = float(np.sum(e))
                c = c0.copy()

                for t_idx in range(steps):
                    c_bar = float(np.mean(c))
                    peer = k_peer * (c_bar - c)

                    if n_act == 0:
                        ch_term = 0.0
                    elif spec == "Additive Linear":
                        ch_term = ch_strength * e_sum
                    elif spec == "Saturating (ceiling)":
                        ch_term = ch_strength * ((1.0 - c) / 0.30) * e_sum
                    elif spec == "Supermodular Synergy":
                        ch_term = ch_strength * (1.0 + synergy_const * max(n_act - 1, 0)) * e_sum
                    elif spec == "Substitutive Overlap":
                        ch_term = ch_strength * e_sum / (1.0 + overlap_const * max(n_act - 1, 0))

                    c = np.clip(c - sh_base_t[t_idx] + peer + ch_term + eps[t_idx], 0.0, 1.0)

                outcomes[sub] = float(np.mean(c)) * 100.0

            if spec == "Additive Linear":
                y_zero[d] = outcomes[(0, 0, 0)]
            y_full[spec][d] = outcomes[(1, 1, 1)]

            # Ordered addition across all 6 permutations
            p_g1, p_g2, p_g3 = [], [], []
            for p in perms:
                s1 = tuple(1 if i == p[0] else 0 for i in range(3))
                s2 = tuple(1 if i in (p[0], p[1]) else 0 for i in range(3))
                s3 = (1, 1, 1)
                p_g1.append(outcomes[s1] - outcomes[(0, 0, 0)])
                p_g2.append(outcomes[s2] - outcomes[s1])
                p_g3.append(outcomes[s3] - outcomes[s2])

            step_gains[spec][d] = [np.mean(p_g1), np.mean(p_g2), np.mean(p_g3)]

            # Pairwise supermodularity averaged across the 3 pairs
            pairs = [((1, 1, 0), (1, 0, 0), (0, 1, 0)),
                     ((1, 0, 1), (1, 0, 0), (0, 0, 1)),
                     ((0, 1, 1), (0, 1, 0), (0, 0, 1))]
            sm_vals = [outcomes[ij] - outcomes[i] - outcomes[j] + outcomes[(0, 0, 0)] for ij, i, j in pairs]
            supermod[spec][d] = np.mean(sm_vals)

        # Role-differentiated check (full & leave-one-out)
        role_subsets = [(1, 1, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
        role_out = {}
        for sub in role_subsets:
            e = np.array([w[m] if sub[m] else 0.0 for m in range(3)])
            n_act = sum(sub)
            c = c0.copy()
            sh_eff_t = sh_base_t * max(0.35, 1.0 - 0.85 * e[2])
            drag_t = 0.01 * k_c * max(n_act - 1, 0)

            for t_idx in range(steps):
                c_bar = float(np.mean(c))
                peer = (k_peer + 0.25 * e[0]) * (c_bar - c)
                thresh = 0.06 * sum(e[m] * np.maximum(tau[m] - c, 0.0) for m in range(3))
                inter = 0.015 * k_int * (e[0] / 0.30) * ((e[1] + e[2]) / 0.60) * np.clip(1.0 - c, 0.0, 1.0)
                c = np.clip(c - sh_eff_t[t_idx] + peer + thresh + inter - drag_t + eps[t_idx], 0.0, 1.0)

            role_out[sub] = float(np.mean(c)) * 100.0

        role_full[d] = role_out[(1, 1, 1)]
        role_drops[d, 0] = role_out[(1, 1, 1)] - role_out[(0, 1, 1)]
        role_drops[d, 1] = role_out[(1, 1, 1)] - role_out[(1, 0, 1)]
        role_drops[d, 2] = role_out[(1, 1, 1)] - role_out[(1, 1, 0)]

    return {
        "specs": specs,
        "step_gains": step_gains,
        "supermod": supermod,
        "y_zero": y_zero,
        "y_full": y_full,
        "role_full": role_full,
        "role_drops": role_drops,
    }


def plot_figure_3(res, save_path="fig3_ordered_channel_gains.png"):
    specs = res["specs"]
    colors = ["#6B7280", "#1E3A8A", "#15803D", "#B45309"]
    n_draws = len(res["y_zero"])

    plt.rcParams.update({"font.family": "serif"})
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), dpi=300)
    fig.suptitle(
        f"Ordered Channel Gains Across Symmetric Specifications (seed = 909, {n_draws} draws; "
        f"zero-channel baseline = {np.mean(res['y_zero']):.1f}%)",
        fontsize=12.5,
        fontweight="bold",
        y=0.98,
    )

    # Panel A: Grouped bar chart
    ax = axes[0]
    x = np.arange(3)
    width = 0.19
    for i, (spec, col) in enumerate(zip(specs, colors)):
        means = np.mean(res["step_gains"][spec], axis=0)
        ses = np.std(res["step_gains"][spec], axis=0, ddof=1) / np.sqrt(n_draws)
        ax.bar(
            x + (i - 1.5) * width,
            means,
            width=width,
            color=col,
            yerr=ses,
            capsize=3,
            label=spec,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(["Step 1\n(1st channel)", "Step 2\n(2nd channel)", "Step 3\n(3rd channel)"])
    ax.set_ylabel("Mean marginal compliance gain (pp ± 1 SE)", fontsize=10)
    ax.set_title("A. Ordered addition gains (all 6 permutations)", fontsize=11)
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)
    ax.legend(loc="upper left", frameon=True, fontsize=9)

    # Panel B: Pairwise supermodularity
    ax = axes[1]
    sm_means = [np.mean(res["supermod"][s]) for s in specs]
    sm_ses = [np.std(res["supermod"][s], ddof=1) / np.sqrt(n_draws) for s in specs]
    x_sm = np.arange(len(specs))
    ax.bar(x_sm, sm_means, width=0.52, color=colors, yerr=sm_ses, capsize=3)
    ax.axhline(0, color="black", lw=0.9)
    ax.set_xticks(x_sm)
    ax.set_xticklabels([
        "Additive\nLinear",
        "Saturating\n(ceiling)",
        "Supermodular\nSynergy",
        "Substitutive\nOverlap",
    ])
    ax.set_ylabel("Pairwise supermodularity (pp ± 1 SE)", fontsize=10)
    ax.set_title("B. Pairwise supermodularity by specification", fontsize=11)
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_figure_4(save_path="fig4_transmission_topology.png"):
    plt.rcParams.update({"font.family": "serif"})
    fig, ax = plt.subplots(figsize=(13.5, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_title(
        "Authority, Operational Capacity & Transmission Topology Across Six Wartime Officials",
        fontsize=13,
        fontweight="bold",
        pad=10,
    )

    officials = [
        ("Rosenberg\n(WMC Region II)", 5.6, "#2563EB"),
        ("Perkins\n(Dept. of Labor)", 4.6, "#16A34A"),
        ("Elliott\n(OPACS Consumer)", 3.6, "#F97316"),
        ("Dulles\n(State / Bretton Woods)", 2.6, "#16A34A"),
        ("Wilkinson\n(UK Home Security PS)", 1.6, "#8B5CF6"),
        ("Horsbrugh\n(UK Health / Food PS)", 0.6, "#8B5CF6"),
    ]

    channels = [
        ("Referral & Transfer\nRouting (Friction f)", 5.3),
        ("Labor Standards &\nWage Admin", 4.2),
        ("Framing & Norm\nChannel", 3.1),
        ("Monetary & FX\nHorizon Planning", 2.0),
        ("Civilian Welfare &\nShock Continuity", 0.9),
    ]

    outcome = ("Workforce &\nCompliance Continuity", 3.1, "#DC2626")

    edges_left = [
        (0, 0, 2.4),
        (1, 0, 1.3),
        (1, 1, 2.2),
        (2, 2, 2.2),
        (3, 3, 2.2),
        (4, 4, 2.2),
        (5, 4, 2.2),
    ]

    x_left, x_mid, x_right = 2.0, 4.9, 7.9

    for u, v, lw in edges_left:
        y1 = officials[u][1]
        y2 = channels[v][1]
        arrow = FancyArrowPatch(
            (x_left + 0.18, y1),
            (x_mid - 0.18, y2),
            connectionstyle="arc3,rad=0.04",
            arrowstyle="-|>,head_length=5,head_width=3",
            lw=lw,
            color="#6B7280",
            alpha=0.85,
        )
        ax.add_patch(arrow)

    for idx, (_, y1) in enumerate(channels):
        lw = 2.5 if idx == 0 else 2.0
        arrow = FancyArrowPatch(
            (x_mid + 0.18, y1),
            (x_right - 0.18, outcome[1]),
            connectionstyle="arc3,rad=-0.04",
            arrowstyle="-|>,head_length=5,head_width=3",
            lw=lw,
            color="#6B7280",
            alpha=0.85,
        )
        ax.add_patch(arrow)

    for label, y, col in officials:
        ax.scatter([x_left], [y], s=780, color=col, edgecolors="black", linewidths=1.2, zorder=4)
        ax.text(x_left - 0.30, y, label, ha="right", va="center", fontsize=9.2, fontweight="bold", color="#1F2937")

    for label, y in channels:
        ax.scatter([x_mid], [y], s=780, color="#737373", edgecolors="black", linewidths=1.2, zorder=4)
        ax.text(x_mid, y + 0.36, label, ha="center", va="bottom", fontsize=9.0, fontweight="bold", color="#1F2937")

    ax.scatter([x_right], [outcome[1]], s=920, color=outcome[2], edgecolors="black", linewidths=1.2, zorder=4)
    ax.text(x_right + 0.30, outcome[1], outcome[0], ha="left", va="center", fontsize=9.5, fontweight="bold", color="#1F2937")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    results = simulate_compliance_panel(n_draws=600, n_agents=800, seed=909)
    plot_figure_3(results)
    plot_figure_4()
    print("Saved Figure 3 and Figure 4.")
