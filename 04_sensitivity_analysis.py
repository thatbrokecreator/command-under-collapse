"""
04_sensitivity_analysis.py
Runs Table 3 one-at-a-time sensitivity checks (using exact 0.0385 and 0.0715 bounds from v21)
plus Appendix A.3 random Monte Carlo checks for routing (seed = 404) and compliance (seed = 505).
"""

import importlib.util
from pathlib import Path
import numpy as np


def _load_module(name, filename):
    path = Path(__file__).resolve().parent / filename
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


routing_mod = _load_module("routing_mod", "02_labor_routing_turnover.py")
comp_mod = _load_module("comp_mod", "03_institutional_authority_network.py")


def run_routing_oat_v21():
    print("=== Table 3 (v21): One-at-a-Time Sensitivity ===")
    cases = [
        ("Routing slope (0.48)", "routing_slope", 0.336, 0.624),
        ("Transfer slope (0.055)", "transfer_slope", 0.0385, 0.0715),
        ("Quit-reduction slope (0.52)", "quit_red_slope", 0.364, 0.676),
        ("Routing-efficiency loss (0.28)", "eff_loss_coeff", 0.196, 0.364),
        ("Ex-post drag coefficient (0.22)", "drag_coeff", 0.11, 0.33),
        ("Ex-post drag exponent (1.3)", "drag_exp", 1.0, 1.6),
    ]

    for label, key, low_v, high_v in cases:
        out = []
        for val in (low_v, high_v):
            f_grid, _, eff_fill, _ = routing_mod.simulate_routing(n_runs=200, seed=202, **{key: val})
            net = eff_fill - 8.5 * (f_grid ** 1.5)
            out.append(f"{val} -> f*={f_grid[np.argmax(net)]:.2f}, +{np.max(net)-net[0]:.2f}")
        print(f"{label:32s} | {out[0]:25s} | {out[1]}")

    for c_val in (4.0, 14.0):
        f_grid, _, eff_fill, _ = routing_mod.simulate_routing(n_runs=200, seed=202)
        net = eff_fill - c_val * (f_grid ** 1.5)
        print(f"Friction cost c={c_val:4.1f}             | f*={f_grid[np.argmax(net)]:.2f}, +{np.max(net)-net[0]:.2f}")

    for sh_val in (0.05, 0.28):
        f_grid, _, eff_fill, _ = routing_mod.simulate_routing(n_runs=200, seed=202, sh=sh_val)
        net = eff_fill - 8.5 * (f_grid ** 1.5)
        print(f"Disruption sh={sh_val:4.2f}            | f*={f_grid[np.argmax(net)]:.2f}, +{np.max(net)-net[0]:.2f}")


def run_routing_random(n_sets=120, seed=404):
    rng = np.random.default_rng(seed)
    sh_choices = [0.05, 0.15, 0.28]
    f_stars_drag, gains_drag, f_stars_base = [], [], []

    for i in range(n_sets):
        r_s = 0.48 * rng.uniform(0.7, 1.3)
        t_s = 0.055 * rng.uniform(0.7, 1.3)
        q_s = 0.52 * rng.uniform(0.7, 1.3)
        e_c = 0.28 * rng.uniform(0.7, 1.3)
        d_c = 0.22 * rng.uniform(0.5, 1.5)
        d_e = rng.uniform(1.0, 1.6)
        c_v = rng.uniform(4.0, 14.0)
        sh_v = sh_choices[int(rng.integers(0, 3))]

        f_grid, gross_fill, eff_fill, _ = routing_mod.simulate_routing(
            n_runs=40,
            seed=202 + i,
            sh=sh_v,
            routing_slope=r_s,
            transfer_slope=t_s,
            quit_red_slope=q_s,
            eff_loss_coeff=e_c,
            drag_coeff=d_c,
            drag_exp=d_e,
        )
        net_drag = eff_fill - c_v * (f_grid ** 1.5)
        net_base = gross_fill - c_v * (f_grid ** 1.5)
        f_stars_drag.append(f_grid[np.argmax(net_drag)])
        gains_drag.append(np.max(net_drag) - net_drag[0])
        f_stars_base.append(f_grid[np.argmax(net_base)])

    f_stars_drag = np.array(f_stars_drag)
    gains_drag = np.array(gains_drag)
    f_stars_base = np.array(f_stars_base)

    print("\n=== Random Routing Sensitivity (120 sets, seed = 404) ===")
    print(
        f"With drag: median f*={np.median(f_stars_drag):.2f}, "
        f"5th-95th=({np.percentile(f_stars_drag, 5):.2f}, {np.percentile(f_stars_drag, 95):.2f}), "
        f"interior={np.mean(f_stars_drag < 0.95)*100:.0f}%, "
        f"median gain=+{np.median(gains_drag):.1f}"
    )
    print(
        f"No drag:   median f*={np.median(f_stars_base):.2f}, "
        f"5th-95th=({np.percentile(f_stars_base, 5):.2f}, {np.percentile(f_stars_base, 95):.2f}), "
        f"interior={np.mean(f_stars_base < 0.95)*100:.0f}%"
    )


def run_compliance_random(n_sets=30, seed=505):
    rng = np.random.default_rng(seed)
    sat_ok = ovl_ok = add_ok = syn_ok = order_ok = role_order_ok = 0

    for i in range(n_sets):
        ch_s = 0.018 * rng.uniform(0.7, 1.3)
        syn_c = rng.uniform(0.10, 0.40)
        ovl_c = rng.uniform(0.25, 1.00)
        sh_s = 0.08 * rng.uniform(0.75, 1.25)

        res = comp_mod.simulate_compliance_panel(
            n_draws=40,
            n_agents=800,
            seed=909 + i,
            ch_strength=ch_s,
            synergy_const=syn_c,
            overlap_const=ovl_c,
            shock_scale=sh_s,
        )

        g_add = np.mean(res["step_gains"]["Additive Linear"], axis=0)
        g_sat = np.mean(res["step_gains"]["Saturating (ceiling)"], axis=0)
        g_syn = np.mean(res["step_gains"]["Supermodular Synergy"], axis=0)
        g_ovl = np.mean(res["step_gains"]["Substitutive Overlap"], axis=0)

        if np.max(g_add) - np.min(g_add) < 0.5:
            add_ok += 1
        if g_sat[0] > g_sat[1] > g_sat[2]:
            sat_ok += 1
        if g_ovl[0] > g_ovl[1] > g_ovl[2] > 0:
            ovl_ok += 1
        if g_syn[0] < g_syn[1] < g_syn[2]:
            syn_ok += 1

        yf = {k: np.mean(v) for k, v in res["y_full"].items()}
        if (
            yf["Supermodular Synergy"]
            > yf["Additive Linear"]
            > yf["Saturating (ceiling)"]
            > yf["Substitutive Overlap"]
        ):
            order_ok += 1

        drops = np.mean(res["role_drops"], axis=0)
        if drops[2] > drops[0] > drops[1]:
            role_order_ok += 1

    print("\n=== Random Compliance Sensitivity (30 sets, seed = 505) ===")
    print(f"Saturating declining: {sat_ok}/{n_sets}")
    print(f"Overlap declining & positive: {ovl_ok}/{n_sets}")
    print(f"Additive constant (<0.5 pp spread): {add_ok}/{n_sets}")
    print(f"Synergy rising: {syn_ok}/{n_sets}")
    print(f"Full-regime ordering (Syn > Add > Sat > Sub): {order_ok}/{n_sets}")
    print(f"Role ordering (Ch 3 > Ch 1 > Ch 2): {role_order_ok}/{n_sets}")


if __name__ == "__main__":
    run_routing_oat_v21()
    run_routing_random()
    run_compliance_random()