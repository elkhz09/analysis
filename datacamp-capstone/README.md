# 🍽️ Recipe Traffic Prediction  
**Predicting High-Traffic Recipes for Business Optimization**

**Author:** Eleanor Koh  
**Date:** January 2025  
**Credential:** DataCamp – Data Scientist Certification (Capstone Project)

---

## 📌 Project Overview

This project focuses on predicting whether a recipe will generate **high user traffic**, enabling a digital food platform to make better content and promotion decisions.

The problem is framed as a **binary classification task**, with a strong emphasis on **precision**, reflecting the real business cost of promoting recipes that fail to attract users.

---

## 🎯 Business Objective

- **Primary goal:** Identify high-traffic recipes with **≥ 80% precision**
- **Key constraint:** Minimize false positives (promoting low-performing recipes)
- **Outcome:** Support content curation and marketing prioritization using data-driven insights

---

## 📊 Data & Features

### Dataset Characteristics
- Recipe metadata, categories, and nutritional information
- Target variable: **High Traffic (Yes / No)**

### Data Preparation
- **Missing values:**  
  ~5.5% missing in nutritional variables, imputed using median values
- **Outliers:**  
  Retained based on domain reasoning (extreme values may reflect valid recipes)
- **Transformations:**  
  Box-Cox transformation applied to reduce skewness
- **Feature Engineering:**  
  - Nutritional values per serving  
  - Encoded categorical recipe types

---

## 🔍 Exploratory Data Analysis (EDA)

### Key Insights
- **Recipe category** is the strongest predictor of traffic
- Categories with strong positive association:
  - **Vegetable**
  - **Potato**
  - **Pork**
- Nutritional variables (calories, protein, sugar) show weaker but statistically significant effects

**EDA takeaway:**  
Traffic is driven more by **content type** than nutritional composition alone.

---

## 🤖 Models Evaluated

The following models were trained and compared:

- Logistic Regression (interpretable baseline)
- Random Forest (non-linear ensemble)
- Support Vector Machine
- Gradient Boosting (high-performance ensemble)

---

## 📈 Model Performance

### Final Model Selection

**Logistic Regression (Original Dataset)**  
- **Precision:** **87%** ✅ (exceeds business requirement)
- **F1-score:** 0.815
- High interpretability and stability

**Gradient Boosting (Engineered Features)**  
- **F1-score:** **0.828** (best overall balance)
- Higher recall, slightly lower precision

**Model choice rationale:**  
Logistic Regression was recommended due to its alignment with the business objective, interpretability, and ease of deployment.

---

## 🔑 Feature Importance

Top predictors of high-traffic recipes:
1. **Vegetable**
2. **Potato**
3. **Pork**

These features were:
- Statistically significant in EDA
- Consistently important across models

---

## 💡 Business Recommendations

1. **Content Optimization**
   - Prioritize promotion of recipes in high-performing categories
   - Use model outputs to guide homepage and campaign placement

2. **Data Enrichment**
   - Collect additional nutritional attributes (e.g. fat content)
   - Incorporate user behavior data to improve demand modeling

---

## 🚀 Key Takeaways

- Achieved **87% precision**, exceeding the required threshold
- Demonstrated the value of **interpretable models** in business contexts
- Showcased a complete data science workflow:
  - EDA → Feature Engineering → Modeling → Business Translation

---

## 🔮 Future Work

- Integrate user interaction data (clicks, saves, dwell time)
- Explore time-based trends in recipe popularity
- Deploy the model as a real-time content scoring tool


