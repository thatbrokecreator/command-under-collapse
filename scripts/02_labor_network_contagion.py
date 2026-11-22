"""
02_labor_network_contagion.py

Econophysics / constrained-flow network model of wartime labor allocation,
mobility friction (Buffalo Plan controlled-referral mechanics), and exogenous
civilian/health capacity shocks.

Key methodological choices:
1. Civilian vs. total employment: Calibrated to U.S. civilian employment
   growth from 44.142M (1938) to 53.960M (1944), explicitly separating
   civilian workers from armed forces personnel (65.370M total employed).
2. Controlled referral & transfer friction (Anna M. Rosenberg / WMC):
   Models permission requirements on job transfers in priority defense sectors
   as an asymmetric friction parameter—curbing poaching-driven turnover churn
   while routing unassigned workers toward high-priority bottlenecks.
3. Indirect civilian & health shocks (Wilkinson / Horsbrugh channels):
   Introduces localized disruption/absenteeism shocks to test how priority
   output holds up under unconstrained churn vs. controlled referral.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def simulate_labor_allocation(
    turnover_frictions: np.ndarray,
    shock_levels: tuple[float, float, float] = (0.05, 0.15, 0.28),
    civilian_emp_1938_m: float = 44.142,
    civilian_emp_1944_m: float = 53.960,
    n_steps: int = 36,
    n_MonteCarlo: int = 120,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Simulates a two-sector wartime labor network (Priority Defense vs. Non-Priority
    Civilian) scaling from 1938 to 1944 civilian employment levels.

    Tracks:
    - Priority-sector staffing fill rate (stability of critical production nodes)
    - Excess turnover / poaching churn rate
    """
    rng = np.random.default_rng(seed)
    records = []

    # Target priority share ramps up across 36 wartime months
    target_priority_share = np.linspace(0.18, 0.42, n_steps)
    total_civ_series = np.linspace(civilian_emp_1938_m, civilian_emp_1944_m, n_steps)

    for shock in shock_levels:
        for friction in turnover_frictions:
            final_fill_rates = []
            avg_churn_rates = []

            for _ in range(n_MonteCarlo):
                # Start with initial 1938 allocation
                emp_total = total_civ_series[0]
                p_workers = emp_total * target_priority_share[0]
                np_workers = emp_total - p_workers

                churn_history = []

                for t in range(1, n_steps):
                    new_total = total_civ_series[t]
                    net_entrants = new_total - total_civ_series[t - 1]
                    target_p = new_total * target_priority_share[t]

                    # Controlled referral steers new/unassigned entrants toward priority plants
                    referral_routing = 0.45 + 0.45 * friction
                    routed_to_priority = net_entrants * referral_routing
                    routed_to_nonpriority = net_entrants - routed_to_priority

                    # Poaching / voluntary quit churn out of priority plants decreases
                    # as transfer-permission friction rises
                    base_quit_rate = 0.085 * (1.0 - 0.82 * friction)
                    # Exogenous civilian/health disruption shock (housing, bombing, morbidity)
                    shock_loss = shock * rng.uniform(0.6, 1.4) * (1.0 - 0.35 * friction)

                    quits_from_p = p_workers * base_quit_rate
                    disrupted_p = p_workers * shock_loss * 0.25

                    # Re-absorption from non-priority pool when priority is understaffed
                    gap = max(target_p - p_workers, 0.0)
                    reallocation = min(np_workers * (0.04 + 0.06 * friction), gap * 0.55)

                    p_workers = max(
                        p_workers + routed_to_priority + reallocation - quits_from_p - disrupted_p,
                        0.0,
                    )
                    np_workers = max(
                        new_total - p_workers,
                        0.0,
                    )

                    churn_history.append((quits_from_p + disrupted_p) / max(target_p, 1e-6))

                final_target_p = total_civ_series[-1] * target_priority_share[-1]
                fill_rate = min(p_workers / final_target_p, 1.05)
                final_fill_rates.append(fill_rate)
                avg_churn_rates.append(np.mean(churn_history))

            records.append(
                {
                    "shock_intensity": shock,
                    "turnover_friction": friction,
                    "mean_fill_rate": float(np.mean(final_fill_rates)),
                    "std_fill_rate": float(np.std(final_fill_rates)),
                    "mean_churn_rate": float(np.mean(avg_churn_rates)),
                }
            )

    return pd.DataFrame(records)


def make_figure(sim_df: pd.DataFrame, save_path: Path) -> None:
    """
    Generates a two-panel figure:
    Left: Priority-sector staffing stability vs. transfer-permission friction across shock regimes.
    Right: Turnover churn suppression curve across friction regimes.
    """
    plt.rcParams.update({
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 8.5,
        "figure.dpi": 300,
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

    shock_labels = {
        0.05: "Low Civilian/Health Shock (5%)",
        0.15: "Moderate Shock (15%)",
        0.28: "Severe Shock (28%)",
    }

    for shock, grp in sim_df.groupby("shock_intensity"):
        grp = grp.sort_values("turnover_friction")
        x = grp["turnover_friction"].to_numpy()
        y_fill = grp["mean_fill_rate"].to_numpy() * 100.0
        y_std = grp["std_fill_rate"].to_numpy() * 100.0
        y_churn = grp["mean_churn_rate"].to_numpy() * 100.0

        label = shock_labels.get(shock, f"Shock {shock:.0%}")
        ax1.plot(x, y_fill, marker="o", markersize=4, linewidth=1.8, label=label)
        ax1.fill_between(x, y_fill - y_std, y_fill + y_std, alpha=0.15)

        ax2.plot(x, y_churn, marker="s", markersize=4, linewidth=1.8, label=label)

    ax1.axvline(0.75, color="black", linestyle="--", linewidth=1.1, label="Buffalo Plan Referral Regime")
    ax1.set_title("A. Priority Sector Fill Rate vs. Mobility Friction")
    ax1.set_xlabel("Transfer & Referral Friction Parameter (0 = Free Churn, 1 = Strict Clearance)")
    ax1.set_ylabel("Priority Sector Staffing Fill Rate (%)")
    ax1.set_ylim(55, 105)
    ax1.grid(True, linestyle="--", alpha=0.35)
    ax1.legend(loc="lower right", frameon=True)

    ax2.axvline(0.75, color="black", linestyle="--", linewidth=1.1, label="Buffalo Plan Referral Regime")
    ax2.set_title("B. Monthly Priority-Labor Churn Under Shocks")
    ax2.set_xlabel("Transfer & Referral Friction Parameter")
    ax2.set_ylabel("Mean Monthly Disruption / Quit Churn (%)")
    ax2.grid(True, linestyle="--", alpha=0.35)
    ax2.legend(loc="upper right", frameon=True)

    fig.suptitle(
        "Command Under Collapse: Controlled Labor Routing & Shock Containment (44.14M → 53.96M Civilian Base)",
        fontsize=11.5,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight")
    plt.savefig(save_path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    output_png = project_root / "figures" / "02_labor_network_contagion.png"

    frictions = np.linspace(0.0, 0.95, 12)
    sim_df = simulate_labor_allocation(turnover_frictions=frictions)
    make_figure(sim_df, output_png)

    print("Saved PNG to:", output_png)
    print("Saved PDF to:", output_png.with_suffix(".pdf"))
    print("\nSample Simulation Summary (Selected Friction Points):")
    sample = sim_df[sim_df["turnover_friction"].isin([frictions[0], frictions[6], frictions[9], frictions[-1]])]
    print(sample.to_string(index=False))


if __name__ == "__main__":
    main()