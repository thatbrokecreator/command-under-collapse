# command-under-collapse

Companion simulation, sensitivity-analysis, and figure-generation scripts for:

**Mobility Friction, Compliance, and Wartime Staffing: Administrative Roles in World War II**  
*Tina Rabiei*

## Repository Structure

- `01_bond_liquidity_regime.py` — Generates **Figure 1** (*Hypothetical Overhang Curves and U.S. Monetary Context, 1939–1944*, Panels A–C) from deterministic overhang curves over $k = 0, \dots, 35$ alongside historical U.S. M1 and M1/nominal GNP series, 1939–1944 (Section 3.1; Appendix A.0).
- `02_labor_routing_turnover.py` — Generates **Figure 2** (*Priority Labor Routing: Baseline and Mismatch/Productivity Sensitivity*, `seed = 202`, 200 runs, Panel A twin-axis fill & cumulative quits and Panel B net-score gains across friction costs $c \in \{4, 8.5, 14\}$ with and without mismatch/productivity drag) and runs **Appendix A.1.1** sensitivity checks across penalty coefficient $\lambda \in \{0.11, 0.22, 0.33\}$ and exponent $\gamma \in \{1.0, 1.3, 1.6\}$ (Section 3.2; Appendix A.1).
- `03_institutional_authority_network.py` — Generates **Figure 3** (*Ordered Channel Gains Across Symmetric Specifications*, `seed = 909`, 600 draws, $N = 800$ agents, all six ordered permutations across four specifications, pairwise supermodularity, and the role-differentiated leave-one-out check) and **Figure 4** (*Authority, Operational Capacity & Transmission Topology Across Six Wartime Officials*) (Sections 2.3 & 3.3; Appendix A.2).
- `04_sensitivity_analysis.py` — Runs one-at-a-time parameter sensitivity checks (**Table 3**, using the v21 transfer-slope bounds `0.0385` and `0.0715`) plus Monte Carlo parameter sensitivity checks for the routing model (`seed = 404`, 120 sets) and compliance model (`seed = 505`, 30 sets) (Section 3.4; Appendix A.1.2 & A.3).
- `05_make_figures.py` — Master build script that generates Figures 1–4 (`fig1_macro_overhang_context.png`, `fig2_labor_routing_friction.png`, `fig3_ordered_channel_gains.png`, and `fig4_transmission_topology.png`).

## Requirements

- Python 3.9+
- `numpy`
- `matplotlib`

## Quickstart

Open a terminal inside the repository folder and run:

```bash
pip install numpy matplotlib
python 05_make_figures.py
python 04_sensitivity_analysis.py