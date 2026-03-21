# Why Your COE Is S$108,000 — And Why It Won't Stay There

*A data-driven look at Singapore's most complained-about market*

---

Every Singaporean has an opinion on COE. Your uncle says it's the government's fault. Your colleague says just take the MRT. Your neighbour just paid S$108,000 for the right to own a car — before the car itself — and is quietly questioning his life choices.

I decided to stop complaining and start analysing. What follows is what 24 years of auction data (Feb 2002 – Feb 2026), a few econometric tests, and one structural forecast actually say about where COE premiums come from, and where they're going.

---

## The System Is Working. That's the Problem.

The COE market is not broken. It is doing exactly what it was designed to do: price out marginal demand until the vehicle population stabilises. The Vehicle Quota System caps the total number of cars on the road. Every month, LTA allocates auction slots based on how many cars were *deregistered roughly six months ago*. Not how many people want a car today. Six months ago.

That lag is the entire story.

When demand surges — post-COVID pent-up buying, PHV fleet expansion, the inexplicable collective decision by half of Singapore to buy a car at the same time — supply cannot respond. The quota is already set. The only thing that can move is price. And move it does.

**The data confirms this at every link in the chain:**

| Causal Link | Lag | p-value |
|---|---|---|
| Deregistrations → Quota | 6 months | 0.003 |
| Quota → Bids received | 5 months | <0.001 |
| Quota → Premium returns | 4 months | 0.021 |

A 1,000-unit increase in monthly quota is associated with a **−2% log return in premium** (p<0.001, HAC-robust standard errors). That is the dominant short-run driver in the model. Not sentiment. Not the bidding frenzy. Quota.

---

## The Number Everyone Watches Is the Wrong Number

The bid-to-quota ratio — bids received divided by slots available — is what most people cite as the measure of market heat. Intuitively it makes sense: more bidders per slot, higher price.

Formally tested, it fails. Granger causality p=0.798. OLS coefficient p=0.415. Statistically indistinguishable from noise.

The reason is economic, not statistical. The bid-to-quota ratio is an *equilibrium outcome* — it reflects the market clearing condition at each auction. By definition, it adjusts simultaneously with price. Asking whether today's ratio predicts tomorrow's premium is asking whether the market's current clearing condition predicts where it will clear next. It does not, because the ratio already incorporates all available information at the moment of clearing.

**Watch the quota numbers. Not the bidding frenzy.**

---

## Two Regimes, One Market

Something changed around 2016. The vehicle population stabilised near 320,000 units. And the COE market became structurally different.

| Metric | Pre-2016 | Post-2016 | Change |
|---|---|---|---|
| Mean premium | S$38,354 | S$67,773 | +77% |
| Median premium | S$35,000 | S$53,243 | +52% |
| Monthly volatility (σ) | 0.11 | 0.06 | −45% |
| Excess demand (mean) | 850 bids/month | 993 bids/month | +17% |

Higher mean, lower volatility. That combination is not random. It reflects a compositional shift in who is buying.

The growth-phase market was full of first-time buyers — price-sensitive, willing to wait, with a genuine outside option (not owning a car yet). The stable-population market is dominated by *replacement buyers* — households renewing an existing car whose COE has expired. Their demand is less elastic because the alternative is losing car access entirely, not just delaying it. More inelastic demand at the margin means the same quota reduction produces a larger price response. Mean premiums rise. Volatility falls because the demand curve is flatter in the relevant range.

Formal break date testing — Chow test, CUSUM, and a grid search across 56 candidate dates from 2008 to 2022 — confirms this break is statistically identifiable, not just an economic narrative.

---

## COVID: The Shock That Explains the Last Three Years

The post-COVID premium surge is not mysterious once you account for what actually happened.

| Period | Mean Premium | Notes |
|---|---|---|
| Pre-COVID (Feb 2002 – Jan 2020) | ~S$38,000 | Full growth + early stable phase |
| COVID dip (Feb 2020 – Jun 2021) | ~S$32,000 | Auctions suspended, showrooms closed |
| Post-COVID (Jul 2021 – Feb 2026) | ~S$85,000 | Pent-up demand released into constrained supply |

Sixteen months of suppressed demand released into a quota system that could not respond. The result was the sharpest sustained rally in the 24-year sample — premiums went from ~S$30k in mid-2020 to S$129,611 at the 2023 peak.

That rebound is now substantially spent. The demand cohort that drove it has been absorbed into the vehicle population. They are not coming back as buyers — they are coming back as *deregistrations*, in about 8–9 years.

---

## The Forecast: Arithmetic, Not Speculation

Short-run premium returns are not reliably forecastable. An ARIMAX model with auction data barely beats a naive random walk on mean absolute error (0.0420 vs 0.0452). The OLS explains 8% of monthly return variance. Anyone claiming to predict next month's COE with precision is selling something.

The 5-year outlook is different. It is not a time-series forecast. It is arithmetic.

**The 2016–2021 registration cohort is coming off the road.**

| Year | Projected Deregistrations (Cat A) | Source Cohort |
|---|---|---|
| 2026 | ~22,000 | 2016 registrations |
| 2027 | ~24,000 | 2017 registrations |
| 2028 | ~26,000 | 2018 registrations |
| 2029 | ~28,000 | 2019 registrations |
| 2030 | ~27,000 | 2020 registrations |
| 2031 | ~25,000 | 2021 registrations |

Those deregistrations feed into quota at a 6-month lag (confirmed, p=0.003). More quota means lower premium returns (confirmed, −2% per 1,000 units, p<0.001). The chain is validated at every link.

**Three scenarios, one direction:**

| Scenario | Assumption | 2031 Premium |
|---|---|---|
| 🐻 Bear | Cohort wave + demand softening from macro headwinds | ~S$48,000 |
| ⚖️ Base | Cohort wave absorbed by resilient replacement demand | ~S$82,000 |
| 🐂 Bull | Demand surge (PHV renewal, population growth) offsets rising supply | ~S$118,000 |

Note: even the bull scenario requires demand to *rise fast enough to offset mechanically rising supply*. A flat-quota bull case is not consistent with the cohort data.

Current premium of S$108,550 sits at **+2.4 standard deviations** above the post-break mean. In 24 years of data, premiums at this z-score have always corrected. The question is not whether they come down. It is how fast.

---

## The Macro Wildcard

The structural supply case for lower premiums is solid. The macro environment makes it more urgent.

Singapore's GDP is approximately 3.5× domestic consumption — the economy runs on trade. The US tariff escalation, Middle East instability keeping oil at US$75–95/bbl, and MAS's downward GDP revision are not modelled here (the data does not support it), but they are asymmetrically skewed to the downside for premiums. The 2008 oil shock saw Cat A premiums fall 60% peak-to-trough. The 2020 COVID shock saw a 40% drawdown in under 6 months.

A recession would dwarf anything the supply mechanics alone can deliver.

---

## What This Means

The supply mechanics are working in your favour. The cohort wave is real and predictable. The macro headwinds are real and not in the model. All three point in the same direction.

The base case of S$82k by 2031 is defensible under stable conditions. Under current conditions, the bear scenario deserves more probability weight than the table implies.

For the Singaporean who has been waiting to buy: patience is the analytically defensible strategy. The relief is already baked in — it just has not arrived yet.

---

## Methodology Note

*Data: SingStat TableBuilder API (M651121, M650291, M650281, M650341). Sample: Feb 2002 – Feb 2026, 289 monthly observations. Tests: ADF stationarity, Granger causality (max lag 6), OLS with Newey-West HAC standard errors (6 lags), Chow test, CUSUM, grid search break date identification, walk-forward ARIMAX validation. All regressions in first differences — the premium series has a unit root in levels (ADF p=0.927) and level regressions produce spurious results.*

---

*This is personal research and documentation. Not financial advice. Do your own due diligence before making any car purchase decisions — or just take the MRT.*
