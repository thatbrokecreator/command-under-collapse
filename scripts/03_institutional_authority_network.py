"""
03_institutional_authority_network.py

Econophysics / multilayer complex-network simulation modeling heterogeneous
institutional authority and compliance contagion across six verified WWII
officials (US & UK).

Key methodological choices:
1. Heterogeneous authority taxonomy (avoiding equal-node bias):
   - Direct Allocation / Mobility Control: Anna M. Rosenberg (WMC Region II / Buffalo Plan)
   - Senior Labor-Policy & Admin Throughput: Frances Perkins (U.S. Dept. of Labor; >100k rulings, ~900k inquiries)
   - Compliance & Consumer Expectations: Harriet Wiseman Elliott (OPACS Consumer Division, 1941)
   - International Planning & Postwar Monetary Order: Eleanor Lansing Dulles (State Dept., Bretton Woods, Vienna)
   - Indirect Civil Defense & Mobility Shock Buffer: Ellen Wilkinson (UK Ministry of Home Security)
   - Indirect Health & Labor-Capacity Buffer: Florence Horsbrugh (UK Ministry of Health, 1939-45)
2. Workload vs. compliance separation: Distinguishes administrative throughput
   (caseload processing) from realized market/household compliance rates.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def build_institutional_graph() -> nx.DiGraph:
    """
    Constructs a directed, weighted institutional influence graph separating
    officials by functional tier and downstream market/system channels.
    """
    G = nx.DiGraph()

    officials = [
        ("Rosenberg\n(WMC Region II)", {"tier": "Direct Allocation", "weight": 0.92, "x": 0.0, "y": 2.5}),
        ("Perkins\n(Dept. of Labor)", {"tier": "Admin & Policy", "weight": 0.78, "x": 0.0, "y": 1.5}),
        ("Elliott\n(OPACS Consumer)", {"tier": "Compliance / Info", "weight": 0.55, "x": 0.0, "y": 0.5}),
        ("Dulles\n(State / Bretton Woods)", {"tier": "Intl / Postwar", "weight": 0.65, "x": 0.0, "y": -0.5}),
        ("Wilkinson\n(UK Home Security)", {"tier": "Indirect Civilian", "weight": 0.48, "x": 0.0, "y": -1.5}),
        ("Horsbrugh\n(UK Health)", {"tier": "Indirect Welfare", "weight": 0.45, "x": 0.0, "y": -2.5}),
    ]

    channels = [
        ("Priority Labor\nAllocation", {"tier": "Market Channel", "weight": 0.85, "x": 1.35, "y": 2.0}),
        ("Wage & Admin\nThroughput", {"tier": "Market Channel", "weight": 0.80, "x": 1.35, "y": 1.0}),
        ("Household Compliance\n& Expectations", {"tier": "Behavioral Channel", "weight": 0.70, "x": 1.35, "y": 0.0}),
        ("Postwar Monetary &\nFX Stability", {"tier": "Macro Channel", "weight": 0.75, "x": 1.35, "y": -1.0}),
        ("Civilian Workforce\nAvailability", {"tier": "Capacity Channel", "weight": 0.68, "x": 1.35, "y": -2.0}),
    ]

    outcome = [
        ("Systemic Market\nStability", {"tier": "System Outcome", "weight": 1.0, "x": 2.65, "y": 0.0}),
    ]

    for node, attrs in officials + channels + outcome:
        G.add_node(node, **attrs)

    edges = [
        # Officials -> Intermediate Channels
        ("Rosenberg\n(WMC Region II)", "Priority Labor\nAllocation", 0.92),
        ("Perkins\n(Dept. of Labor)", "Wage & Admin\nThroughput", 0.80),
        ("Perkins\n(Dept. of Labor)", "Priority Labor\nAllocation", 0.42),
        ("Elliott\n(OPACS Consumer)", "Household Compliance\n& Expectations", 0.62),
        ("Dulles\n(State / Bretton Woods)", "Postwar Monetary &\nFX Stability", 0.72),
        ("Wilkinson\n(UK Home Security)", "Civilian Workforce\nAvailability", 0.52),
        ("Horsbrugh\n(UK Health)", "Civilian Workforce\nAvailability", 0.50),
        # Channels -> Systemic Market Stability
        ("Priority Labor\nAllocation", "Systemic Market\nStability", 0.90),
        ("Wage & Admin\nThroughput", "Systemic Market\nStability", 0.82),
        ("Household Compliance\n& Expectations", "Systemic Market\nStability", 0.68),
        ("Postwar Monetary &\nFX Stability", "Systemic Market\nStability", 0.74),
        ("Civilian Workforce\nAvailability", "Systemic Market\nStability", 0.60),
    ]

    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    return G


def simulate_compliance_regimes(
    n_agents: int = 800,
    n_steps: int = 40,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Simulates behavioral compliance / anti-hoarding contagion across 800 household
    and firm agents hit by an exogenous inflationary supply shock at t = 6.

    Compares four institutional configurations:
    1. Unregulated / No Intervention
    2. Informational / Voluntary Messaging Only (Elliott 1941 model)
    3. Messaging + Administrative Throughput (Elliott + Perkins support)
    4. Multi-Tier Institutional Architecture (Direct allocation + Admin + Messaging + Civilian buffer)
    """
    rng = np.random.default_rng(seed)

    regimes = {
        "1. Unregulated Shock Baseline": {"info_pull": 0.02, "admin_enforce": 0.00, "structural_lock": 0.00},
        "2. Voluntary Messaging Only (Elliott '41)": {"info_pull": 0.14, "admin_enforce": 0.04, "structural_lock": 0.02},
        "3. Messaging + Admin Throughput (Perkins)": {"info_pull": 0.16, "admin_enforce": 0.22, "structural_lock": 0.08},
        "4. Full Multi-Tier Architecture": {"info_pull": 0.20, "admin_enforce": 0.30, "structural_lock": 0.28},
    }

    records = []

    for regime_name, params in regimes.items():
        # Agent state: 1.0 = full compliance / stable expectations, 0.0 = panic hoarding / black-market defection
        compliance = np.clip(rng.normal(loc=0.88, scale=0.06, size=n_agents), 0.5, 1.0)

        for t in range(n_steps):
            # Exogenous wartime scarcity/price shock hits at t=6 and persists with decaying turbulence
            if t < 6:
                shock = 0.01
            else:
                shock = 0.16 * np.exp(-0.03 * (t - 6)) + 0.04

            # Peer contagion: agents observe average neighborhood compliance
            mean_c = float(np.mean(compliance))
            peer_pressure = 0.12 * (mean_c - compliance)

            # Institutional pull: separates soft persuasion from structural allocation locks
            persuasion = params["info_pull"] * (0.85 - compliance)
            enforcement = params["admin_enforce"] * (0.92 - compliance)
            structural = params["structural_lock"] * (0.96 - compliance)

            noise = rng.normal(0.0, 0.025, size=n_agents)
            compliance = np.clip(
                compliance - shock + peer_pressure + persuasion + enforcement + structural + noise,
                0.0,
                1.0,
            )

            records.append(
                {
                    "regime": regime_name,
                    "step": t,
                    "mean_compliance": float(np.mean(compliance)),
                    "std_compliance": float(np.std(compliance)),
                }
            )

    return pd.DataFrame(records)


def make_figure(G: nx.DiGraph, sim_df: pd.DataFrame, save_path: Path) -> None:
    """
    Generates a two-panel figure:
    Left: Heterogeneous institutional authority & channel network.
    Right: Dynamic compliance & anti-hoarding stability across institutional tiers.
    """
    plt.rcParams.update({
        "font.size": 9.5,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 8.0,
        "figure.dpi": 300,
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.4), gridspec_kw={"width_ratios": [1.15, 1.0]})

    # Panel A: Directed Heterogeneous Network
    pos = {n: (d["x"], d["y"]) for n, d in G.nodes(data=True)}
    node_colors = []
    node_sizes = []
    for _, d in G.nodes(data=True):
        tier = d["tier"]
        if tier == "Direct Allocation":
            node_colors.append("#1f77b4")
        elif tier in ("Admin & Policy", "Intl / Postwar"):
            node_colors.append("#2ca02c")
        elif tier == "Compliance / Info":
            node_colors.append("#ff7f0e")
        elif tier in ("Indirect Civilian", "Indirect Welfare"):
            node_colors.append("#9467bd")
        elif tier == "System Outcome":
            node_colors.append("#d62728")
        else:
            node_colors.append("#7f7f7f")
        node_sizes.append(650 + 650 * d["weight"])

    edge_widths = [1.0 + 2.8 * d["weight"] for _, _, d in G.edges(data=True)]

    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax1,
        width=edge_widths,
        alpha=0.55,
        edge_color="#4a4a4a",
        arrows=True,
        arrowsize=13,
        connectionstyle="arc3,rad=0.04",
    )
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax1,
        node_color=node_colors,
        node_size=node_sizes,
        alpha=0.92,
        edgecolors="black",
        linewidths=1.0,
    )
    nx.draw_networkx_labels(G, pos, ax=ax1, font_size=7.6, font_weight="bold")

    ax1.set_title("A. Heterogeneous Authority & Transmission Topology")
    ax1.set_xlim(-0.55, 3.15)
    ax1.set_ylim(-3.1, 3.1)
    ax1.axis("off")

    # Panel B: Compliance Contagion Trajectories
    for regime_name, grp in sim_df.groupby("regime"):
        grp = grp.sort_values("step")
        x = grp["step"].to_numpy()
        y = grp["mean_compliance"].to_numpy() * 100.0
        ax2.plot(x, y, linewidth=2.0, label=regime_name)

    ax2.axvline(6, color="black", linestyle="--", linewidth=1.1, label="Exogenous Supply/Price Shock (t = 6)")
    ax2.set_title("B. Market Compliance Contagion by Authority Tier")
    ax2.set_xlabel("Simulation Time Step (Months)")
    ax2.set_ylabel("Aggregate Market / Household Compliance (%)")
    ax2.set_ylim(10, 100)
    ax2.grid(True, linestyle="--", alpha=0.35)
    ax2.legend(loc="lower right", frameon=True)

    fig.suptitle(
        "Command Under Collapse: Multi-Tier Institutional Authority & Compliance Dynamics",
        fontsize=12,
        fontweight="bold",
        y=1.01,
    )
    plt.tight_layout()

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight")
    plt.savefig(save_path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    output_png = project_root / "figures" / "03_institutional_authority_network.png"

    G = build_institutional_graph()
    sim_df = simulate_compliance_regimes()
    make_figure(G, sim_df, output_png)

    print("Saved PNG to:", output_png)
    print("Saved PDF to:", output_png.with_suffix(".pdf"))
    print("\nTerminal Compliance Summary (at final step t = 39):")
    final_summary = sim_df[sim_df["step"] == sim_df["step"].max()][["regime", "mean_compliance", "std_compliance"]]
    print(final_summary.to_string(index=False))


if __name__ == "__main__":
    main()
    