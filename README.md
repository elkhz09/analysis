# Analysis

Two pieces of research carried to a conclusion, and the working notebooks that
got there. One asks how Singapore's COE premium is actually formed. The other is
a classification problem where the right model was the one that lost on F1.

This is a notebook collection, not a package. Nothing here is installable and
nothing here runs on a schedule. Read the finding, then the notebook if you want
to check it.

---

## COE Price Dynamics, Singapore

[`coe-price-dynamics/`](coe-price-dynamics/)

Singapore caps the vehicle population and auctions the ten-year right to own a
car. Category A population has been statistically flat since 2016. Premiums have
not been. The question is why the two came apart.

The chain the data supports: deregistrations Granger-cause the quota, which is
what the policy is designed to do, since the quota is derived from cars leaving
the fleet. The quota then moves bidding activity and new registrations. But the
quota does not directly move premiums. Bids received and new registrations do.

So the quota sets how many certificates exist and competition among bidders sets
what they cost. Capping the population constrains the first and leaves the second
alone. A premium is an auction clearing price, and reading it as a supply and
demand equilibrium explains very little of its variance.

Monthly LTA and data.gov.sg series, 2002 to 2025. ADF tests, first differencing,
Spearman correlations on levels and differences, Granger causality along the
chain. The two demand-to-premium results are the weakest links in it and the
notebook README says exactly how weak.

## Recipe Traffic Prediction

[`datacamp-capstone/`](datacamp-capstone/)

Binary classification on recipe metadata, predicting whether a recipe draws high
traffic. The cost of error is asymmetric, so the brief set a floor of 80%
precision rather than an accuracy target.

Logistic regression reached 0.87 precision and 0.81 F1. A tuned gradient boosting
model on engineered features reached 0.83 F1 and 0.94 recall, and 0.74 precision,
which is below the floor. Recommended the logistic model: it clears the constraint
that was set, and its coefficients can be read by the people deciding what to
promote. The best model on the usual aggregate metric was the wrong model for the
stated objective.

The strongest predictor was recipe category, not nutrition. Submitted as the
DataCamp Data Scientist Professional capstone, January 2025.

---

Python, pandas, statsmodels, scikit-learn, Jupyter.

MIT licensed, covering the code and writing here. The DataCamp brief
(`Instruction.pdf`) and the dataset it supplied are not mine to license.
