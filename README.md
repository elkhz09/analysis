# Analysis

Research notebooks. Two projects, both finished enough to have a conclusion.

---

## COE Price Dynamics — Singapore

[`coe-price-dynamics/`](coe-price-dynamics/)

Singapore caps the vehicle population and auctions the right to own a car. The
population has been flat since 2016 and premiums have not been. This asks why.

Finding: stock-level supply does not set the price. Deregistrations drive the
quota, the quota drives bidding activity, and it is bids received and new
registrations that Granger-cause premium changes. The premium behaves like an
auction clearing price under competition and expectations, not an equilibrium
price under a supply cap.

ADF tests, first-differencing, Granger causality, lagged correlations, on 20+
years of LTA and data.gov.sg series.

## Recipe Traffic Prediction

[`datacamp-capstone/`](datacamp-capstone/)

Binary classification on recipe metadata, predicting whether a recipe draws high
traffic. The business constraint was precision, not accuracy — a false positive
means promoting a recipe that nobody reads. Logistic regression reached 87%
precision against an 80% target, and was chosen over a gradient-boosted model
with a better F1 because the brief asked for precision and interpretability.

Submitted as the DataCamp Data Scientist Professional capstone.

---

Python, pandas, statsmodels, scikit-learn, Jupyter.

MIT licensed, covering the code and writing here. The DataCamp brief
(`Instruction.pdf`) and the dataset it supplied are not mine to license.
