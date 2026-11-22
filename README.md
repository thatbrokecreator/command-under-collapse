# Command Under Collapse: Women in Wartime Authority, Systemic Risk, and Market Stability During World War II

Computational econophysics and behavioral finance simulations supporting an interdisciplinary review article on how women in wartime executive, administrative, and policy roles shaped market stability, resource allocation, and systemic resilience during World War II (1939–1945).

## Repository Structure

```text
command-under-collapse/
├── README.md
├── scripts/
│   ├── 01_bond_liquidity_regime.py
│   ├── 02_labor_network_contagion.py
│   └── 03_institutional_authority_network.py
├── figures/
│   ├── 01_bond_liquidity_regime.png
│   ├── 01_bond_liquidity_regime.pdf
│   ├── 02_labor_network_contagion.png
│   ├── 02_labor_network_contagion.pdf
│   ├── 03_institutional_authority_network.png
│   └── 03_institutional_authority_network.pdf
└── manuscript/Simulation Modules, Figures & Explanations
1. Bond Absorption & Household Portfolio Reallocation (scripts/01_bond_liquidity_regime.py)
What the Figure Shows: Tracks U.S. Series E, F, and G savings-bond absorption (1941–1945) alongside regime shifts between steady payroll-like accumulation and war-loan campaign drives, plus household asset reallocation and retention dynamics.

Empirical & Theoretical Explanation: Calibrated to U.S. Treasury sales benchmarks ($2.54B in May–Dec 1941, $9.16B in 1942, $13.73B in 1943, $16.04B in 1944, and $12.94B in 1945), the model distinguishes steady baseline accumulation (47% Series E benchmark) from campaign-driven spikes (53%). Rather than treating bond purchases as net wealth destruction, it models them as household portfolio reallocation—converting liquid purchasing power into illiquid/non-marketable Treasury claims (85.2% June 1945 retention)—dampening near-term inflationary liquidity overhang while altering household balance-sheet composition.

2. Labor-Network Contagion & Mobility Friction (scripts/02_labor_network_contagion.py)
What the Figure Shows: Panel A plots priority-sector staffing fill rates against job-transfer/referral friction across low (5%), moderate (15%), and severe (28%) civilian/health shock intensities; Panel B plots mean monthly priority-labor churn across those same regimes.

Empirical & Theoretical Explanation: Anchored to the reconciled U.S. civilian employment trajectory (44.142M in 1938 to 53.960M in 1944, keeping armed forces personnel distinct from civilian labor supply), this constrained-flow model captures Anna M. Rosenberg's controlled-referral and transfer-permission architecture (the Buffalo Plan), interacting with Frances Perkins's labor-standards/wage-stabilization context and indirect civilian/health capacity shocks associated with Ellen Wilkinson and Florence Horsbrugh. Zero friction leaves priority plants vulnerable to poaching and quit churn; moderate-to-high referral friction (~0.75 regime) dampens churn and stabilizes bottleneck staffing even under severe exogenous shocks.

3. Heterogeneous Institutional Authority & Compliance Contagion (scripts/03_institutional_authority_network.py)
What the Figure Shows: Panel A maps six officials across distinct institutional tiers and intermediate market/behavioral/macro channels toward systemic market stability; Panel B simulates aggregate household/market compliance over 40 months following an inflationary supply shock at t = 6 across four institutional regimes.

Empirical & Theoretical Explanation: Avoids treating wartime officials as having uniform market-clearing authority by separating:

Direct allocation / mobility control: Anna M. Rosenberg (WMC Region II / Buffalo Plan),

Senior labor-policy & administrative throughput: Frances Perkins (U.S. Department of Labor; over 100,000 rulings/determinations and roughly 900,000 inquiries—measuring administrative load rather than assuming automatic compliance),

Compliance & consumer expectations: Harriet Wiseman Elliott (OPACS Consumer Division, 1941),

International & postwar monetary planning: Eleanor Lansing Dulles (State Department, Bretton Woods, Vienna), and

Indirect civilian defense & health buffers: Ellen Wilkinson (UK Ministry of Home Security) and Florence Horsbrugh (UK Ministry of Health).

In Panel B, voluntary messaging alone raises compliance above the unregulated baseline but hits a ceiling under persistent scarcity shocks, whereas combining administrative enforcement and structural allocation locks sustains much higher market stability.