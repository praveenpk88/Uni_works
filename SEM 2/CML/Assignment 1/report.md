# Airbnb Price Prediction Report

Student: <YOUR NAME> (s1234567)
Course: COSC2793
Date: 11 Apr 2026

## 1. Introduction
Online short-term rental platforms like Airbnb require hosts to set competitive nightly prices. Pricing is influenced by location, listing characteristics, and host attributes. The objective of this project is to build a supervised learning model that predicts the nightly price of a Melbourne listing using historical data. The model is evaluated using standard regression metrics and then used to generate predictions for a separate test set.

## 2. Task Definition
**Learning task:** Supervised regression.

**Target:** `price` (nightly price).

**Inputs:** Listing attributes such as location, room type, capacity, room counts, review statistics, and host information.

**Performance measures:** Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R2.

**Success criteria:** Choose the model with the lowest validation RMSE, corroborated by cross-validation results. Generate a correctly formatted predictions file for the test set.

## 3. Dataset Description
The dataset is derived from Inside Airbnb and a Kaggle Melbourne Airbnb dataset, with additional processing applied for this assignment. The provided files are:

- `train_data.csv`: 8,586 rows and 16 columns (15 features + `price`).
- `test_data.csv`: 8,585 rows and 15 columns (same features, no `price`).

**Features (provided by the brief):**
- host_is_superhost
- city
- country
- latitude
- longitude
- room_type
- accommodates
- bathrooms
- bedrooms
- beds
- minimum_nights
- number_of_reviews
- review_scores_rating
- instant_bookable
- calculated_host_listings_count

**Data types:**
- Categorical: host_is_superhost, city, country, room_type, instant_bookable.
- Numerical: latitude, longitude, accommodates, bathrooms, bedrooms, beds, minimum_nights, number_of_reviews, review_scores_rating, calculated_host_listings_count.

**Missing values:** None detected in the training data.

## 4. Exploratory Data Analysis (EDA)
The target `price` is strongly right-skewed with high-end outliers. Summary statistics:
- min = 0, max = 3000
- mean = 139.77, median = 115.00
- std = 123.29, skew = 5.77

The histogram and boxplot confirm a long tail of high-priced listings. The correlation heatmap shows that `price` is most positively associated with capacity and room-related variables (accommodates, bedrooms, bathrooms, beds). Review metrics and minimum nights have weak correlations with price. This suggests that space and room capacity are primary drivers, while review volume and minimum stay constraints are less predictive in a linear model.

## 5. Preprocessing and Feature Engineering
The dataset includes both numerical and categorical features. A single preprocessing pipeline is used across all models for fair comparison:

- Numerical features: median imputation + standardization
- Categorical features: most-frequent imputation + one-hot encoding

This approach handles mixed data types, stabilizes model training, and avoids data leakage by fitting transformations only within the training fold.

## 6. Evaluation Framework
The evaluation strategy combines a hold-out split and cross-validation:

- Train/validation split: 80/20 with random_state = 42
- Cross-validation: 5-fold CV on the training portion
- Metrics: MAE, RMSE, R2

Validation RMSE is used to select the final model, with CV metrics reported as a robustness check.

## 7. Models Considered
Three linear models (taught up to Week 4) were evaluated:

1. Linear Regression (baseline)
2. Ridge Regression (L2 regularization)
3. Lasso Regression (L1 regularization)

**Hyperparameter analysis:**
- Ridge `alpha` tested on a log-spaced grid from 1e-3 to 1e3.
- Lasso `alpha` tested on a log-spaced grid from 1e-4 to 1e1.

The best `alpha` is chosen by the lowest validation RMSE.

## 8. Results and Model Selection
**Validation and CV performance:**

- Linear Regression
  - Val MAE: 47.82
  - Val RMSE: 103.68
  - Val R2: 0.3955
  - CV MAE: 47.85
  - CV RMSE: 90.68
  - CV R2: 0.4316

- Ridge (best alpha = 31.62)
  - Val MAE: 47.17
  - Val RMSE: 103.57
  - Val R2: 0.3968
  - CV MAE: 47.29
  - CV RMSE: 90.58
  - CV R2: 0.4329

- Lasso (best alpha = 0.152)
  - Val MAE: 47.01
  - Val RMSE: 103.56
  - Val R2: 0.3969
  - CV MAE: 47.24
  - CV RMSE: 90.60
  - CV R2: 0.4327

**Selected model:** Lasso (alpha = 0.152), based on the lowest validation RMSE with comparable CV scores.

## 9. Error Analysis
Residual analysis indicates a largely centered residual pattern, but variance increases for higher predicted prices. This suggests heteroscedasticity and underperformance on expensive listings. Such behavior is typical for linear models applied to skewed targets with outliers.

## 10. Feature Importance (Linear Model Coefficients)
Coefficient inspection indicates that capacity and room-related features contribute positively to price. High positive coefficients appear for:
- accommodates
- bedrooms
- bathrooms
- room_type (Entire home/apt)
- central cities (e.g., Melbourne, Yarra)

Negative coefficients appear for:
- room_type (Shared room)
- certain outer suburbs
- number_of_reviews (small negative effect)

These coefficients are indicative of linear association and should be interpreted cautiously due to multicollinearity and encoding effects.

## 11. Limitations and Ethical Considerations
- Linear models may underfit nonlinear relationships or complex location effects.
- The dataset likely reflects historical market bias; using predictions for automated pricing could reinforce inequities.
- Pricing decisions should remain human-in-the-loop with periodic monitoring for drift and fairness issues.

## 12. Recommendations and Potential Improvements
- Consider target transformations (e.g., log price) to address skew.
- Add engineered interactions (e.g., accommodates x room_type) within allowed methods.
- Use robust validation or trimmed metrics to mitigate outlier impact.
- Incorporate richer location features if available (within policy constraints).

## 13. Conclusion
A consistent preprocessing pipeline was applied across Linear, Ridge, and Lasso models. Lasso (alpha = 0.152) achieved the best validation RMSE and comparable cross-validation performance, making it the selected model for final predictions. The resulting predictions file was generated in the required format.

## 14. References
- Inside Airbnb: https://insideairbnb.com/about/
- Kaggle Melbourne Airbnb Open Data: https://www.kaggle.com/datasets/tylerx/melbourne-airbnb-open-data
- Scikit-learn Documentation: https://scikit-learn.org/

## 15. GenAI Usage Statement
I used GitHub Copilot Chat (VS Code) on 11 Apr 2026 to assist with debugging, explanations, and drafting. Prompts used (exact text) are listed below.

- please resolve the error
- display(train_df.isna().sum()[train_df.isna().sum() > 0]) these 2 doesn't print anything properly
- review  the entire notebook with the provided spec and rubric marking. check for completion and marking the assignment and let me know how much i'll get.
- please do all the 3,
- can you please create  the report,
