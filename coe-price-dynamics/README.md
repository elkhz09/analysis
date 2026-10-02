# COE Price Dynamics — Singapore

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
  supply — deregistrations minus new registrations — oscillating around zero.
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
causality along the chain above. Monthly data, 2002–2025.

## Data

data.gov.sg and LTA: quota, bids received and premiums by category; new
registrations and deregistrations; vehicle population under the quota system;
revalidation statistics. All public.

---

## Files

Read `coe_market_dynamics_professional.ipynb` for the written-up version of the
argument. Note that it is a writeup rather than a live notebook — most cells are
not executed, and the numbers in it come from the working notebooks below.

`coe_analysis.ipynb` is the analysis proper: diagnostics, tests and charts, with
outputs saved.

The rest are kept deliberately, as working passes rather than tidy results:

- `coe.ipynb`, `coe2.ipynb` — earlier passes over the same question. `coe2`
  contains the ACF/PACF and stationarity exploration that set up the
  differencing decision. `coe.ipynb` is large; it carries embedded plot output.
- `bike.py` — a data.gov.sg API client with on-disk caching, written to pull the
  series without re-downloading them.
- `bike2.py` — a SingStat table-builder fetcher, same purpose, different source.
- `bike_analysis.ipynb` — the motorcycle category thread. Separate question,
  unfinished, left in because the fetchers are the useful part.
- `substack_coe.md` — a draft writeup for a general audience.
- `coe.csv`, `coe_results.csv` — the pulled series and the test output.

If you only read one thing, read the findings above. If you want to check the
work, `coe_analysis.ipynb`.
