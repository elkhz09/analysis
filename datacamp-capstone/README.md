# Recipe Traffic Prediction

Predicting whether a recipe will draw high traffic, from its category and
nutritional metadata. DataCamp Data Scientist Professional capstone, January 2025.

---

## The brief

A food platform wants to decide which recipes to promote on its homepage. The
cost of being wrong is asymmetric: promoting a recipe nobody reads wastes the
slot, while missing a good one costs comparatively little. So the target was
**precision of at least 80%**, not accuracy.

## Result

Logistic regression, on the original features:

| | F1 | AUC | Precision | Recall |
|---|---|---|---|---|
| Logistic regression | 0.809 | 0.870 | **0.87** | 0.76 |
| Gradient boosting (tuned, engineered features) | 0.828 | 0.837 | 0.74 | 0.94 |

Gradient boosting wins on F1 and finds far more of the high-traffic recipes
(recall 0.94 against 0.76). It also misses the brief: at 0.74 precision it falls
below the 80% floor, so a quarter of what it promotes is wrong. Recommended the
logistic model: it clears the constraint that was actually set, and its
coefficients can be read by the people deciding what to promote.

A useful reminder that the best model by the usual aggregate metric can be the
wrong model for the stated objective.

### How much to trust those numbers

947 rows, split 757 train and 190 test. Seven model types across two feature sets,
fourteen combinations in all, were compared on that single 190-row holdout.
Hyperparameters were tuned by 5-fold cross-validation on the training set, so the
tuning is clean, but the final choice between the fourteen was made by looking at
the test set. Picking the best of fourteen on 190 rows makes the reported test
metrics optimistic, and 0.87 precision carries a confidence interval wide enough
to touch the 0.80 floor.

That does not change the recommendation, because the argument does not rest on a
precision of exactly 0.87. It rests on gradient boosting at 0.74 being clearly
below a stated constraint while logistic regression is clearly above it, and on
the logistic model being readable by the people using it. A nested split, or
selection on cross-validated precision rather than on the holdout, is what the
analysis should have done.

## What drove the prediction

Recipe category, by a wide margin. Vegetable, potato and pork are most strongly
associated with high traffic. Nutritional variables (calories, protein, sugar)
were statistically significant but weak. Traffic follows what kind of dish it is,
not its nutritional profile.

## Handling of the data

- Roughly 5.5% missing in the nutritional columns, median-imputed.
- Outliers retained. Extreme values here are plausible recipes, not errors.
- Box-Cox transform on skewed nutritional variables.
- Features added for per-serving nutritional values; categories encoded.

Models compared: logistic regression, random forest, SVM, gradient boosting,
each on original and engineered feature sets.

---

## Files

- `submission.ipynb`, the submitted notebook, outputs included
- `presentation_deck.pdf`, the accompanying presentation
- `Instruction.pdf`, the original brief
- `recipe_site_traffic_2212.csv`, the provided dataset

Dataset supplied by DataCamp as part of the certification.
