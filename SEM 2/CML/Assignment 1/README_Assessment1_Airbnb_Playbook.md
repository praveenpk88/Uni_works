# Assessment 1 Airbnb Notebook: End-to-End Master Guide

This README is your complete one-stop guide to finish the assignment from scratch.

Use this file to understand:
- what to build,
- how to build it,
- why each step is done,
- what output to produce,
- how to package the final submission.

---

## 1) What You Are Solving

Goal: predict Airbnb listing nightly `price` (regression problem) using provided features.

Input files:
- `train_data.csv` (has target `price`)
- `test_data.csv` (no target)

Output file to submit:
- `sXXXXXXX_predictions.csv`
- exactly one column named `price`
- same row order as `test_data.csv`

---

## 2) Folder Setup (What You Need)

Keep only these files in your assignment folder:
- `assignment1_airbnb_pipeline.ipynb`
- `train_data.csv`
- `test_data.csv`
- `README_Assessment1_Airbnb_Playbook.md`

---

## 3) Notebook Structure You Should Follow

Use this exact section order in the notebook.

1. Title, objective, reproducibility note
2. Imports and setup
3. Task definition and evaluation framework
4. Data loading and schema summary
5. Exploratory data analysis (EDA)
6. Train/validation split + preprocessing pipeline
7. Model 1: LinearRegression
8. Model 2: Ridge (alpha investigation)
9. Model 3: Lasso (alpha investigation)
10. Model comparison and selection
11. Error analysis (residuals)
12. Feature importance interpretation
13. Final model training on full data
14. Test predictions and CSV export
15. Ethical considerations, limitations, conclusion

---

## 4) Full Code Blueprint

Paste these blocks in order and run top-to-bottom.

### 4.1 Imports and setup

```python
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

RANDOM_STATE = 42
sns.set_theme(style='whitegrid')
```

### 4.2 Load data and inspect

```python
train_df = pd.read_csv('train_data.csv')
test_df = pd.read_csv('test_data.csv')

print('Train shape:', train_df.shape)
print('Test shape:', test_df.shape)
display(train_df.head())
display(train_df.dtypes.to_frame('dtype'))
display(train_df.describe(include='all').T)

print('Missing values (train):')
display(train_df.isna().sum()[train_df.isna().sum() > 0])
```

### 4.3 Define features and EDA

```python
X = train_df.drop(columns=['price'])
y = train_df['price']

categorical_features = X.select_dtypes(include=['object', 'string', 'category']).columns.tolist()
numeric_features = [c for c in X.columns if c not in categorical_features]

print('Categorical:', categorical_features)
print('Numeric:', numeric_features)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(y, kde=True, ax=axes[0])
axes[0].set_title('Price distribution')
sns.boxplot(x=y, ax=axes[1])
axes[1].set_title('Price boxplot')
plt.tight_layout()
plt.show()

corr = train_df[numeric_features + ['price']].corr(numeric_only=True)
plt.figure(figsize=(10, 6))
sns.heatmap(corr, cmap='coolwarm', center=0)
plt.title('Numeric correlation heatmap')
plt.tight_layout()
plt.show()
```

### 4.4 Split, preprocess, evaluation function

```python
X_train, X_val, y_train, y_val = train_test_split(
   X, y, test_size=0.2, random_state=RANDOM_STATE
)

preprocessor = ColumnTransformer(
   transformers=[
      ('num', Pipeline([
         ('imputer', SimpleImputer(strategy='median')),
         ('scaler', StandardScaler())
      ]), numeric_features),
      ('cat', Pipeline([
         ('imputer', SimpleImputer(strategy='most_frequent')),
         ('onehot', OneHotEncoder(handle_unknown='ignore'))
      ]), categorical_features)
   ]
)

kfold = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

def metrics(y_true, y_pred):
   return {
      'MAE': mean_absolute_error(y_true, y_pred),
      'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
      'R2': r2_score(y_true, y_pred)
   }

def evaluate(name, model):
   pipe = Pipeline([('preprocess', preprocessor), ('model', model)])
   pipe.fit(X_train, y_train)

   val_pred = pipe.predict(X_val)
   val_m = metrics(y_val, val_pred)

   cv = cross_validate(
      pipe, X_train, y_train, cv=kfold,
      scoring=('neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2'),
      n_jobs=-1
   )

   return {
      'Model': name,
      'Val_MAE': val_m['MAE'],
      'Val_RMSE': val_m['RMSE'],
      'Val_R2': val_m['R2'],
      'CV_MAE': -cv['test_neg_mean_absolute_error'].mean(),
      'CV_RMSE': -cv['test_neg_root_mean_squared_error'].mean(),
      'CV_R2': cv['test_r2'].mean()
   }, pipe
```

### 4.5 Train 3 models

```python
# Model 1
linear_row, _ = evaluate('LinearRegression', LinearRegression())
display(pd.DataFrame([linear_row]))

# Model 2 (Ridge)
ridge_alphas = np.logspace(-3, 3, 13)
ridge_rows = []
for a in ridge_alphas:
   row, _ = evaluate(f'Ridge(alpha={a:.4g})', Ridge(alpha=float(a), random_state=RANDOM_STATE))
   row['alpha'] = a
   ridge_rows.append(row)
ridge_df = pd.DataFrame(ridge_rows).sort_values('Val_RMSE').reset_index(drop=True)
best_ridge_alpha = float(ridge_df.loc[0, 'alpha'])
display(ridge_df.head())

# Model 3 (Lasso)
lasso_alphas = np.logspace(-4, 1, 12)
lasso_rows = []
for a in lasso_alphas:
   row, _ = evaluate(f'Lasso(alpha={a:.4g})', Lasso(alpha=float(a), random_state=RANDOM_STATE, max_iter=20000))
   row['alpha'] = a
   lasso_rows.append(row)
lasso_df = pd.DataFrame(lasso_rows).sort_values('Val_RMSE').reset_index(drop=True)
best_lasso_alpha = float(lasso_df.loc[0, 'alpha'])
display(lasso_df.head())
```

### 4.6 Compare, select, analyze

```python
comparison = pd.DataFrame([
   linear_row,
   ridge_df.loc[0].to_dict(),
   lasso_df.loc[0].to_dict()
]).sort_values('Val_RMSE').reset_index(drop=True)

display(comparison[['Model', 'Val_MAE', 'Val_RMSE', 'Val_R2', 'CV_MAE', 'CV_RMSE', 'CV_R2']])
best_model_name = comparison.loc[0, 'Model']
print('Selected model:', best_model_name)

if best_model_name.startswith('LinearRegression'):
   selected_estimator = LinearRegression()
elif best_model_name.startswith('Ridge'):
   selected_estimator = Ridge(alpha=best_ridge_alpha, random_state=RANDOM_STATE)
else:
   selected_estimator = Lasso(alpha=best_lasso_alpha, random_state=RANDOM_STATE, max_iter=20000)

# Residual analysis on validation split
analysis_pipe = Pipeline([('preprocess', preprocessor), ('model', selected_estimator)])
analysis_pipe.fit(X_train, y_train)
val_pred = analysis_pipe.predict(X_val)
residuals = y_val - val_pred

plt.figure(figsize=(7, 4))
sns.scatterplot(x=val_pred, y=residuals, alpha=0.6)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted price')
plt.ylabel('Residual (actual - predicted)')
plt.title('Residual plot on validation set')
plt.tight_layout()
plt.show()

# Coefficient-based importance
importance_pipe = Pipeline([('preprocess', preprocessor), ('model', selected_estimator)])
importance_pipe.fit(X, y)
model = importance_pipe.named_steps['model']
feature_names = importance_pipe.named_steps['preprocess'].get_feature_names_out()
coef_df = pd.DataFrame({'feature': feature_names, 'coefficient': model.coef_}).sort_values('coefficient')
display(coef_df.head(10))
display(coef_df.tail(10))
```

### 4.7 Final training and prediction export

```python
final_pipeline = Pipeline([('preprocess', preprocessor), ('model', selected_estimator)])
final_pipeline.fit(X, y)

test_pred = np.clip(final_pipeline.predict(test_df), a_min=0, a_max=None)

student_number = 'sXXXXXXX'  # replace
out_file = f'{student_number}_predictions.csv'
pred_df = pd.DataFrame({'price': test_pred})
pred_df.to_csv(out_file, index=False)

print('Saved:', out_file)
print('Shape:', pred_df.shape)
print('Columns:', pred_df.columns.tolist())
display(pred_df.head())

assert pred_df.shape[0] == test_df.shape[0]
assert pred_df.columns.tolist() == ['price']
```

---

## 4.8 Step-by-step explanation (beginner-friendly)

Use this as a plain-English guide for why each block exists and what the outputs mean.

### Imports and setup
- **Why**: Load tools for data handling, plotting, preprocessing, modeling, and evaluation.
- **How**: Import the libraries and set a fixed seed (`RANDOM_STATE = 42`) for reproducibility.
- **Output**: No output; it prepares your environment.

### Load data and inspect
- **Why**: Confirm files load correctly and check basic structure.
- **How**: `read_csv` loads the data, `shape` shows rows/columns, `head()` previews records, `dtypes` shows column types.
- **Output**: Shapes printed, a small sample table, and a list of data types.

### Summary stats and missing values
- **Why**: Understand distributions and detect missing data.
- **How**: `describe(include='all')` summarizes numeric and categorical columns; missing-value check lists only columns with NaNs.
- **Output**: A stats table and either an empty missing-value list or a list of columns with missing values.

### Missingness profile plot
- **Why**: Visualize where missing data concentrates.
- **How**: Count missing values per feature and plot a bar chart if any exist.
- **Output**: A bar chart of missing counts, or a message saying there are none.

### Define features and target
- **Why**: Separate inputs (`X`) from the target (`y`) and identify categorical vs numeric features.
- **How**: Drop `price` from inputs; use dtypes to split feature lists.
- **Output**: Printed lists of categorical and numeric columns.

### Target distribution plots
- **Why**: Check if the target is skewed or has outliers.
- **How**: Histogram + boxplot of `price`.
- **Output**: A histogram (shape of distribution) and a boxplot (outliers and spread).

### Correlation heatmap
- **Why**: See which numeric features move together and which relate to price.
- **How**: Compute correlations for numeric columns and plot a heatmap.
- **Output**: A heatmap; warmer colors indicate stronger positive relationships. This is correlation, not causation.

### Split, preprocess, evaluate
- **Why**: Avoid leakage and ensure fair model evaluation.
- **How**: 80/20 split, preprocessing pipeline for numeric/categorical columns, define metrics and evaluation helper.
- **Output**: No immediate output; it prepares the pipeline and evaluation logic.

### Train 3 models
- **Why**: Compare multiple linear models as required by the brief.
- **How**: Fit Linear Regression, then scan Ridge/Lasso over alpha values.
- **Output**: Tables of validation and CV metrics; best alpha identified by lowest validation RMSE.

### Compare, select, analyze
- **Why**: Choose the best model and interpret error patterns.
- **How**: Combine results, select the lowest validation RMSE, plot residuals, and inspect coefficients.
- **Output**: Comparison table, selected model message, residual plot, and top positive/negative coefficients.

### Final training and prediction export
- **Why**: Train on full data and generate test predictions for submission.
- **How**: Fit the final pipeline on all training data and predict `test_df`.
- **Output**: A CSV file named `{student_number}_predictions.csv` with one column `price`. Assertions confirm format and row count.

---

## 4.9 Line-by-line code explanations (beginner-friendly)

Use this when you want to explain every line in simple terms.

### Imports and setup
- `warnings.filterwarnings('ignore')`: hides non-critical warnings to keep outputs readable.
- `numpy`/`pandas`: numeric and table operations.
- `seaborn`/`matplotlib`: plotting.
- `ColumnTransformer`, `Pipeline`: apply different preprocessing to different columns in one object.
- `SimpleImputer`: fills missing values so models do not crash.
- `OneHotEncoder`: turns categories into numeric columns.
- `StandardScaler`: puts numeric features on comparable scales.
- `train_test_split`, `KFold`, `cross_validate`: data splitting and evaluation.
- `LinearRegression`, `Ridge`, `Lasso`: required linear models (Week 1-4).
- `mean_absolute_error`, `mean_squared_error`, `r2_score`: evaluation metrics.
- `RANDOM_STATE = 42`: ensures the same split each run.
- `sns.set_theme(...)`: controls plot appearance only.

### Load data and inspect
- `pd.read_csv(...)`: load CSV files into DataFrames.
- `shape`: confirms rows/columns and catches file issues.
- `head()`: sanity-check data.
- `dtypes`: decide which columns are numeric vs categorical.
- `describe(include='all')`: distribution statistics for numeric + frequency summaries for categorical.
- `isna().sum()`: missing-value counts per column.

### Missingness profile
- `sort_values(ascending=False)`: show most-missing columns first.
- `missing_counts[missing_counts > 0]`: filter to only missing columns.
- Plot or message: visualize missingness if present.

### Feature/target split
- `X = train_df.drop(columns=['price'])`: inputs only.
- `y = train_df['price']`: target only.
- `select_dtypes(...)`: split categorical vs numeric features.

### Target distribution plots
- `histplot(...)`: shows overall distribution and skew.
- `boxplot(...)`: highlights outliers and spread.

### Correlation heatmap
- `corr(...)`: compute numeric correlations.
- `heatmap(...)`: visualize which features co-move with price (not causal).

### Train/validation split
- `train_test_split(..., test_size=0.2)`: hold-out 20% for validation.

### Preprocessing pipeline
- Numeric pipeline: median imputation + scaling.
- Categorical pipeline: most-frequent imputation + one-hot encoding.
- `ColumnTransformer`: applies both in parallel.

### Evaluation utilities
- `metrics(...)`: returns MAE, RMSE, R2 in one place.
- `evaluate(...)`: trains model, computes validation metrics, and CV metrics.

### Ridge/Lasso tuning
- `np.logspace(...)`: tests alpha across orders of magnitude.
- `ridge_df`/`lasso_df`: results table sorted by best validation RMSE.
- Plot: use alpha-sorted values so the curve is readable.

### Model selection + diagnostics
- `comparison`: side-by-side model metrics.
- `selected_estimator`: choose best model by validation RMSE.
- Residual plot: check bias and error spread.
- Coefficients: interpret strongest positive/negative features (with caution).

### Final predictions
- Fit on all training data, predict test set.
- `np.clip(..., a_min=0)`: avoid negative prices.
- Save CSV and assert row/column correctness.

---

## 4.10 Oral defense: questions you should be ready to answer

Use these as quick answers if asked "why" during a discussion.

### Task and data
- **Why regression?** Target `price` is continuous.
- **Why these features?** Provided by the brief; they cover location, listing, and host info.
- **Any missing values?** Check shows none; imputation stays for robustness.

### Splitting and evaluation
- **Why 80/20 split?** Standard balance between training data and validation reliability.
- **Why cross-validation?** Ensures performance is not a fluke from one split.
- **Why MAE/RMSE/R2?** MAE is interpretable, RMSE penalizes large errors, R2 summarizes explained variance.

### Preprocessing
- **Why impute?** Models cannot handle NaNs; ensures pipeline stability.
- **Why median for numeric?** Robust to outliers and skew.
- **Why most-frequent for categorical?** Simple and consistent when missingness is low.
- **Why one-hot encode?** Linear models require numeric inputs; avoids false ordering.
- **Why standardize?** Ridge/Lasso are scale-sensitive; scaling makes regularization fair.

### Models and tuning
- **Why Linear/Ridge/Lasso?** Week 1-4 allowed methods; good baseline + regularized variants.
- **Why tune alpha?** Controls bias-variance; select best validation RMSE.
- **Why log-spaced alphas?** Regularization strength spans orders of magnitude.

### Diagnostics
- **Why residual plot?** Detect bias, nonlinearity, and heteroscedasticity.
- **Why coefficients?** Provide interpretable feature direction/magnitude (with caution).

### Output
- **Why clip predictions at 0?** Prices cannot be negative.
- **Why assert checks?** Ensure CSV matches submission format.

---

## 5) What To Write In Markdown (Inside Notebook)

For each section, explain:
- what you did,
- why you did it,
- what the output means,
- what limitation remains.

Minimum markdown sections to include:
- Task definition
- Dataset overview
- EDA interpretation
- Preprocessing rationale
- Model-by-model interpretation
- Hyperparameter effect (Ridge/Lasso alpha)
- Model comparison and selection rationale
- Residual/error interpretation
- Feature importance interpretation
- Real-world suitability
- Ethics and professional responsibility
- Conclusion

---

## 6) Report Blueprint (5 to 10 pages)

Use these headings:
1. Introduction
2. Task Definition
3. Dataset Description
4. EDA
5. Splitting and Preprocessing
6. Model Development (3 models)
7. Hyperparameter Investigation
8. Comparative Evaluation
9. Error Analysis + Feature Importance
10. Ethical Considerations and Professional Responsibilities
11. Recommendations and Improvements
12. Conclusion
13. References

---

## 7) Submission Files You Must Produce

1. `assignment1_airbnb_pipeline.ipynb`
2. PDF export of notebook (same content)
3. `sXXXXXXX_predictions.csv`
4. report PDF

---

## 8) Practical Writing Tips For Better Marks

- Avoid generic claims like "model performed well". Always cite numbers.
- Compare at least validation and CV metrics when selecting model.
- Mention both strengths and failure cases (e.g., outliers, high-price errors).
- Keep language concise, technical, and evidence-based.
- In ethics section, discuss bias, transparency, uncertainty, accountability.

---

## 9) Install Requirements

```bash
pip install numpy pandas seaborn matplotlib scikit-learn
```

---

## 10) Final Run Instructions

1. Open notebook.
2. Replace placeholders for name and student number.
3. Run all cells top-to-bottom once.
4. Confirm selected model and saved predictions file.
5. Export notebook PDF.
6. Finalize report PDF.

If you follow this README from start to finish, you can complete the assignment end-to-end using only this file and the two CSV datasets.

---

## 11) Course Content Integration (Week 1 to Week 4)

This section connects lecture theory to what you are implementing in this assignment.

### 11.1 Week 1 Foundations: Task, Experience, Performance

Core idea from class:
- A learning system is defined by Task (T), Experience (E), and Performance (P).

For this assignment:
- Task (T): supervised regression to predict listing price.
- Experience (E): training examples from train_data.csv.
- Performance (P): MAE, RMSE, and R2 measured on validation/CV splits.

Write this in your notebook/report:
- "This problem is a supervised learning regression task because the target variable price is continuous."
- "The model learns a mapping from listing features to price using historical labeled examples."

### 11.2 Week 2 Regression: Model Space, Loss, Optimization

Core idea from class:
- Regression learns an approximation f_hat(x) to unknown target function f(x).
- Linear regression chooses a linear model space.
- Typical training objective uses squared-error style loss.

In sklearn, optimization is handled internally (you do not manually code gradient descent), but the conceptual objective is the same: minimize prediction error on training data while preserving generalization.

How this appears in your notebook:
- LinearRegression gives a baseline linear model.
- Ridge and Lasso add regularization to control complexity.

Write this in your notebook/report:
- "Linear regression provides a strong interpretable baseline for continuous target prediction."
- "Regularized variants are used to reduce overfitting risk by constraining coefficient magnitude."

### 11.3 Week 2 Practical Issue: Feature Scaling

Core idea from class:
- Very different feature scales can make optimization unstable/slow and coefficients hard to compare.

How your pipeline addresses it:
- StandardScaler is applied to numeric features.
- OneHotEncoder is used for categorical variables.

Write this in your notebook/report:
- "Numeric scaling standardizes features to comparable ranges, improving regularized model behavior."

### 11.4 Week 3 Regularization: Bias-Variance Tradeoff

Core idea from class:
- Increasing model complexity can overfit (high variance).
- Too simple models can underfit (high bias).
- Regularization parameter alpha/lambda controls this tradeoff.

How this appears in your notebook:
- You tune alpha for Ridge and Lasso.
- You compare validation and CV metrics to select a balanced model.

Important interpretation from Week 3:
- Larger alpha: stronger regularization, simpler model, potential underfitting.
- Smaller alpha: weaker regularization, more flexible model, potential overfitting.

Write this in your notebook/report:
- "Hyperparameter tuning was used to identify the regularization strength that best balanced underfitting and overfitting."

### 11.5 Week 4 Evaluation: Hold-Out, Validation, and CV

Core idea from class:
- Do not use test data for model tuning.
- Use hold-out validation and/or cross-validation for model selection.
- Keep final test set independent for final prediction/output.

How your notebook follows this:
- 80/20 train-validation split for development.
- 5-fold CV on training portion for stability.
- test_data.csv is only used at the final prediction stage.

Write this in your notebook/report:
- "Model selection was based on validation and cross-validation metrics; test data remained unseen during development to preserve independence."

### 11.6 Week 4 Metrics: Why MAE, RMSE, and R2

Use this interpretation directly:
- MAE: average absolute pricing error in currency units (business-readable).
- RMSE: penalizes larger errors, useful when large mistakes are costly.
- R2: proportion of variance in price explained by the model.

Write this in your notebook/report:
- "RMSE was prioritized for final ranking because large pricing errors are practically more harmful than small deviations."

### 11.7 What Not To Do (Directly from Week 4 Principles)

- Do not tune alpha on test data.
- Do not report only one metric.
- Do not claim causal relationships from correlation plots.
- Do not compare models using training error only.

---

## 12) Ready-to-Use Markdown Snippets (Copy Into Notebook)

### 12.1 Task Definition Snippet

"The task is supervised regression: estimate nightly Airbnb price from listing, host, and location features. Because price is continuous, regression is appropriate rather than classification."

### 12.2 Preprocessing Rationale Snippet

"A column-wise preprocessing pipeline is used to prevent data leakage and ensure compatibility with linear-family models: median imputation and scaling for numeric features, and most-frequent imputation plus one-hot encoding for categorical features."

### 12.3 Evaluation Framework Snippet

"An 80/20 hold-out split is used for model development, while 5-fold cross-validation on the training split estimates metric stability. The test set is kept independent and used only after final model selection."

### 12.4 Hyperparameter Snippet

"Regularization strength (alpha) was tuned for Ridge/Lasso. Small alpha values reduce regularization and may overfit, while large values increase shrinkage and may underfit. The selected alpha achieved the best validation RMSE with competitive CV performance."

### 12.5 Ethics Snippet

"This model should be used as decision support, not an autonomous pricing authority. Historical data may encode socioeconomic or geographic bias, and predictions should be communicated with uncertainty awareness and human oversight."

---

## 13) COSC2673 vs COSC2793 Focus

If you are in COSC2793, explicitly strengthen these parts:
- Hyperparameter analysis depth (alpha trend and justification).
- Feature importance discussion from model coefficients.
- More critical evaluation of limitations and professional responsibility.

If you are in COSC2673, keep these too, but depth can be slightly lighter while still evidence-based.
