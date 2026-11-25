"""
05_make_figures.py
Master build script that generates Figures 1–4 and prints summary tables for the paper.
"""

from importlib.machinery import SourceFileLoader

mod1 = SourceFileLoader("mod1", "01_bond_liquidity_regime.py").load_module()
mod2 = SourceFileLoader("mod2", "02_labor_routing_turnover.py").load_module()
mod3 = SourceFileLoader("mod3", "03_institutional_authority_network.py").load_module()


def main():
    print("Generating Figure 1...")
    mod1.run_macro_context(save_path="fig1_macro_overhang_context.png")

    print("Generating Figure 2...")
    mod2.plot_figure_2(save_path="fig2_labor_routing_friction.png")

    print("Generating Figure 3 & Figure 4...")
    res3 = mod3.simulate_compliance_panel(n_draws=600, n_agents=800, seed=909)
    mod3.plot_figure_3(res3, save_path="fig3_ordered_channel_gains.png")
    mod3.plot_figure_4(save_path="fig4_transmission_topology.png")

    print("All figures generated successfully.")


if __name__ == "__main__":
    main()
