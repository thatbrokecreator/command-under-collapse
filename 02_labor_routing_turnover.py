"""
02_labor_routing_turnover.py
Generates Figure 2 (v21 two-panel layout: Panel A twin-axis fill & cumulative quits;
Panel B net-score gains across friction costs c in {4, 8.5, 14} with & without drag)
and runs Appendix A.1.1 penalty sensitivity checks (lambda and gamma).
"""

import numpy as np
import matplotlib.pyplot as plt


def simulate_routing(
    f_grid=None,
    n_runs=200,
    seed=202,
    sh=0.15,
    routing_slope=0.48,
    transfer_slope=0.055,
    quit_red_slope=0.52,
    eff_loss_coeff=0.28,
    drag_coeff=0.22,
    drag_exp=1.3,
):
    if f_grid is None:
        f_grid = np.round(np.arange(0.0, 0.951, 0.05), 2)

    rng = np.random.default_rng(seed)
    steps = 35
    E_t = np.linspace(44.220, 53.960, steps + 1)
    s_t = np.linspace(0.18, 0.42, steps + 1)
    u_draws = rng.uniform(0.65, 1.35, size=(n_runs, steps))

    gross_fill = np.zeros_like(f_grid, dtype=float)
    eff_fill = np.zeros_like(f_grid, dtype=float)
    cum_quits = np.zeros_like(f_grid, dtype=float)

    for idx, f in enumerate(f_grid):
        P = np.full(n_runs, s_t[0] * E_t[0], dtype=float)
        quits_acc = np.zeros(n_runs, dtype=float)
        eta_f = max(0.0, 1.0 - eff_loss_coeff * (f ** 2))

        for t in range(1, steps + 1):
            N_prev = E_t[t - 1] - P
            q_t = P * 0.076 * (1.0 - quit_red_slope * f)
            d_t = P * sh * u_draws[:, t - 1] * (1.0 - 0.22 * f) * 0.14
            r_t = (E_t[t] - E_t[t - 1]) * (0.42 + routing_slope * f) * eta_f

            raw_x = N_prev * (0.035 + transfer_slope * f) * eta_f
            cap_x = 0.50 * np.maximum(s_t[t] * E_t[t] - P, 0.0)
            x_t = np.minimum(raw_x, cap_x)

            P = np.maximum(P + r_t + x_t - q_t - d_t, 0.0)
            quits_acc += q_t

        fill_runs = np.minimum(P / (s_t[steps] * E_t[steps]), 1.05) * 100.0
        mean_fill = float(np.mean(fill_runs))
        gross_fill[idx] = mean_fill
        eff_fill[idx] = mean_fill * max(0.0, 1.0 - drag_coeff * (f ** drag_exp))
        cum_quits[idx] = float(np.mean(quits_acc))

    return f_grid, gross_fill, eff_fill, cum_quits


def run_penalty_sensitivity():
    f_grid, gross_fill, _, _ = simulate_routing(n_runs=200, seed=202, sh=0.15)
    costs = [4.0, 8.5, 14.0]
    print("=== Appendix A.1.1: Mismatch/Productivity Penalty Sensitivity ===")
    for lam in [0.11, 0.22, 0.33]:
        eff = gross_fill * np.maximum(0.0, 1.0 - lam * (f_grid ** 1.3))
        row = []
        for c in costs:
            net = eff - c * (f_grid ** 1.5)
            f_star = f_grid[np.argmax(net)]
            gain = np.max(net) - net[0]
            row.append(f"c={c:4.1f}: f*={f_star:.2f}, gain={gain:.2f}")
        print(f"lambda={lam:.2f} (gamma=1.3) -> " + " | ".join(row))

    for gam in [1.0, 1.3, 1.6]:
        eff = gross_fill * np.maximum(0.0, 1.0 - 0.22 * (f_grid ** gam))
        row = []
        for c in costs:
            net = eff - c * (f_grid ** 1.5)
            f_star = f_grid[np.argmax(net)]
            gain = np.max(net) - net[0]
            row.append(f"c={c:4.1f}: f*={f_star:.2f}, gain={gain:.2f}")
        print(f"gamma ={gam:.2f} (lambda=0.22)-> " + " | ".join(row))


def plot_figure_2(save_path="fig2_labor_routing_friction.png"):
    f_grid, gross_fill, eff_fill, cum_quits = simulate_routing(n_runs=200, seed=202, sh=0.15)

    plt.rcParams.update({"font.family": "sans-serif"})
    fig, axes = plt.subplots(1, 2, figsize=(15.2, 5.4), dpi=300)
    fig.suptitle(
        "Priority Labor Routing: Baseline and Mismatch/Productivity Sensitivity (seed = 202)",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    # Panel A: Twin axis
    ax_left = axes[0]
    ax_right = ax_left.twinx()

    l1, = ax_left.plot(f_grid, gross_fill, color="#1F5FA8", lw=2.3, label="Gross priority fill (%)")
    l2, = ax_left.plot(
        f_grid,
        eff_fill,
        color="#E06D16",
        lw=2.3,
        ls="--",
        label="Mismatch/productivity-adjusted fill (%)",
    )
    l3, = ax_right.plot(
        f_grid,
        cum_quits,
        color="#1F5FA8",
        lw=2.2,
        ls=":",
        label="Cumulative priority quits (millions, right axis)",
    )

    ax_left.set_title("A. Fill and cumulative quits", fontsize=11.5)
    ax_left.set_xlabel("Mobility friction parameter (f)", fontsize=10.5)
    ax_left.set_ylabel("Fill (%)", fontsize=10.5)
    ax_right.set_ylabel("Cumulative priority quits (millions)", fontsize=10.5)
    ax_left.grid(True, linestyle="-", alpha=0.35)

    lines = [l1, l2, l3]
    labels = [l.get_label() for l in lines]
    ax_left.legend(lines, labels, loc="lower left", frameon=True, fontsize=8.8)

    # Panel B: Net-score gains by friction cost
    ax_b = axes[1]
    c_specs = [
        (4.0, "#1F5FA8", "-", "Baseline, c=4"),
        (8.5, "#2E7D32", "-", "Baseline, c=8.5"),
        (14.0, "#7E57C2", "-", "Baseline, c=14"),
        (4.0, "#E06D16", "--", "Drag, c=4"),
        (8.5, "#D32F2F", "--", "Drag, c=8.5"),
        (14.0, "#6D4C41", "--", "Drag, c=14"),
    ]

    for c, col, ls, lbl in c_specs:
        net_b = gross_fill - c * (f_grid ** 1.5)
        net_d = eff_fill - c * (f_grid ** 1.5)
        curve = (net_b - net_b[0]) if lbl.startswith("Baseline") else (net_d - net_d[0])
        ax_b.plot(f_grid, curve, color=col, lw=2.1, ls=ls, label=lbl)

    ax_b.set_title("B. Net-score gains by friction cost", fontsize=11.5)
    ax_b.set_xlabel("Mobility friction parameter (f)", fontsize=10.5)
    ax_b.set_ylabel("Net-score gain over f = 0 (points)", fontsize=10.5)
    ax_b.grid(True, linestyle="-", alpha=0.35)
    ax_b.legend(loc="lower left", ncol=2, frameon=True, fontsize=8.8)

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    plot_figure_2()
    run_penalty_sensitivity()
