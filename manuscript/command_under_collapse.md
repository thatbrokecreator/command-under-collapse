# Command Under Collapse: Women in Wartime Authority, Systemic Risk, and Market Stability During World War II

**Keywords:** Econophysics; Behavioral Economics; Neurofinance; Wartime Stabilization; Institutional Authority; Labor Networks; Portfolio Reallocation; World War II

## Abstract

World War II (1939–1945) subjected Allied economies to simultaneous structural shocks: surge fiscal mobilization, physical scarcity in consumer markets, acute labor-bottleneck pressures, and severe household uncertainty. While traditional macroeconomic accounts emphasize aggregate fiscal multipliers or central planning, they often treat institutional governance as a uniform black box or overlook key administrative and operational mechanisms through which wartime stability was maintained. This review article develops an interdisciplinary framework bridging **econophysics** (constrained-flow networks, regime-switching dynamics, and contagion modeling) and **behavioral/neuroeconomic reasoning** (scarcity-induced liquidity preferences, expectation anchoring, and compliance thresholds) to examine how six women exercising executive, administrative, and policy authority—**Anna M. Rosenberg**, **Frances Perkins**, **Harriet Wiseman Elliott**, **Eleanor Lansing Dulles**, **Ellen Wilkinson**, and **Florence Horsbrugh**—interacted with wartime market stability and systemic risk. Rather than assuming equal market-setting power across officials, we classify their roles across distinct institutional tiers—direct allocation and mobility friction, administrative throughput, consumer compliance and expectation framing, international monetary architecture, and indirect civilian/health capacity buffers—and synthesize these mechanisms with empirical anchors from U.S. Treasury savings-bond sales (1941–1945), reconciled U.S. civilian employment records (1938–1944), and administrative caseload evidence.

---

## 1. Introduction: Wartime Mobilization as a Constrained Complex System

A wartime economy is not simply a larger version of a peacetime economy; it is a **constrained complex system** operating near structural boundaries. When defense production expands rapidly while civilian goods production is curtailed or diverted, excess purchasing power collides with physical supply ceilings. Left unbuffered, this imbalance manifests across multiple coupled channels: inflationary price pressure and black-market leakage, panic hoarding by households under scarcity uncertainty, destructive labor poaching and turnover contagion in bottleneck defense plants, and workforce attrition driven by civil-defense or public-health disruptions.

Conventional historical and macroeconomic narratives frequently analyze these dynamics through broad aggregates—gross national output, total war expenditure, or centralized directive decrees—while under-examining the **micro-institutional and behavioral friction points** where policy meets real human decision-making. Yet wartime stability depended heavily on whether institutions could:
1. absorb excess short-term household liquidity without destroying household balance-sheet confidence,
2. route scarce labor toward critical production nodes while curbing destabilizing turnover cascades, and
3. sustain compliance and workforce continuity under persistent physical and informational shocks.

During World War II, women in the United States and the United Kingdom occupied pivotal positions across several of these governance layers. Examining their contributions through an econophysics and behavioral/neurofinance lens allows us to ask a precise analytical question: **Through what distinct institutional mechanisms—and under what structural constraints—did women in wartime authority dampen contagion and preserve market stability under extreme resource scarcity?**

To answer this question rigorously, this review pairs historical verification with three computational simulation modules (`01_bond_liquidity_regime.py`, `02_labor_network_contagion.py`, and `03_institutional_authority_network.py`) archived in this repository. Each model is designed not as a claim of exact historical omnipotence, but as a structured testbed for evaluating how institutional rules and behavioral responses interact under stress.

---

## 2. Theoretical Framework: Econophysics, Scarcity Adaptation, and Institutional Authority Tiers

### 2.1 Scarcity, Liquidity Overhang, and Portfolio Reallocation

In econophysics and behavioral finance, periods of acute supply constraint alter both **resource flows** and **agent decision rules**. Under scarcity and heightened uncertainty, households face a tension between holding liquid purchasing power for immediate defensive consumption (or precautionary cash buffers) and shifting wealth into longer-horizon, less liquid instruments. Treating wartime bond absorption merely as an accounting subtraction from consumption misses its balance-sheet character: savings-bond subscriptions represent **portfolio reallocation** from liquid cash/deposits into non-marketable government claims that lock up near-term inflationary liquidity while preserving household wealth claims over time.

From a neuroeconomic and behavioral perspective, scarcity conditions heighten sensitivity to perceived loss, future uncertainty, and social signaling. Institutional instruments that combine **habitual/payroll continuity** with **episodic mobilization campaigns** can shift how households allocate marginal income—provided institutional credibility and redemption expectations remain anchored.

### 2.2 Constrained-Flow Networks and Labor Mobility Friction

In a high-mobilization labor market, workers and firms form a **constrained flow network** subject to skill specificity, geographic friction, and bottleneck dependencies. When competing employers poach scarce skilled labor in the absence of coordination rules, high turnover acts like **contagion or friction loss** in a transport network: production lines experience repeated disruption, training overhead rises, and bottleneck output falls below capacity even when aggregate employment is expanding.

Introducing **controlled-referral and transfer-permission rules**—exemplified in U.S. labor administration by **Anna M. Rosenberg** in War Manpower Commission Region II and the **Buffalo Plan**—operates as a structural friction/routing mechanism on worker mobility. Rather than viewing all friction as market inefficiency, a constrained-flow perspective asks when regulated transfer friction *reduces* destructive churn and improves bottleneck staffing under severe external shocks.

### 2.3 A Heterogeneous Taxonomy of Institutional Authority

A central methodological pitfall in comparative institutional analysis is treating diverse offices as interchangeable nodes with identical causal leverage over prices, output, or compliance. To avoid overstating or misattributing impact, we distinguish **five tiers of institutional authority** across our six focal figures:

| Authority Tier | Representative Figure(s) | Primary Mechanism | Analytical Caveat |
| :--- | :--- | :--- | :--- |
| **1. Direct Allocation & Mobility Control** | **Anna M. Rosenberg** (WMC Region II / Buffalo Plan) | Controlled job referrals, transfer clearances, and localized manpower routing in priority defense areas | Localized/regional scope and operational friction require careful scaling claims |
| **2. Senior Labor-Policy & Admin Throughput** | **Frances Perkins** (U.S. Dept. of Labor) | Institutional labor-standards governance, wage-stabilization administration, and high-volume case/inquiry processing | High administrative caseload/rulings measure institutional workload, not automatic market compliance |
| **3. Compliance & Expectation Framing** | **Harriet Wiseman Elliott** (OPACS Consumer Division, 1941) | Consumer information, anti-hoarding norms, and voluntary expectation management | Voluntary persuasion faces limits without binding rationing or price enforcement |
| **4. International & Postwar Monetary Order** | **Eleanor Lansing Dulles** (State Dept., Bretton Woods, Vienna) | Cross-border monetary coordination, financial reconstruction, and institutional stabilization | Macro/international effects operate over longer horizons and multi-actor negotiations |
| **5. Indirect Civilian & Health Buffers** | **Ellen Wilkinson** (UK Home Security); **Florence Horsbrugh** (UK Health) | Civil defense, shelter/disruption management, and public-health/morbidity protection | Affects market stability indirectly by preserving civilian safety and workforce capacity |

This taxonomy clarifies why different interventions exhibit different dynamics: persuasion shapes expectations and norms, administrative throughput processes disputes and rules, direct routing alters physical/labor flows, and civilian/health buffers protect the underlying human capacity on which all economic activity depends.
---

## 3. Empirical Anchors and Computational Synthesis

To ground the theoretical taxonomy in verified historical data, each computational module in this study calibrates its parameters to documented wartime records while embedding relative image paths (`../figures/...`) directly into the manuscript structure.

### 3.1 Household Liquidity Absorption and Portfolio Reallocation (1941–1945)

Between May 1941 and the end of 1945, U.S. Treasury Series E, F, and G savings-bond sales absorbed substantial household liquidity across distinct mobilization phases: **$2.54 billion** in May–December 1941, **$9.16 billion** in 1942, **$13.73 billion** in 1943, **$16.04 billion** in 1944, and **$12.94 billion** in 1945 (U.S. Treasury historical savings-bond series). Crucially, institutional distribution relied on two complementary behavioral channels: routine payroll-deduction subscriptions (accounting for approximately **47%** of Series E benchmark volume) and episodic war-loan drives (accounting for approximately **53%**).

![Bond Absorption and Household Portfolio Reallocation](../figures/01_bond_liquidity_regime.png)

As illustrated in **Figure 1** (`scripts/01_bond_liquidity_regime.py`), modeling these inflows as a regime-switching allocation process highlights two critical mechanisms:
1. **Liquidity Lock-Up Without Balance-Sheet Destruction:** Unlike outright taxation, savings-bond purchases reallocated household portfolios from immediately spendable cash into non-marketable claims, curbing near-term inflationary demand pressure in constrained consumer markets while preserving household asset holdings.
2. **Sustained Retention Under Scarcity:** Cumulative Series E–G retention stood at **85.2%** as of June 1945, demonstrating that institutional framing and payroll continuity prevented rapid redemption cascades even as war-weariness and supply constraints persisted.

---

### 3.2 Labor-Network Contagion and Controlled-Referral Friction (1938–1944)

Evaluating wartime labor governance requires strict statistical discipline: total wartime employment figures that combine armed forces personnel with civilian workers (`65.370 million` total employed in 1944) overstate civilian industrial labor supply if used unadjusted. Calibrating strictly to the **reconciled U.S. civilian employment trajectory**—which expanded from **44.142 million** in 1938 to **53.960 million** in 1944—isolates the actual civilian workforce available to absorb industrial mobilization.

Within that civilian labor pool, rapid expansion of priority defense manufacturing created acute poaching incentives: firms facing tight delivery schedules bid away skilled workers from neighboring plants, generating turnover churn that degraded bottleneck output. Under **Anna M. Rosenberg's** regional leadership in War Manpower Commission Region II and the **Buffalo Plan**, controlled-referral and transfer-clearance rules introduced targeted administrative friction on uncoordinated job switching while routing unassigned entrants toward high-priority facilities. Simultaneously, **Frances Perkins's** Department of Labor maintained the institutional wage-stabilization and labor-standards framework, while British counterparts **Ellen Wilkinson** (Ministry of Home Security) and **Florence Horsbrugh** (Ministry of Health) managed civil-defense shelter and public-health continuity under direct aerial and morbidity shocks.

![Labor Network Contagion and Mobility Friction](../figures/02_labor_network_contagion.png)

**Figure 2** (`scripts/02_labor_network_contagion.py`) simulates this constrained two-sector labor network across varying transfer-friction regimes and exogenous civilian/health shock intensities (`5%`, `15%`, and `28%`):
* **Unconstrained Churn Regime (`friction ≈ 0`):** High quit and poaching rates prevent priority defense nodes from reaching target staffing fill rates, and severe civilian or public-health shocks trigger sharp output-capacity drops.
* **Controlled-Referral Regime (`friction ≈ 0.75`):** Regulated transfer permissions suppress monthly priority-labor churn and stabilize bottleneck fill rates even under severe exogenous disruption, illustrating how targeted institutional friction can act as a network stabilizer rather than a deadweight loss.

---

### 3.3 Heterogeneous Authority Tiers and Market Compliance Contagion

A key analytical risk in institutional history is conflating **administrative workload** with **realized behavioral compliance**. For example, wartime records from the U.S. Department of Labor under **Frances Perkins** document extraordinary administrative throughput—exceeding **100,000 formal rulings and determinations** and roughly **900,000 public and employer inquiries**—yet throughput measures institutional processing capacity rather than automatic market adherence. Similarly, **Harriet Wiseman Elliott's** leadership of the Consumer Division within the Office of Price Administration and Civilian Supply (OPACS) in 1941 centered on consumer information, anti-hoarding norms, and voluntary compliance *prior* to the transition toward statutory price ceilings and mandatory rationing. Meanwhile, **Eleanor Lansing Dulles** operated across international monetary planning (including Bretton Woods preparations and postwar Austrian financial reconstruction), anchoring longer-horizon institutional credibility.

![Heterogeneous Institutional Authority and Compliance Contagion](../figures/03_institutional_authority_network.png)

**Figure 3** (`scripts/03_institutional_authority_network.py`) formalizes this distinction. **Panel A** maps all six officials onto their respective structural transmission channels, weighting direct allocation, administrative throughput, informational framing, macro-monetary coordination, and indirect civilian capacity buffers separately. **Panel B** simulates behavioral compliance across `800` heterogeneous household and firm agents subjected to an inflationary scarcity shock at `t = 6`:
* **Voluntary Messaging Alone (Elliott 1941 Baseline):** Informational appeals elevate compliance above an unregulated panic-hoarding baseline, but compliance plateaus once persistent scarcity pressures incentivize individual defection.
* **Messaging + Administrative Throughput:** Adding institutional rule-processing and dispute resolution dampens compliance decay by reducing ambiguity and reinforcing credible enforcement expectations.
* **Full Multi-Tier Architecture:** Combining structural allocation rules, administrative throughput, expectation anchoring, and civilian/health capacity protection yields the highest post-shock compliance stability.

---

## 4. Methodological Nuances, Scope Conditions, and Limitations

Translating historical governance into econophysics and behavioral models requires explicit guardrails against anachronism and over-attribution:

1. **Non-Uniform Causal Leverage:** None of the six officials exercised unilateral macro-command over an entire national economy. Rosenberg's controlled-referral innovations operated through regional manpower boards before influencing broader WMC policy; Elliott's 1941 OPACS Consumer Division functioned within an advisory and informational mandate prior to mandatory OPA rationing; and Wilkinson and Horsbrugh shaped economic resilience indirectly by protecting civilian safety, shelter, and health rather than setting prices or wages.
2. **Workload vs. Compliance Identification:** High administrative counts—such as Perkins's >