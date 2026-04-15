# Airbnb Price Prediction Report

Student: Praveen Kumar Saravanan (S4163448)
Course: COSC2793
Date: 11 Apr 2026

## 1. Introduction
Online short-term rental platforms like Airbnb require hosts to set competitive nightly prices. Pricing is influenced by location, listing characteristics, and host attributes. The objective of this project is to build a supervised learning model that predicts the nightly price of a Melbourne listing using historical data. The model is evaluated using standard regression metrics and then used to generate predictions for a separate test set. All results are reproducible with a fixed random seed (random_state = 42).

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

### 3.1 Descriptive Statistics and Categorical Distributions
Per-feature statistics are computed directly from the training data. Numerical features report min, max, mean, median, and standard deviation. Categorical features report unique values, most frequent category, and its count.

**Numerical features (including target):**

| Feature | Min | Max | Mean | Median | Std |
| --- | --- | --- | --- | --- | --- |
| latitude | -38.224 | -37.491 | -37.825 | -37.816 | 0.065 |
| longitude | 144.532 | 145.760 | 145.009 | 144.977 | 0.130 |
| accommodates | 1.000 | 16.000 | 3.560 | 3.000 | 2.226 |
| bathrooms | 0.000 | 9.000 | 1.282 | 1.000 | 0.558 |
| bedrooms | 0.000 | 10.000 | 1.533 | 1.000 | 0.916 |
| beds | 0.000 | 18.000 | 2.036 | 2.000 | 1.545 |
| price | 0.000 | 3000.000 | 139.771 | 115.000 | 123.293 |
| minimum_nights | 1.000 | 1000.000 | 3.159 | 2.000 | 20.788 |
| number_of_reviews | 1.000 | 479.000 | 27.947 | 11.000 | 42.410 |
| review_scores_rating | 20.000 | 100.000 | 94.176 | 97.000 | 8.472 |
| calculated_host_listings_count | 1.000 | 98.000 | 7.427 | 1.000 | 15.438 |

**Categorical features:**

| Feature | Unique | Top | Freq |
| --- | --- | --- | --- |
| host_is_superhost | 2 | f | 6105 |
| city | 30 | Melbourne | 2917 |
| country | 1 | Australia | 8586 |
| room_type | 3 | Entire home/apt | 5771 |
| instant_bookable | 2 | f | 4461 |

## 4. Exploratory Data Analysis (EDA)
The target `price` is strongly right-skewed with high-end outliers. Summary statistics:
- min = 0, max = 3000
- mean = 139.77, median = 115.00
- std = 123.29, skew = 5.77

The histogram and boxplot confirm a long tail of high-priced listings. The correlation heatmap shows that `price` is most positively associated with capacity and room-related variables (accommodates, bedrooms, bathrooms, beds). Review metrics and minimum nights have weak correlations with price. This suggests that space and room capacity are primary drivers, while review volume and minimum stay constraints are less predictive in a linear model.

Capacity-related features (accommodates, bedrooms, beds, bathrooms) are also correlated with each other, indicating multicollinearity. Regularized models (Ridge/Lasso) are therefore suitable choices because they stabilize coefficients when predictors overlap and help identify the most informative features without discarding them prematurely.

## 5. Preprocessing and Feature Engineering
The dataset includes both numerical and categorical features. A single preprocessing pipeline (scikit-learn ColumnTransformer + Pipeline) is used across all models for fair comparison:

- Numerical features: median imputation + standardization
- Categorical features: most-frequent imputation + one-hot encoding

This approach handles mixed data types, stabilizes model training, and avoids data leakage by fitting transformations only within the training fold.

## 6. Evaluation Framework
The evaluation strategy combines a hold-out split and cross-validation:

- Train/validation split: 80/20 with random_state = 42
- Cross-validation: 5-fold CV on the training portion (KFold, shuffle=True, random_state=42)
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

**Why these models:** Linear Regression provides a transparent baseline. Ridge reduces sensitivity to multicollinearity by shrinking coefficients, while Lasso performs implicit feature selection by driving weaker coefficients to zero. These models align with the course scope and offer interpretability appropriate for explaining price drivers.

## 8. Results and Model Selection
**Validation and CV performance:**

| Model | Val MAE | Val RMSE | Val R2 | CV MAE | CV RMSE | CV R2 |
| --- | --- | --- | --- | --- | --- | --- |
| Linear Regression | 47.82 | 103.68 | 0.3955 | 47.85 | 90.68 | 0.4316 |
| Ridge (alpha = 31.62) | 47.17 | 103.57 | 0.3968 | 47.29 | 90.58 | 0.4329 |
| Lasso (alpha = 0.152) | 47.01 | 103.56 | 0.3969 | 47.24 | 90.60 | 0.4327 |

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

Across models, the importance ranking is consistent for the strongest signals (capacity, room type, and location). Ridge keeps all features but reduces volatility of coefficients; Lasso highlights a smaller subset by zeroing some one-hot categories, which acts as a simple feature selection mechanism.

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

## 14. Prediction Output
The final model was refit on the full training data and applied to the test set. Predictions were saved to s4163448_predictions.csv with a single column named price, matching the required submission format.

## 15. References
- Inside Airbnb: https://insideairbnb.com/about/
- Kaggle Melbourne Airbnb Open Data: https://www.kaggle.com/datasets/tylerx/melbourne-airbnb-open-data
- Scikit-learn Documentation: https://scikit-learn.org/

## 16. GenAI Usage Statement
I used GitHub Copilot Chat (VS Code) on 11 Apr 2026 to assist with debugging, explanations, and drafting. Prompts used (exact text) are listed below.

- explain the error in cell 17
- display(train_df.isna().sum()[train_df.isna().sum() > 0]) these 2 doesn't print anything properly
- rephrase the markdown on cell 1,2,5,7,15
- rephrase and correct the grammer for the report content,
