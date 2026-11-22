"""
01_bond_liquidity_regime.py

Econophysics / behavioral portfolio model for U.S. WWII savings-bond
absorption (Series E, F, and G, 1941-1945), calibrated to corrected
historical benchmarks while explicitly modeling asset reallocation rather
than simple money-supply destruction.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_empirical_series() -> pd.DataFrame:
    """
    Reconciled U.S. Series E, F, and G savings-bond sales (in $ billions)
    for 1941-1945, using corrected 1943 ($13.729B) and 1945 ($12.937B) figures.
    """
    records = [
        {"period": "1941 (May-Dec)", "year_num": 1941.33, "sales_b": 2.537210},
        {"period": "1942", "year_num": 1942.00, "sales_b": 9.156957},
        {"period": "1943", "year_num": 1943.00, "sales_b": 13.729000},
        {"period": "1944", "year_num": 1944.00, "sales_b": 16.044085},
        {"period": "1945", "year_num": 1945.00, "sales_b": 12.937000},
    ]
    return pd.DataFrame(records)


def simulate_bond_channels(
    df: pd.DataFrame,
    payroll_share: float = 0.47,
    drive_pulse_strength: float = 0.22,
    retention_rate_1945: float = 0.852,
    n_households: int = 2000,
    seed: int = 42,
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Simulates channel decomposition (steady payroll vs. pulsed drives) and
    household portfolio reallocation (liquid cash vs. bond claims).
    """
    rng = np.random.default_rng(seed)

    steady_component = df["sales_b"].to_numpy() * payroll_share
    drive_component = df["sales_b"].to_numpy() * (1.0 - payroll_share)

    wave_factors = np.array([0.85, 0.95, 1.05, 1.15, 0.90])
    modulated_drive = drive_component * (1.0 + drive_pulse_strength * (wave_factors - 1.0))
    reconciled_total = steady_component + modulated_drive
    scale = df["sales_b"].sum() / reconciled_total.sum()
    steady_component *= scale
    modulated_drive *= scale

    out = df.copy()
    out["payroll_channel_b"] = steady_component
    out["drive_channel_b"] = modulated_drive
    out["net_retained_1945_equiv_b"] = out["sales_b"] * retention_rate_1945

    initial_liquid = rng.lognormal(mean=0.0, sigma=0.45, size=n_households)
    propensity = np.clip(rng.normal(loc=0.42, scale=0.14, size=n_households), 0.05, 0.85)
    retained_fraction = np.clip(
        rng.normal(loc=retention_rate_1945, scale=0.06, size=n_households), 0.50, 0.99
    )

    bond_claims = initial_liquid * propensity * retained_fraction
    remaining_liquid = np.maximum(initial_liquid - bond_claims, 0.0)
    total_household_assets = remaining_liquid + bond_claims

    summary_arrays = np.vstack([initial_liquid, remaining_liquid, bond_claims, total_household_assets])
    return out, summary_arrays


def make_figure(sim_df: pd.DataFrame, agent_matrix: np.ndarray, save_path: Path) -> None:
    """
    Generates a two-panel publication-style chart and saves both PNG and PDF.
    """
    plt.rcParams.update({
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 8.5,
        "figure.dpi": 300,
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

    x = np.arange(len(sim_df))
    payroll_vals = sim_df["payroll_channel_b"].to_numpy()
    drive_vals = sim_df["drive_channel_b"].to_numpy()
    emp_totals = sim_df["sales_b"].to_numpy()

    ax1.bar(x, payroll_vals, width=0.55, label="Steady / Payroll-like Channel (47% E-bond benchmark)")
    ax1.bar(
        x,
        drive_vals,
        width=0.55,
        bottom=payroll_vals,
        label="Drive / Campaign Channel (53% E-bond benchmark)",
    )
    ax1.plot(x, emp_totals, color="black", marker="o", linewidth=1.5, label="Empirical E/F/G Sales ($B)")

    ax1.set_title("A. U.S. Savings-Bond Sales & Channel Split (1941–1945)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(sim_df["period"], rotation=20, ha="right")
    ax1.set_ylabel("Billions of USD ($B)")
    ax1.set_ylim(0, max(emp_totals) * 1.22)
    ax1.grid(axis="y", linestyle="--", alpha=0.35)
    ax1.legend(loc="upper left", frameon=True)

    labels = ["Initial Liquid", "Post-Shift Liquid", "Bond Claims", "Total Assets"]
    means = [agent_matrix[i].mean() for i in range(4)]
    q25 = [np.percentile(agent_matrix[i], 25) for i in range(4)]
    q75 = [np.percentile(agent_matrix[i], 75) for i in range(4)]

    yerr_low = np.maximum(np.array(means) - np.array(q25), 0.0)
    yerr_high = np.maximum(np.array(q75) - np.array(means), 0.0)

    bx = np.arange(len(labels))
    ax2.bar(bx, means, width=0.52)
    ax2.errorbar(
        bx,
        means,
        yerr=[yerr_low, yerr_high],
        fmt="none",
        ecolor="black",
        elinewidth=1.2,
        capsize=4,
    )

    ax2.set_title("B. Household Asset Reallocation (Mean & IQR)")
    ax2.set_xticks(bx)
    ax2.set_xticklabels(labels, rotation=15, ha="right")
    ax2.set_ylabel("Normalized Household Units")
    ax2.grid(axis="y", linestyle="--", alpha=0.35)

    fig.suptitle(
        "Command Under Collapse: Bond Absorption & Portfolio Reallocation Dynamics",
        fontsize=12.5,
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
    output_png = project_root / "figures" / "01_bond_liquidity_regime.png"

    emp_df = get_empirical_series()
    sim_df, agent_matrix = simulate_bond_channels(emp_df)
    make_figure(sim_df, agent_matrix, output_png)

    print("Saved PNG to:", output_png)
    print("Saved PDF to:", output_png.with_suffix(".pdf"))
    print("\nReconciled Table:")
    print(sim_df.to_string(index=False))


if __name__ == "__main__":
    main()