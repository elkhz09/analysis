# COE Price Dynamics, Singapore

Singapore limits its vehicle population with a quota and auctions the right to
own a car for ten years, the Certificate of Entitlement. Category A population
has been statistically flat since 2016. Premiums over the same period have been
anything but. This looks at why the two came apart.

---

## Question

Does stabilising the vehicle population stabilise COE premiums?

Short answer: no, and the reason is where in the system the quota binds.

## Findings

- Category A population has been statistically stable since 2016, with net
  supply, deregistrations minus new registrations, oscillating around zero.
- Premiums stayed volatile throughout. Stock-level supply does not set the price.
- Deregistrations Granger-cause the quota, which is what the policy is designed
  to do: the quota is derived from cars leaving the fleet.
- The quota moves bidding activity and new registrations, but does not directly
  move premiums.
- Bids received and new registrations Granger-cause changes in premiums. Demand
  pressure dominates short-run price formation.

So the quota determines how many certificates exist, and competition among
bidders determines what they cost. Capping the population constrains the first
and leaves the second alone. A premium is an auction clearing price, and treating
it as a supply-demand equilibrium price explains none of its variance.

## Method

Exploratory analysis of population and net supply flow, then Spearman
correlations on levels and on first differences, then ADF tests on every series
with differencing where needed to avoid spurious regression, then Granger
causality along the chain above. Monthly data, 2002 to 2025.

ADF puts quota, bids, premium, deregistrations and new registrations in levels as
non-stationary and stationary after one difference, consistent with I(1). Net
supply is stationary in levels, which is what a policy that targets a stable
fleet should produce. Everything downstream is run on differences, and premium on
log differences.

## How strong the findings actually are

Worth stating plainly, because the headline conclusion rests on the weakest two
tests in the table.

Granger tests were run over lags 1 to 6 and the reported p-value for each pair is
the smallest across those six lags. For the strong relationships that choice
changes nothing: quota to new registrations is 4e-13, quota to bids is 5e-07,
new registrations to quota is 2.6e-04, deregistrations to quota is 4.1e-03. Any
correction leaves them significant.

For the two results that carry the argument it does matter. New registrations to
premium is p = 0.016 at lag 2, and bids to premium is p = 0.020 at lag 6. Both are
the best of six lags. Adjust for having picked the best of six and neither clears
5%. So the direction is supported and the significance is weaker than the summary
table implies, and the honest version of the claim is that demand-side flows are
the only variables that show any predictive relationship to premiums at all, not
that the relationship is firmly established.

Granger causality is predictive precedence, not causation. The series are
administrative monthly aggregates and the quota is set by formula, so some of what
looks like prediction is mechanism.

## Data

data.gov.sg and LTA: quota, bids received and premiums by category; new
registrations and deregistrations; vehicle population under the quota system;
revalidation statistics. All public.

---

## Files

Read `coe_market_dynamics_professional.ipynb` for the written-up version of the
argument. Note that it is a writeup rather than a live notebook: most cells are
not executed, and the numbers in it come from the working notebooks below.

`coe_analysis.ipynb` is the analysis proper: diagnostics, tests and charts, with
outputs saved.

The rest are kept deliberately, as working passes rather than tidy results:

- `coe.ipynb`, `coe2.ipynb` are earlier passes over the same question. `coe2`
  contains the ACF/PACF and stationarity exploration that set up the
  differencing decision. `coe.ipynb` is large; it carries embedded plot output.
- `bike.py` is a data.gov.sg API client with on-disk caching, written to pull the
  series without re-downloading them.
- `bike2.py` is a SingStat table-builder fetcher, same purpose, different source.
- `bike_analysis.ipynb` is the motorcycle category thread. Separate question,
  unfinished, left in because the fetchers are the useful part.
- `substack_coe.md` is a draft writeup for a general audience.
- `coe_results.csv` is the pulled bidding series: one row per month, bidding
  round and category, with quota, bids received, successful bids and premium.
  `coe.csv` is a 410-row premium series. Neither is test output, which an
  earlier version of this file claimed.

If you only read one thing, read the findings above. If you want to check the
work, `coe_analysis.ipynb`.
