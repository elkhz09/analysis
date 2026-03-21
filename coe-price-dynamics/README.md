# COE Price Dynamics — Singapore

Time-series econometric analysis of Singapore's Certificate of Entitlement (COE) premium system, Category A vehicles.

---

## What This Project Demonstrates

Relevant to quant research and financial analysis roles:

- **Time-series econometrics** — ADF stationarity testing, first-differencing, Granger causality
- **Market microstructure reasoning** — auction-cleared price formation vs. static supply-demand equilibrium
- **Structured research methodology** — EDA → diagnostics → causality testing → interpretation
- **Policy-aware analysis** — understanding how institutional design (quota allocation rules) shapes market dynamics
- **Data sourcing and preparation** — 20+ years of LTA / data.gov.sg data across multiple series

---

## Research Question

Does stabilising Singapore's vehicle population stabilise COE premiums?

Category A vehicle population has been statistically stable since 2016, yet COE premiums have remained highly volatile. This analysis investigates the structural reasons.

---

## Methodology

**1. Exploratory Data Analysis**
- Population trends and net supply flow (deregistrations minus new registrations)
- Visual inspection of price cycles and volatility

**2. Correlation Analysis**
- Spearman correlations on levels (structural relationships)
- First-differenced correlations (short-run dynamics)
- Lagged correlations to explore lead-lag structure

**3. Time-Series Diagnostics**
- ADF stationarity tests on all series
- First-differencing where required to avoid spurious regression

**4. Granger Causality Tests**
- Deregistrations → quota allocation
- Quota → bids received and new registrations
- Bids received / new registrations → premium changes

---

## Key Findings

- Category A vehicle population has been statistically stable since 2016; net supply oscillates around zero
- COE premiums remain highly volatile despite population stability — stock-level supply does not determine prices
- Deregistrations Granger-cause quota, consistent with institutional policy design
- Quota influences bidding activity and new registrations, but does not directly drive premiums
- Bids received and new registrations Granger-cause changes in premiums — demand pressure is the dominant short-run price driver
- COE premiums behave like auction-cleared prices influenced by expectations and competition, not static equilibrium prices

---

## Data Sources

All data from **data.gov.sg / LTA** (2002–2025):
- COE quota, bids received, and premiums (monthly, by category)
- Vehicle deregistrations and new registrations
- Vehicle population under the quota system
- COE revalidation statistics

---

## Files

- `coe_analysis.ipynb` — main analysis notebook
