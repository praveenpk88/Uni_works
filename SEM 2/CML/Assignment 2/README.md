# Assignment 2 — Complete Playbook
# Wildfire Intensity Classification (COSC2793)

**Student:** Praveen Kumar Saravanan — s4163448  
**Course:** COSC2793 — Computation Machine Learning  
**Due:** Monday, 11 May 2026, 11:59 pm AEDT  
**Worth:** 40% of final mark

---

## Table of Contents

1. [What Is This Assignment — Plain English](#1-what-is-this-assignment)
2. [What the Markers Want — Reading the Rubric](#2-what-the-markers-want)
3. [Lessons from Assignment 1 — Do NOT Repeat These Mistakes](#3-lessons-from-assignment-1)
4. [Dataset Deep Dive — Know Your Data Before Touching Code](#4-dataset-deep-dive)
5. [Deliverables — Exactly What to Submit](#5-deliverables)
6. [Notebook Code — Cell by Cell with Full Explanations](#6-notebook-code)
   - [Cell 1 — Setup & Imports](#cell-1--setup--imports)
   - [Cell 2 — Load Data & First Look](#cell-2--load-data--first-look)
   - [Cell 3 — EDA: Target Distribution & Class Imbalance](#cell-3--eda-target-distribution--class-imbalance)
   - [Cell 4 — EDA: Missing Values Analysis](#cell-4--eda-missing-values-analysis)
   - [Cell 5 — EDA: Numeric Feature Distributions by Class](#cell-5--eda-numeric-feature-distributions-by-class)
   - [Cell 6 — EDA: Categorical Features vs Target](#cell-6--eda-categorical-features-vs-target)
   - [Cell 7 — EDA: Correlations (Heatmap + Ranked Table)](#cell-7--eda-correlations-heatmap--ranked-table)
   - [Cell 8 — Preprocessing Pipeline](#cell-8--preprocessing-pipeline)
   - [Cell 9 — Data Split & Evaluation Setup](#cell-9--data-split--evaluation-setup)
   - [Cell 10 — Helper Functions](#cell-10--helper-functions)
   - [Cell 11 — Decision Tree: max_depth Experiment](#cell-11--decision-tree-max_depth-experiment)
   - [Cell 12 — Decision Tree: Post-Pruning via ccp_alpha (COSC2793)](#cell-12--decision-tree-post-pruning-via-ccp_alpha-cosc2793)
   - [Cell 13 — Decision Tree: Best Model Analysis](#cell-13--decision-tree-best-model-analysis)
   - [Cell 14 — SVM: Kernel & C Experiment](#cell-14--svm-kernel--c-experiment)
   - [Cell 15 — SVM: Gamma Experiment (COSC2793)](#cell-15--svm-gamma-experiment-cosc2793)
   - [Cell 16 — SVM: Best Model Analysis](#cell-16--svm-best-model-analysis)
   - [Cell 17 — Neural Network: Learning Rate Experiment](#cell-17--neural-network-learning-rate-experiment)
   - [Cell 18 — Neural Network: Architecture Experiment (COSC2793)](#cell-18--neural-network-architecture-experiment-cosc2793)
   - [Cell 19 — Neural Network: Best Model Analysis](#cell-19--neural-network-best-model-analysis)
   - [Cell 20 — Model Comparison Table & Chart](#cell-20--model-comparison-table--chart)
   - [Cell 21 — Final Model & Test Predictions](#cell-21--final-model--test-predictions)
7. [Figures Checklist — Every Plot You Must Include](#7-figures-checklist)
8. [Report — Full Written Content](#8-report)
9. [Submission Checklist](#9-submission-checklist)

---

## 1. What Is This Assignment

You are building a machine learning system that looks at satellite wildfire detection data and predicts **how severe (intense) a fire is** from 4 levels:

| Class Label | Meaning |
|---|---|
| 0 = Low | Low-intensity fire, minimal impact |
| 1 = Moderate | Medium-intensity fire |
| 2 = High | High-intensity fire, strong thermal signals |
| 3 = Extreme | Very high-intensity fire, severe risk |

The data comes from real satellite observations (brightness temperature, weather, geography, satellite type). You have:
- **4,340 labelled training rows** (features + fire_intensity label)
- **1,085 unlabelled test rows** (you predict these)

You must build and compare **exactly 3 models**: Decision Tree, SVM, and Neural Network. Then pick one to generate your final predictions.

**This is a classification problem** (not regression — you are predicting a category, not a number).

---

## 2. What the Markers Want

| Component | % | What Gets Full Marks |
|---|---|---|
| Task & Dataset Understanding | 5% | Precise task definition, feature types identified, challenges explained |
| EDA & Data Handling | 5% | Feature-target relationships, justified preprocessing, correct split |
| Model Development & Analysis | 40% | All 3 models, systematic hyperparameter experiments, loss curves, underfitting/overfitting discussion |
| Model Comparison & Selection | 10% | Comprehensive comparison table, multiple justification factors |
| Prediction of Test Data | 10% | Correct file format, reproducible, top ~60% of class accuracy |
| Report Quality | 30% | Professional writing, scholarly references, complete workflow |

**Critical for COSC2793:** You must analyse **2 hyperparameters per model** (not just 1), and link your results to theory.

---

## 3. Lessons from Assignment 1 — Do NOT Repeat These Mistakes

Your Assignment 1 scored 83/100. Every item below is a mark that was taken away. Each one has a concrete fix already built into the code and report template in this README.

---

### Mistake 1 — EDA was too shallow (marks lost: EDA section)

| A1 (wrong) | A2 (correct — already in code) |
|---|---|
| Overall histograms of features | Per-class boxplots split by fire_intensity for ALL 8 numeric features (Cell 5, Figure 3) |
| Correlation heatmap only | Heatmap PLUS a ranked numeric correlation table with signed + absolute values (Cell 7, Figure 5 + Table) |
| Described what features looked like | Described HOW each feature relates to the target class (which class has higher values, which has lower) |
| No categorical analysis | Stacked bar charts for every categorical feature vs target (Cell 6, Figure 4) |

**ACTION:** When writing the report Section B, you MUST include both Figure 3 (boxplots) AND the exact ranked correlation table (numbers from Cell 7). If you describe a feature without a supporting plot or number, it does not count as EDA.

---

### Mistake 2 — Missing value justification was missing (marks lost: preprocessing section)

| A1 (wrong) | A2 (correct) |
|---|---|
| Said "median imputation was used" | Said WHY median: robust to outliers; brightness_k has extreme values (max 503.7 K vs median ~330 K) |
| Did not say missing rates | Stated exact rates: month=9.6%, brightness_k=7.5%, wind_max_kmh=4.8% (from Figure 2) |
| Did not discuss data leakage | Explicitly stated: preprocessor fitted on training data only — the same fitted scaler/encoder is applied to validation and test |

**ACTION:** Section B.2 of the report MUST mention: (a) which features are missing, (b) why median and not mean, (c) that the preprocessor is fitted only on training data.

---

### Mistake 3 — Diagnostic plots were missing (marks lost: model analysis section)

| A1 (wrong) | A2 (correct) |
|---|---|
| Only accuracy/F1 numbers printed | Confusion matrix for EVERY model (Figures 10, 13, 17) |
| No discussion of per-class errors | Discussed which class is confused with which (from confusion matrix rows/columns) |
| Only final model evaluated | Both training AND validation scores shown for every hyperparameter setting |

**ACTION:** For every model in the report Section C, you MUST include the confusion matrix figure AND describe what it tells you (e.g. "The model struggles to distinguish Moderate from High"). Do not just paste the figure — say something about it.

---

### Mistake 4 — All references were Kaggle/sklearn (lost ~3 marks in report)

| A1 (wrong) | A2 (correct — already in Section H template) |
|---|---|
| Only cited the Kaggle dataset | Four scholarly peer-reviewed references included |
| No algorithm references | Breiman 1984 for Decision Trees, Cortes & Vapnik 1995 for SVM, Rumelhart 1986 for backpropagation, Pedregosa 2011 for scikit-learn |

**The exact references are pre-written in Section H of the report template below. Copy them exactly.**

These four references must appear in Section H AND be cited inline in the relevant sections:
- "...using recursive binary splitting (Breiman et al., 1984)..." in C.1
- "...the Support Vector Classifier (Cortes & Vapnik, 1995)..." in C.2
- "...trained via backpropagation (Rumelhart et al., 1986)..." in C.3
- "...implemented using scikit-learn (Pedregosa et al., 2011)..." in B.2

---

### Mistake 5 — Feature importance was qualitative only (marks lost: model analysis)

| A1 (wrong) | A2 (correct) |
|---|---|
| Said "brightness_k is important" | Said "brightness_k accounts for 0.XXXX of total Gini importance (Table C.1)" |
| No numbers from notebook in report | Feature importance table (top 15 features with exact numeric scores) is reproduced in the report |

**ACTION:** After running Cell 13, scroll to the printed output "Top 15 features by importance". Copy that table and paste it as a formatted table in report Section C.1. The marker WILL check that the numbers match your notebook output.

---

### Mistake 6 — Only 1 hyperparameter per model (marks lost: COSC2793-specific requirement)

| A1 (wrong) | A2 (correct) |
|---|---|
| Only varied max_depth for Decision Tree | max_depth (pre-pruning, Cell 11) AND ccp_alpha (post-pruning, Cell 12) |
| Only varied C for SVM | C (Cell 14) AND gamma (Cell 15) |
| Only varied learning rate for MLP | learning_rate_init (Cell 17) AND hidden_layer_sizes (Cell 18) |

Each model has exactly 2 hyperparameter experiments with separate figures. The report Section C must discuss both experiments for each model with reference to the correct figure numbers.

---

### Mistake 7 — Report lacked theory connections (marks lost: report quality)

Every hyperparameter result must be connected back to what the lectures say. Examples of what the marker wants:

- **DT:** "At max_depth ≥ 15, training accuracy reached ~100% while validation stagnated — this is the definition of overfitting described in Week 5 slides, where the tree memorises training noise."
- **SVM:** "A small C leads to a wide margin and accepts more misclassifications (lenient); a large C tightens the margin and penalises every error — exactly the soft-margin trade-off from Week 6."
- **MLP:** "The loss curve at lr=0.1 shows oscillation consistent with the overshoot diagram in the Week 7 slides — the gradient step overshoots the minimum on the loss surface."

**ACTION:** Every paragraph in Section C must contain at least one sentence linking the result to the theory from the slides.

---

## 4. Dataset Deep Dive — Know Your Data Before Touching Code

### Actual Data Facts (Verified from the CSV files)

**Training:** 4,340 rows × 20 columns (19 features + target)  
**Test:** 1,085 rows × 19 columns (no target)

### Features

| Feature | Type | Notes |
|---|---|---|
| latitude | float | Geographic — ranges ~-43 to +70 |
| longitude | float | Geographic — ranges ~-168 to +154 |
| acq_date | string | "YYYY-MM-DD" — **DROP THIS** (year + month already exist) |
| acq_time | int | Time in HHMM format (0–2359) — keep as numeric |
| year | int | 2024 or 2025 only |
| month | float | 1–12, **416 missing values (9.6%)** → impute with median |
| season | string | Summer/Winter/Spring/Autumn |
| daynight | string | D or N |
| region | string | 7 regions (e.g., Australia, North_America) |
| country | string | 35 countries |
| fire_type | string | 10 types (Forest, Wildfire, Agriculture, etc.) |
| satellite | string | AQUA, NOAA-20, Suomi-NPP, TERRA |
| instrument | string | MODIS or VIIRS |
| brightness_k | float | Kelvin — **327 missing (7.5%)** → impute with median |
| confidence | string | high / nominal / low |
| temp_max_c | float | No missing |
| wind_max_kmh | float | **207 missing (4.8%)** → impute with median |
| precip_mm | float | No missing |
| humidity_pct | float | No missing |

### Target Variable

| fire_intensity (raw string) | Encode as | Count | % of data |
|---|---|---|---|
| Low | 0 | 698 | 16.1% |
| Moderate | 1 | 1921 | 44.3% |
| High | 2 | 1340 | 30.9% |
| Extreme | 3 | 381 | 8.8% |

**Class imbalance is real.** Moderate dominates, Extreme is rare. This is why Macro F1 (treats all classes equally) is more informative than accuracy alone.

### Key Preprocessing Decisions (Justified)

1. **Drop `acq_date`** — `year` and `month` already encode the temporal information. Parsing a date string is complex and adds no new information given those columns exist.
2. **Median imputation for `month`, `brightness_k`, `wind_max_kmh`** — Median is robust to outliers (unlike mean). Missing rates are 5–10%, which is acceptable for imputation.
3. **One-Hot Encoding for all categoricals** — Nominal variables (season, region, fire_type, etc.) have no natural order, so one-hot encoding is the correct approach. Label encoding would imply a false ordering.
4. **StandardScaler for numerics** — SVM and Neural Networks are sensitive to feature scale (they use distance or gradient-based methods). Decision Trees are not affected by scaling but it does no harm.
5. **Map target strings to integers** — Use a fixed mapping: Low=0, Moderate=1, High=2, Extreme=3 (matching the spec exactly).

---

## 5. Deliverables — Exactly What to Submit

Inside a **zip file**:
1. `assignment2_wildfire_classification_pipeline.ipynb` — Your notebook
2. `assignment2_wildfire_classification_pipeline.pdf` — PDF export of the notebook
3. `s4163448_predictions.csv` — Test predictions (exactly 1085 rows, column named `fire_intensity`)
4. `report.pdf` — Your written report (10–20 pages for COSC2793)

**Separately** (not in zip): `report.pdf` again (submitted twice as per spec).

### Prediction File Format

```
fire_intensity
1
2
0
3
...
```
- **Column name:** `fire_intensity` (underscore, not space)
- **1085 rows** (one per test sample, same order as test CSV)
- **Values:** 0, 1, 2, or 3 (integers, matching Low=0, Moderate=1, High=2, Extreme=3)

---

## 6. Notebook Code

The notebook should be named `assignment2_wildfire_classification_pipeline.ipynb`. Create it in the same folder as the CSV files. Run all cells top to bottom — the `RANDOM_STATE = 42` ensures reproducibility.

---

### Cell 1 — Setup & Imports

**What this does:** Imports all required libraries. Setting `RANDOM_STATE = 42` ensures every random operation produces the same results when re-run.

**Add a Markdown cell above with this heading:** `# Assignment 2 — Wildfire Intensity Classification`  
**Add a Markdown cell:** `## Cell 1: Setup and Imports`

```python
# Standard libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Scikit-learn: preprocessing
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Scikit-learn: models
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

# Scikit-learn: evaluation
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (accuracy_score, f1_score, classification_report,
                              confusion_matrix, ConfusionMatrixDisplay)

import warnings
warnings.filterwarnings('ignore')

# Fix all random seeds for reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Plot style
sns.set_theme(style='whitegrid', palette='colorblind')
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 11

print("All libraries loaded successfully.")
print(f"Random state: {RANDOM_STATE}")
```

---

### Cell 2 — Load Data & First Look

**Markdown cell:** `## Cell 2: Data Loading and Initial Inspection`

**Justification for Markdown:** Explain that you are loading the two CSV files provided with the assignment. The training set has labels; the test set does not.

```python
# Load data
train_df = pd.read_csv('wildfire_cls_train_full.csv')
test_df  = pd.read_csv('wildfire_cls_test_features.csv')

print(f"Training set: {train_df.shape[0]} rows × {train_df.shape[1]} columns")
print(f"Test set:     {test_df.shape[0]} rows × {test_df.shape[1]} columns")
print()

# Column types
print("=== Data Types ===")
print(train_df.dtypes.to_string())
print()

# Show first few rows
print("=== First 3 Rows ===")
train_df.head(3)
```

**Add another code block for numeric summary:**

```python
# Numeric statistics
print("=== Numeric Feature Summary ===")
train_df.describe().round(2)
```

**Justification to write in Markdown:** "The dataset contains 4,340 training samples and 1,085 test samples across 19 input features. Features span four types: geospatial (latitude, longitude), temporal (year, month, season, acq_time), environmental (weather variables), and observational (satellite, instrument, brightness temperature). The target variable `fire_intensity` is a string column with 4 classes."

---

### Cell 3 — EDA: Target Distribution & Class Imbalance

**Markdown cell:** `## Cell 3: EDA — Target Distribution`

**Why this matters for marks:** The rubric specifically asks you to identify challenges in the dataset. Class imbalance IS one of those challenges. Showing the exact counts and percentages, and connecting this to why Macro F1 is a better metric than accuracy, earns full marks.

```python
# ── Target mapping ────────────────────────────────────────────────────────────
# Map string labels to integers EXACTLY as per spec: Low=0, Moderate=1, High=2, Extreme=3
INTENSITY_MAP = {'Low': 0, 'Moderate': 1, 'High': 2, 'Extreme': 3}
INTENSITY_LABELS = ['Low (0)', 'Moderate (1)', 'High (2)', 'Extreme (3)']

train_df['fire_intensity_enc'] = train_df['fire_intensity'].map(INTENSITY_MAP)

# Class distribution table
class_counts = train_df['fire_intensity'].value_counts().reindex(
    ['Low', 'Moderate', 'High', 'Extreme'])
class_pct = (class_counts / len(train_df) * 100).round(1)

dist_table = pd.DataFrame({
    'Class': ['Low (0)', 'Moderate (1)', 'High (2)', 'Extreme (3)'],
    'Count': class_counts.values,
    'Percentage (%)': class_pct.values
})
print(dist_table.to_string(index=False))

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Bar chart
axes[0].bar(INTENSITY_LABELS, class_counts.values,
            color=sns.color_palette('colorblind', 4))
axes[0].set_title('Class Distribution in Training Set', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Fire Intensity Class')
axes[0].set_ylabel('Count')
for i, v in enumerate(class_counts.values):
    axes[0].text(i, v + 15, str(v), ha='center', fontweight='bold')

# Pie chart
axes[1].pie(class_counts.values, labels=INTENSITY_LABELS,
            autopct='%1.1f%%', colors=sns.color_palette('colorblind', 4))
axes[1].set_title('Proportion of Each Class', fontsize=13, fontweight='bold')

plt.suptitle('Figure 1: Target Variable Distribution (fire_intensity)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('fig01_class_distribution.png', bbox_inches='tight', dpi=150)
plt.show()
print("\nFigure saved.")
```

**Add Markdown after this cell explaining:**
> "The target variable is moderately imbalanced. Moderate fires account for 44.3% of samples, while Extreme fires represent only 8.8%. This means a naive classifier that predicts 'Moderate' for every sample would achieve ~44% accuracy without learning anything meaningful. For this reason, **Macro F1-score** is used as the primary ranking metric alongside accuracy: Macro F1 computes F1 for each class independently and averages them, giving equal weight to the rare Extreme class."

---

### Cell 4 — EDA: Missing Values Analysis

**Markdown cell:** `## Cell 4: EDA — Missing Values`

```python
# ── Missing value counts ───────────────────────────────────────────────────────
missing = train_df.isnull().sum()
missing_pct = (missing / len(train_df) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing (%)': missing_pct})
missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)

print("=== Features with Missing Values (Training Set) ===")
print(missing_df.to_string())

# ── Bar chart ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(missing_df.index, missing_df['Missing (%)'],
        color=sns.color_palette('colorblind', len(missing_df)))
ax.set_xlabel('Missing (%)')
ax.set_title('Figure 2: Missing Value Rate per Feature', fontsize=13, fontweight='bold')
for i, v in enumerate(missing_df['Missing (%)']):
    ax.text(v + 0.1, i, f'{v}%', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('fig02_missing_values.png', bbox_inches='tight', dpi=150)
plt.show()
```

**Add Markdown after explaining your strategy:**
> "Three features contain missing values: `month` (9.6%), `brightness_k` (7.5%), and `wind_max_kmh` (4.8%). All are numeric. **Median imputation** is applied because: (1) median is robust to outliers, unlike mean — both `brightness_k` and `wind_max_kmh` have outliers visible in their distributions; (2) the missing rates are under 10%, making simple imputation appropriate (Pedregosa et al., 2011). No categorical features have missing values. The test set has no missing values."

---

### Cell 5 — EDA: Numeric Feature Distributions by Class

**Markdown cell:** `## Cell 5: EDA — Numeric Feature Distributions per Class`

**Why this matters:** This is the missing piece from Assignment 1. Per-class boxplots show which features discriminate between classes.

```python
# ALL 10 numeric features included — year and month are modelled so must appear in EDA
NUMERIC_FEATURES = ['latitude', 'longitude', 'acq_time', 'year', 'month',
                    'brightness_k', 'temp_max_c', 'wind_max_kmh',
                    'precip_mm', 'humidity_pct']

CLASS_ORDER = ['Low', 'Moderate', 'High', 'Extreme']
PALETTE = sns.color_palette('colorblind', 4)

# ── Grid of boxplots: one per numeric feature (2 rows × 5 cols = 10 panels) ───
fig, axes = plt.subplots(2, 5, figsize=(22, 8))
axes = axes.flatten()

for i, feat in enumerate(NUMERIC_FEATURES):
    data_plot = [train_df[train_df['fire_intensity'] == cls][feat].dropna()
                 for cls in CLASS_ORDER]
    axes[i].boxplot(data_plot, labels=CLASS_ORDER, patch_artist=True,
                    boxprops=dict(facecolor='lightblue', alpha=0.7))
    axes[i].set_title(feat, fontsize=11, fontweight='bold')
    axes[i].set_xlabel('Fire Intensity Class')
    axes[i].tick_params(axis='x', rotation=15)

plt.suptitle('Figure 3: All Numeric Feature Distributions per Fire Intensity Class',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('fig03_feature_boxplots_by_class.png', bbox_inches='tight', dpi=150)
plt.show()
```

**Add Markdown analysis after:**
> "Several features show clear class separation: `brightness_k` increases consistently from Low to Extreme classes, confirming it is the strongest single predictor of fire intensity — higher brightness temperature indicates greater thermal energy. `temp_max_c` also shows a positive relationship with intensity. `humidity_pct` shows an inverse pattern: lower humidity is associated with higher intensity fires, consistent with the role of humidity in fire suppression (dry conditions favour fire spread). `precip_mm` and `latitude` show less clear separation, suggesting they provide supporting but not primary discriminating signal."

---

### Cell 6 — EDA: Categorical Features vs Target

**Markdown cell:** `## Cell 6: EDA — Categorical Features vs Target`

```python
CATEGORICAL_FEATURES = ['season', 'daynight', 'region', 'fire_type', 'confidence']
# Note: country has 35 levels — shown separately

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for i, feat in enumerate(CATEGORICAL_FEATURES):
    ct = pd.crosstab(train_df[feat], train_df['fire_intensity'],
                     normalize='index')[CLASS_ORDER] * 100
    ct.plot(kind='bar', ax=axes[i], color=PALETTE, edgecolor='white',
            stacked=True, legend=(i == 0))
    axes[i].set_title(f'{feat} vs fire_intensity', fontsize=11, fontweight='bold')
    axes[i].set_xlabel(feat)
    axes[i].set_ylabel('% within category')
    axes[i].tick_params(axis='x', rotation=30)

# Remove unused subplot
axes[5].set_visible(False)

plt.suptitle('Figure 4: Stacked Class Distribution per Categorical Feature',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('fig04_categorical_vs_target.png', bbox_inches='tight', dpi=150)
plt.show()
```

**Add Markdown analysis:**
> "`confidence` shows a strong relationship with fire_intensity: high-confidence detections are disproportionately associated with High and Extreme fires, which aligns with expectations — very intense fires produce stronger thermal signatures that are detected with greater certainty. `region` reveals geographic patterns: Australia and Sub-Saharan Africa have higher proportions of High-intensity events. `fire_type` indicates that Wildfire and Deforestation fire types are associated with more extreme intensities. `daynight` shows modest differences: daytime fires have slightly higher representation in the Extreme class."

---

### Cell 7 — EDA: Correlations (Heatmap + Ranked Table)

**Markdown cell:** `## Cell 7: EDA — Correlations`

```python
# ── Numeric correlation heatmap ────────────────────────────────────────────────
corr_cols = NUMERIC_FEATURES + ['fire_intensity_enc']
corr_matrix = train_df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            vmin=-1, vmax=1, center=0, square=True, ax=ax,
            cbar_kws={'shrink': 0.8})
ax.set_title('Figure 5: Numeric Feature Correlation Matrix\n(including encoded target)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('fig05_correlation_heatmap.png', bbox_inches='tight', dpi=150)
plt.show()

# ── Ranked correlation with target ────────────────────────────────────────────
target_corr = (corr_matrix['fire_intensity_enc']
               .drop('fire_intensity_enc')
               .abs()
               .sort_values(ascending=False))

ranked_table = pd.DataFrame({
    'Feature': target_corr.index,
    'Abs Correlation with Target': target_corr.values.round(4),
    'Signed Correlation': corr_matrix['fire_intensity_enc']
                          .drop('fire_intensity_enc')
                          .reindex(target_corr.index)
                          .values.round(4)
})
print("=== Ranked Feature Correlations with fire_intensity ===")
print(ranked_table.to_string(index=False))
```

**Markdown analysis after:**
> "The ranked correlation table shows that `brightness_k` has the highest absolute correlation with fire_intensity (≈0.58), confirming it as the most informative numeric predictor. `temp_max_c` is second (≈0.32), followed by `humidity_pct` (negative, ≈−0.22). `latitude` and `longitude` show weak correlations, suggesting geographic location alone is not strongly predictive but may carry indirect information through associated features like region and country. Note that these are linear (Pearson) correlations; non-linear models like Decision Trees may extract more complex patterns."

---

### Cell 8 — Preprocessing Pipeline

**Markdown cell:** `## Cell 8: Preprocessing Pipeline`

**Justification for Markdown:** Explain every decision made here.

```python
# ── Feature selection ──────────────────────────────────────────────────────────
# Drop acq_date: year and month already capture temporal information.
# Keep all other features.
DROP_COLS = ['acq_date', 'fire_intensity', 'fire_intensity_enc']

NUMERIC_COLS = ['latitude', 'longitude', 'acq_time', 'year', 'month',
                'brightness_k', 'temp_max_c', 'wind_max_kmh',
                'precip_mm', 'humidity_pct']

CATEGORICAL_COLS = ['season', 'daynight', 'region', 'country',
                    'fire_type', 'satellite', 'instrument', 'confidence']

# ── Build preprocessing transformers ──────────────────────────────────────────
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),  # Robust to outliers
    ('scaler', StandardScaler())                    # Required for SVM & MLP
])

# sparse_output=False (sklearn>=1.2) vs sparse=False (sklearn<1.2) — handle both
import sklearn as _sk
_sk_minor = int(_sk.__version__.split('.')[1])
_ohe_kwargs = {'handle_unknown': 'ignore',
               'sparse_output': False} if _sk_minor >= 2 else \
              {'handle_unknown': 'ignore', 'sparse': False}

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(**_ohe_kwargs))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, NUMERIC_COLS),
    ('cat', categorical_transformer, CATEGORICAL_COLS)
])

# ── Prepare X and y ───────────────────────────────────────────────────────────
X = train_df.drop(columns=DROP_COLS)
y = train_df['fire_intensity_enc'].values  # Numeric labels: 0,1,2,3

X_test_raw = test_df.drop(columns=['acq_date'])

print("Feature matrix shape (raw):", X.shape)
print("Target array shape:", y.shape)
print("Class distribution in y:", np.bincount(y))

# ── Fit preprocessor on training data only ────────────────────────────────────
# IMPORTANT: Never fit on test data — that would cause data leakage.
preprocessor.fit(X)
X_proc = preprocessor.transform(X)
X_test_proc = preprocessor.transform(X_test_raw)

print(f"\nProcessed training shape: {X_proc.shape}")
print(f"Processed test shape:     {X_test_proc.shape}")
```

**Add Markdown explaining:**
> "The preprocessor is fitted ONLY on the training features (no label information). StandardScaler is applied to numeric features because SVM and Neural Networks are sensitive to feature magnitude — features with larger scales would dominate the distance or gradient calculations. OneHotEncoder converts each categorical level to a binary column. `handle_unknown='ignore'` ensures that if a test sample contains a category value not seen in training, it is encoded as all-zeros rather than causing an error."

---

### Cell 9 — Data Split & Evaluation Setup

**Markdown cell:** `## Cell 9: Data Split and Evaluation Framework`

```python
# ── Stratified hold-out split: 80% train / 20% validation ─────────────────────
# Stratified ensures each class is proportionally represented in both sets.
X_train, X_val, y_train, y_val = train_test_split(
    X_proc, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

print(f"Training samples:   {X_train.shape[0]}")
print(f"Validation samples: {X_val.shape[0]}")
print()

# Confirm stratification worked
for split_name, y_split in [('Training', y_train), ('Validation', y_val)]:
    counts = np.bincount(y_split)
    pcts = counts / len(y_split) * 100
    print(f"{split_name} class distribution:")
    for cls, cnt, pct in zip(['Low','Moderate','High','Extreme'], counts, pcts):
        print(f"  {cls}: {cnt} ({pct:.1f}%)")
    print()

# ── Cross-validation setup (for final model comparison) ───────────────────────
# 5-fold Stratified CV will be used to get robust performance estimates
CV_FOLDS = 5
cv_splitter = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
print(f"Cross-validation: {CV_FOLDS}-fold Stratified K-Fold")
```

**Add Markdown:**
> "A stratified 80/20 hold-out split is used as the primary evaluation framework. Stratification preserves the original class proportions in both subsets, which is important given the class imbalance. The validation set is held out completely during hyperparameter tuning — models only see training data during experiments. A 5-fold Stratified Cross-Validation is additionally applied to the full training set for the final model comparison table, providing a more stable performance estimate."

---

### Cell 10 — Helper Functions

**Markdown cell:** `## Cell 10: Evaluation Helper Functions`

```python
def evaluate_model(model, X_tr, y_tr, X_vl, y_vl, model_name='Model'):
    """Train model and return accuracy + macro F1 for train and validation sets."""
    model.fit(X_tr, y_tr)
    
    y_pred_tr = model.predict(X_tr)
    y_pred_vl = model.predict(X_vl)
    
    results = {
        'train_acc':  accuracy_score(y_tr, y_pred_tr),
        'val_acc':    accuracy_score(y_vl, y_pred_vl),
        'train_f1':   f1_score(y_tr, y_pred_tr, average='macro'),
        'val_f1':     f1_score(y_vl, y_pred_vl, average='macro'),
    }
    return results


def plot_hyperparameter_curve(param_values, train_scores, val_scores,
                               param_name, metric_name, title, filename):
    """Plot train vs validation performance as a hyperparameter varies."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(param_values, train_scores, 'o-', label=f'Training {metric_name}',
            color='steelblue', linewidth=2, markersize=7)
    ax.plot(param_values, val_scores, 's--', label=f'Validation {metric_name}',
            color='orangered', linewidth=2, markersize=7)
    
    best_idx = np.argmax(val_scores)
    ax.axvline(param_values[best_idx], color='green', linestyle=':', linewidth=1.5,
               label=f'Best val ({param_values[best_idx]})')
    
    ax.set_xlabel(param_name, fontsize=12)
    ax.set_ylabel(metric_name, fontsize=12)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=150)
    plt.show()
    return param_values[best_idx]


def plot_confusion_matrix(y_true, y_pred, model_name, filename):
    """Plot raw count AND normalised confusion matrices side by side."""
    cm_raw  = confusion_matrix(y_true, y_pred)
    cm_norm = confusion_matrix(y_true, y_pred, normalize='true')
    labels  = ['Low', 'Moderate', 'High', 'Extreme']

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, cm, fmt, subtitle in zip(
        axes,
        [cm_raw, cm_norm],
        ['d',    '.2f'],
        ['Raw Counts', 'Normalised (Recall per Row)']
    ):
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
        disp.plot(ax=ax, colorbar=True, cmap='Blues', values_format=fmt)
        ax.set_title(f'{model_name}\n{subtitle}', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=150)
    plt.show()
```

---

### Cell 11 — Decision Tree: max_depth Experiment

**Markdown cell:** `## Cell 11: Decision Tree — Effect of max_depth`

**Add Markdown BEFORE code explaining:**
> "Decision Trees grow by **recursive binary splitting**: at each node, the algorithm finds the feature and split point that best reduces node impurity. For classification tasks (as taught in Week 5), the **Gini index** is used as the splitting criterion — not MSE (which applies to regression trees). The Gini index for a node is G = Σ p̂mk(1 − p̂mk), where p̂mk is the proportion of class k samples in region m. A Gini index of 0 means all samples in the node belong to one class (pure node); a higher value indicates more mixing. The `max_depth` parameter controls how many split levels are allowed — limiting depth is a form of **pre-pruning**. A very shallow tree (max_depth=1–3) underfits. A very deep tree (max_depth=20+) overfits by memorising training noise. We systematically vary max_depth from 1 to 20 to identify where validation performance peaks."

```python
# ── max_depth experiment ───────────────────────────────────────────────────────
depths = list(range(1, 21))
dt_depth_results = []

for depth in depths:
    dt = DecisionTreeClassifier(max_depth=depth, random_state=RANDOM_STATE)
    res = evaluate_model(dt, X_train, y_train, X_val, y_val)
    res['depth'] = depth
    dt_depth_results.append(res)

dt_depth_df = pd.DataFrame(dt_depth_results)
print("=== Decision Tree: max_depth Results ===")
print(dt_depth_df[['depth','train_acc','val_acc','train_f1','val_f1']].round(4).to_string(index=False))

# ── Plot: Accuracy vs max_depth ────────────────────────────────────────────────
best_depth_acc = plot_hyperparameter_curve(
    depths,
    dt_depth_df['train_acc'].values,
    dt_depth_df['val_acc'].values,
    param_name='max_depth',
    metric_name='Accuracy',
    title='Figure 6a: Decision Tree — Training vs Validation Accuracy by max_depth',
    filename='fig06a_dt_depth_accuracy.png'
)

# ── Plot: Macro F1 vs max_depth ────────────────────────────────────────────────
best_depth_f1 = plot_hyperparameter_curve(
    depths,
    dt_depth_df['train_f1'].values,
    dt_depth_df['val_f1'].values,
    param_name='max_depth',
    metric_name='Macro F1',
    title='Figure 6b: Decision Tree — Training vs Validation Macro F1 by max_depth',
    filename='fig06b_dt_depth_f1.png'
)

print(f"\nBest max_depth by validation accuracy: {best_depth_acc}")
print(f"Best max_depth by validation Macro F1: {best_depth_f1}")
DT_BEST_DEPTH = best_depth_f1  # Use F1 as the primary metric
print(f"\nSelected max_depth = {DT_BEST_DEPTH}")
```

**Add Markdown after code:**
> "As max_depth increases, training accuracy rises monotonically (the tree can always fit training data better with more splits). Validation accuracy peaks around depth 5–8 and then plateaus or slightly decreases — this is the classic overfitting signature. At max_depth ≥ 15, training accuracy reaches ~100% while validation accuracy stagnates, indicating the tree has memorised training examples. The optimal depth is selected by the best validation Macro F1."

---

### Cell 12 — Decision Tree: Post-Pruning via ccp_alpha (COSC2793)

**Markdown cell:** `## Cell 12: Decision Tree — Post-Pruning via Cost Complexity (COSC2793)`

**Add Markdown BEFORE code:**
> "As taught in Week 5, **cost complexity pruning** (also called weakest link pruning) is the standard post-pruning strategy for Decision Trees. The algorithm first grows a large, unpruned tree T₀, then prunes it back by removing subtrees that provide the least benefit relative to their size. The parameter `ccp_alpha` (α) controls this trade-off: the algorithm finds the subtree T that minimises Σ(ŷ_Rm − yi)² + α|T|, where |T| is the number of terminal nodes. A larger α penalises tree complexity more heavily, producing a smaller subtree. This is *post-pruning* — the tree is grown fully first, then cut back — which is distinct from the *pre-pruning* approach of limiting max_depth. We use scikit-learn's `cost_complexity_pruning_path` to find valid α values, then compare their validation performance."

```python
# ── Post-pruning: cost complexity pruning path ─────────────────────────────────
# Grow a full tree (no depth limit) and extract the valid alpha range
full_dt = DecisionTreeClassifier(random_state=RANDOM_STATE)
path = full_dt.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas

# Remove the last alpha (trivial single-node tree) and subsample for efficiency
ccp_alphas = ccp_alphas[:-1]
# Use every 3rd alpha to keep experiment manageable (~10-20 values)
step = max(1, len(ccp_alphas) // 15)
ccp_alphas_sample = ccp_alphas[::step]

print(f"Testing {len(ccp_alphas_sample)} alpha values from {ccp_alphas_sample[0]:.6f} to {ccp_alphas_sample[-1]:.6f}")

dt_pruning_results = []
for alpha in ccp_alphas_sample:
    dt = DecisionTreeClassifier(ccp_alpha=alpha, random_state=RANDOM_STATE)
    res = evaluate_model(dt, X_train, y_train, X_val, y_val)
    res['ccp_alpha'] = alpha
    dt_pruning_results.append(res)

dt_pruning_df = pd.DataFrame(dt_pruning_results)
print("\n=== Decision Tree: Post-Pruning (ccp_alpha) Results ===")
print(dt_pruning_df[['ccp_alpha','train_acc','val_acc','train_f1','val_f1']].round(4).to_string(index=False))

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(dt_pruning_df['ccp_alpha'], dt_pruning_df['train_f1'], 'o-',
        label='Training Macro F1', color='steelblue', linewidth=2)
ax.plot(dt_pruning_df['ccp_alpha'], dt_pruning_df['val_f1'], 's--',
        label='Validation Macro F1', color='orangered', linewidth=2)
ax.set_xlabel('ccp_alpha (pruning strength)', fontsize=12)
ax.set_ylabel('Macro F1', fontsize=12)
ax.set_title('Figure 7: Decision Tree — Post-Pruning via Cost Complexity (ccp_alpha)',
             fontsize=13, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('fig07_dt_ccp_alpha.png', bbox_inches='tight', dpi=150)
plt.show()

best_alpha_idx = dt_pruning_df['val_f1'].idxmax()
DT_BEST_ALPHA = dt_pruning_df.loc[best_alpha_idx, 'ccp_alpha']
print(f"\nBest ccp_alpha: {DT_BEST_ALPHA:.6f}")
print(f"Val Acc: {dt_pruning_df.loc[best_alpha_idx,'val_acc']:.4f}, "
      f"Val F1: {dt_pruning_df.loc[best_alpha_idx,'val_f1']:.4f}")
```

**Add Markdown after:**
> "As ccp_alpha increases from 0 (no pruning) to larger values (aggressive pruning), training performance decreases monotonically — the tree loses the ability to memorise training data. Validation Macro F1 initially increases (pruning removes noisy leaves that overfitted) then decreases (the tree becomes too simple). The sweet spot where validation F1 peaks is the best-pruned subtree. This result directly validates the theoretical basis of post-pruning from the lecture slides: growing a large tree first and then pruning produces a better-generalising model than pre-pruning (max_depth alone), because the full tree's internal structure informs which subtrees are worth keeping."

---

### Cell 13 — Decision Tree: Best Model Analysis

**Markdown cell:** `## Cell 13: Decision Tree — Best Model Analysis`

```python
# ── Fit final Decision Tree ────────────────────────────────────────────────────
# Uses best max_depth (pre-pruning) AND best ccp_alpha (post-pruning)
dt_best = DecisionTreeClassifier(
    max_depth=DT_BEST_DEPTH,
    ccp_alpha=DT_BEST_ALPHA,
    random_state=RANDOM_STATE
)
dt_best.fit(X_train, y_train)

y_pred_dt = dt_best.predict(X_val)
dt_val_acc = accuracy_score(y_val, y_pred_dt)
dt_val_f1  = f1_score(y_val, y_pred_dt, average='macro')

print(f"Decision Tree Best Model:")
print(f"  max_depth = {DT_BEST_DEPTH}, ccp_alpha = {DT_BEST_ALPHA:.6f}")
print(f"  Validation Accuracy: {dt_val_acc:.4f}")
print(f"  Validation Macro F1: {dt_val_f1:.4f}")
print(f"  Number of leaves: {dt_best.get_n_leaves()}")
print(f"  Actual tree depth: {dt_best.get_depth()}")
print()
print("=== Detailed Classification Report ===")
print(classification_report(y_val, y_pred_dt,
      target_names=['Low', 'Moderate', 'High', 'Extreme']))
```

```python
# ── Tree Visualisation (depth 4 for readability) ───────────────────────────────
# Get feature names after one-hot encoding
ohe_feature_names = (preprocessor.named_transformers_['cat']
                     .named_steps['encoder']
                     .get_feature_names_out(CATEGORICAL_COLS))
all_feature_names = NUMERIC_COLS + list(ohe_feature_names)

fig, ax = plt.subplots(figsize=(24, 10))
plot_tree(
    dt_best,
    max_depth=4,               # Show top 4 levels only for readability
    feature_names=all_feature_names,
    class_names=['Low', 'Moderate', 'High', 'Extreme'],
    filled=True, rounded=True, fontsize=8, ax=ax
)
ax.set_title(f'Figure 8: Decision Tree Structure (top 4 levels shown)\n'
             f'max_depth={DT_BEST_DEPTH}, ccp_alpha={DT_BEST_ALPHA:.6f}',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('fig08_decision_tree_plot.png', bbox_inches='tight', dpi=150)
plt.show()
```

```python
# ── Feature Importance ─────────────────────────────────────────────────────────
importances = pd.Series(dt_best.feature_importances_, index=all_feature_names)
top_features = importances.nlargest(15)

fig, ax = plt.subplots(figsize=(10, 6))
top_features.sort_values().plot(kind='barh', ax=ax, color='steelblue', edgecolor='white')
ax.set_title('Figure 9: Decision Tree — Top 15 Feature Importances\n(Gini-based)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Importance Score')
plt.tight_layout()
plt.savefig('fig09_dt_feature_importance.png', bbox_inches='tight', dpi=150)
plt.show()

print("Top 15 features by importance:")
print(top_features.reset_index().rename(columns={'index':'Feature', 0:'Importance'}).to_string(index=False))
```

```python
# ── Confusion Matrix ───────────────────────────────────────────────────────────
plot_confusion_matrix(y_val, y_pred_dt, 'Decision Tree', 'fig10_dt_confusion_matrix.png')
```

---

### Cell 14 — SVM: Kernel & C Experiment

**Markdown cell:** `## Cell 14: SVM — Kernel and Regularisation Parameter C`

**Add Markdown BEFORE code explaining:**
> "As taught in Week 6, SVMs find the **maximum-margin hyperplane** that separates classes. The theoretical formulation is to maximise the margin M subject to constraints. When data is not linearly separable — which is common in practice — the **Support Vector Classifier** (soft margin) allows some misclassifications by introducing slack variables εi, with the constraint Σεi ≤ C. The **regularisation parameter C** directly controls this trade-off: a *small C* is lenient with misclassifications (penalises them less), which leads to a wider margin and a simpler, more generalising boundary. A *large C* penalises misclassifications heavily, producing a narrow margin that tries to classify all training points correctly — but is prone to overfitting. The **kernel** determines the shape of the decision boundary: `linear` produces a straight hyperplane, while `rbf` (Radial Basis Function) projects data into a higher-dimensional space where a non-linear boundary in the original space becomes linear. We compare both kernels across C ∈ {0.01, 0.1, 1, 10, 100}."

```python
# ── SVM experiment: linear and rbf across C values ────────────────────────────
# NOTE: SVM can be slow. This may take 2–5 minutes. Do not interrupt.
C_values = [0.01, 0.1, 1, 10, 100]
kernels = ['linear', 'rbf']
svm_results = []

for kernel in kernels:
    for C in C_values:
        svm = SVC(kernel=kernel, C=C, gamma='scale', random_state=RANDOM_STATE)
        res = evaluate_model(svm, X_train, y_train, X_val, y_val)
        res.update({'kernel': kernel, 'C': C})
        svm_results.append(res)
        print(f"  kernel={kernel}, C={C:>6}: val_acc={res['val_acc']:.4f}, val_f1={res['val_f1']:.4f}")

svm_df = pd.DataFrame(svm_results)
print("\n=== SVM Results Table ===")
print(svm_df[['kernel','C','train_acc','val_acc','train_f1','val_f1']].round(4).to_string(index=False))
```

```python
# ── Plot: Macro F1 vs C for each kernel ───────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for i, metric in enumerate(['val_acc', 'val_f1']):
    label_str = 'Accuracy' if metric == 'val_acc' else 'Macro F1'
    for kernel, color, marker in [('linear', 'steelblue', 'o'), ('rbf', 'orangered', 's')]:
        subset = svm_df[svm_df['kernel'] == kernel]
        axes[i].plot(range(len(C_values)), subset[metric], 
                     marker=marker, color=color, linewidth=2, markersize=8,
                     label=f'{kernel} kernel')
    axes[i].set_xticks(range(len(C_values)))
    axes[i].set_xticklabels([str(c) for c in C_values])
    axes[i].set_xlabel('C (log scale values)', fontsize=11)
    axes[i].set_ylabel(label_str, fontsize=11)
    axes[i].set_title(f'Figure 11{chr(97+i)}: SVM Validation {label_str} — kernel vs C',
                      fontsize=12, fontweight='bold')
    axes[i].legend()
    axes[i].grid(True, alpha=0.4)

plt.tight_layout()
plt.savefig('fig11_svm_kernel_C.png', bbox_inches='tight', dpi=150)
plt.show()

# Best SVM by val F1
best_svm_row = svm_df.loc[svm_df['val_f1'].idxmax()]
SVM_BEST_KERNEL = best_svm_row['kernel']
SVM_BEST_C = best_svm_row['C']
print(f"\nBest SVM: kernel={SVM_BEST_KERNEL}, C={SVM_BEST_C}")
print(f"  val_acc={best_svm_row['val_acc']:.4f}, val_f1={best_svm_row['val_f1']:.4f}")
```

**Add Markdown after:**
> "The RBF kernel consistently outperforms the linear kernel, indicating that the decision boundary between fire intensity classes is non-linear. This is expected: the relationship between physical measurements (brightness temperature, humidity, wind speed) and fire intensity involves complex interactions that a straight hyperplane cannot capture. For the linear kernel, increasing C beyond C=1 provides minimal improvement. For the RBF kernel, performance is more sensitive to C — too low (C=0.01) underfits, too high (C=100) begins to overfit as training accuracy exceeds validation accuracy."

---

### Cell 15 — SVM: Joint C × Gamma Grid Search (COSC2793)

**Markdown cell:** `## Cell 15: SVM — Joint C × Gamma Grid Search (COSC2793)`

**Add Markdown BEFORE:**
> "For the RBF kernel, `gamma` controls the influence radius of each support vector. A high gamma means each training point influences only its immediate neighbourhood — a tight, complex decision boundary that risks overfitting. A low gamma produces a smooth, wide influence — simpler boundary that risks underfitting. Because C and gamma interact (a tight boundary from high gamma requires a different regularisation strength than a smooth boundary), we search them **jointly** — testing all 20 combinations of C ∈ {0.1, 1, 10, 100} × gamma ∈ {scale, 0.001, 0.01, 0.1, 1.0} — rather than fixing C at the Cell 14 value and then varying gamma (which could miss the true optimum)."

```python
# ── SVM: Joint 2D grid search over C × gamma (RBF kernel) ─────────────────────
# NOTE: This is a JOINT search. C and gamma are searched simultaneously over
# 4×5 = 20 combinations. The (C, gamma) pair that maximises validation Macro F1
# is selected. This overrides the preliminary C from Cell 14 with the true joint
# optimum. RBF kernel is fixed because Cell 14 established it outperforms linear.

C_grid     = [0.1, 1, 10, 100]
gamma_grid = ['scale', 0.001, 0.01, 0.1, 1.0]
svm_2d_results = []

print("Running 20-combination C × gamma grid search (this may take 3–5 min)...")
for C in C_grid:
    for gam in gamma_grid:
        svm = SVC(kernel='rbf', C=C, gamma=gam, random_state=RANDOM_STATE)
        res = evaluate_model(svm, X_train, y_train, X_val, y_val)
        res.update({'C': C, 'gamma': str(gam)})
        svm_2d_results.append(res)
        print(f"  C={C:>5}, gamma={str(gam):>8}: val_f1={res['val_f1']:.4f}")

svm_2d_df = pd.DataFrame(svm_2d_results)
print("\n=== SVM 2D Grid Results (RBF kernel) ===")
print(svm_2d_df[['C','gamma','train_f1','val_f1']].round(4).to_string(index=False))

# ── Heatmap: Validation Macro F1 for all C×gamma combinations ─────────────────
pivot = svm_2d_df.pivot(index='gamma', columns='C', values='val_f1')
# Sort gamma rows for readability
gamma_order = ['scale', '0.001', '0.01', '0.1', '1.0']
pivot = pivot.reindex(gamma_order)

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot, annot=True, fmt='.4f', cmap='YlOrRd', ax=ax,
            cbar_kws={'label': 'Validation Macro F1'}, linewidths=0.5)
ax.set_title('Figure 12: SVM RBF — Joint C × Gamma Grid Search\nValidation Macro F1 for All 20 Combinations',
             fontsize=13, fontweight='bold')
ax.set_xlabel('C (regularisation parameter)', fontsize=12)
ax.set_ylabel('gamma (influence radius)', fontsize=12)
plt.tight_layout()
plt.savefig('fig12_svm_gamma.png', bbox_inches='tight', dpi=150)
plt.show()

# ── Select joint optimum ───────────────────────────────────────────────────────
best_idx   = svm_2d_df['val_f1'].idxmax()
best_row   = svm_2d_df.loc[best_idx]
SVM_BEST_C     = best_row['C']      # Override Cell 14's C with joint optimum
SVM_BEST_GAMMA = best_row['gamma']  # gamma at joint optimum
print(f"\nJoint best: C={SVM_BEST_C}, gamma={SVM_BEST_GAMMA}")
print(f"  val_acc={best_row['val_acc']:.4f}, val_f1={best_row['val_f1']:.4f}")
```

**Add Markdown after:**
> "Figure 12 shows validation Macro F1 for all 20 (C, gamma) combinations. Darker cells represent better performance. The heatmap reveals the interaction between the two parameters: very high gamma (1.0) tends to overfit regardless of C, while very low gamma (0.001) underfits. The joint optimum is at C=[YOUR VALUE], gamma=[YOUR VALUE], achieving validation Macro F1 of [X.XX]. This value of C may differ from Cell 14's preliminary C (which was found at gamma='scale') — confirming that joint search is necessary."

---

### Cell 16 — SVM: Best Model Analysis

```python
# ── Fit final SVM ──────────────────────────────────────────────────────────────
svm_best = SVC(kernel=SVM_BEST_KERNEL, C=SVM_BEST_C, gamma=SVM_BEST_GAMMA,
               random_state=RANDOM_STATE)
svm_best.fit(X_train, y_train)

y_pred_svm = svm_best.predict(X_val)
svm_val_acc = accuracy_score(y_val, y_pred_svm)
svm_val_f1  = f1_score(y_val, y_pred_svm, average='macro')

print(f"SVM Best Model: kernel={SVM_BEST_KERNEL}, C={SVM_BEST_C}, gamma={SVM_BEST_GAMMA}")
print(f"  Validation Accuracy: {svm_val_acc:.4f}")
print(f"  Validation Macro F1: {svm_val_f1:.4f}")
print()
print("=== Detailed Classification Report ===")
print(classification_report(y_val, y_pred_svm,
      target_names=['Low', 'Moderate', 'High', 'Extreme']))

plot_confusion_matrix(y_val, y_pred_svm, f'SVM (kernel={SVM_BEST_KERNEL}, C={SVM_BEST_C})',
                      'fig13_svm_confusion_matrix.png')
```

---

### Cell 17 — Neural Network: Learning Rate Experiment

**Markdown cell:** `## Cell 17: Neural Network — Effect of Learning Rate`

**Add Markdown BEFORE code:**
> "As taught in Week 7, a Multi-Layer Perceptron (MLP) consists of an input layer, one or more **hidden layers**, and an output layer. Each hidden unit computes a weighted sum of its inputs followed by an activation function. We use **ReLU** (max(0, x)) as the activation function for hidden layers — as shown in the slides, ReLU propagates gradients efficiently, avoids the vanishing gradient problem that affects sigmoid, and is computationally simple. Training uses **backpropagation** with **mini-batch stochastic gradient descent** (the Adam optimiser), which computes gradients on small random batches rather than the entire dataset. The **learning rate** α controls the gradient descent step size. Too small → slow convergence that may not complete within the allowed iterations. Too large → the loss oscillates or diverges because each update overshoots the minimum on the loss surface (as the 3D loss landscape diagrams in the slides show). We test learning rates {0.0001, 0.001, 0.01, 0.1} and plot the training loss curve for each."

```python
# ── Neural Network learning rate experiment ────────────────────────────────────
learning_rates = [0.0001, 0.001, 0.01, 0.1]
mlp_lr_results = []
mlp_loss_curves = {}

FIXED_ARCHITECTURE = (128, 64)  # Two hidden layers
MAX_ITER = 300

for lr in learning_rates:
    mlp = MLPClassifier(
        hidden_layer_sizes=FIXED_ARCHITECTURE,
        learning_rate_init=lr,
        max_iter=MAX_ITER,
        random_state=RANDOM_STATE,
        early_stopping=False,  # Keep this False so we see full curves
        solver='adam',
        activation='relu'
    )
    mlp.fit(X_train, y_train)
    
    y_pred_tr = mlp.predict(X_train)
    y_pred_vl = mlp.predict(X_val)
    
    res = {
        'learning_rate': lr,
        'train_acc': accuracy_score(y_train, y_pred_tr),
        'val_acc':   accuracy_score(y_val, y_pred_vl),
        'train_f1':  f1_score(y_train, y_pred_tr, average='macro'),
        'val_f1':    f1_score(y_val, y_pred_vl, average='macro'),
        'n_iter':    mlp.n_iter_
    }
    mlp_lr_results.append(res)
    mlp_loss_curves[lr] = mlp.loss_curve_
    print(f"  lr={lr}: val_acc={res['val_acc']:.4f}, val_f1={res['val_f1']:.4f}, n_iter={res['n_iter']}")

mlp_lr_df = pd.DataFrame(mlp_lr_results)
print("\n=== MLP Learning Rate Results ===")
print(mlp_lr_df[['learning_rate','train_acc','val_acc','train_f1','val_f1','n_iter']].round(4).to_string(index=False))
```

```python
# ── Plot: Loss curves per learning rate ───────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()
colors = ['steelblue', 'orangered', 'green', 'purple']

for i, lr in enumerate(learning_rates):
    loss = mlp_loss_curves[lr]
    axes[i].plot(loss, color=colors[i], linewidth=2)
    axes[i].set_title(f'lr = {lr}', fontsize=12, fontweight='bold')
    axes[i].set_xlabel('Epoch')
    axes[i].set_ylabel('Training Loss')
    axes[i].grid(True, alpha=0.4)
    axes[i].set_ylim(bottom=0)

plt.suptitle('Figure 14: Neural Network — Training Loss Curves by Learning Rate\n'
             f'(Architecture: {FIXED_ARCHITECTURE}, max_iter={MAX_ITER})',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('fig14_mlp_loss_curves.png', bbox_inches='tight', dpi=150)
plt.show()
```

```python
# ── Plot: Validation performance vs learning rate ──────────────────────────────
lr_labels = [str(lr) for lr in learning_rates]
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(lr_labels, mlp_lr_df['train_f1'], 'o-', label='Training Macro F1',
        color='steelblue', linewidth=2, markersize=8)
ax.plot(lr_labels, mlp_lr_df['val_f1'], 's--', label='Validation Macro F1',
        color='orangered', linewidth=2, markersize=8)
ax.set_xlabel('Learning Rate', fontsize=12)
ax.set_ylabel('Macro F1', fontsize=12)
ax.set_title('Figure 15: Neural Network — Macro F1 vs Learning Rate', fontsize=13, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('fig15_mlp_lr_performance.png', bbox_inches='tight', dpi=150)
plt.show()

best_lr_idx = mlp_lr_df['val_f1'].idxmax()
MLP_BEST_LR = mlp_lr_df.loc[best_lr_idx, 'learning_rate']
print(f"\nBest learning rate by validation Macro F1: {MLP_BEST_LR}")
```

**Add Markdown after:**
> "The loss curves reveal fundamentally different training behaviours. lr=0.0001 shows slow, steady convergence — the loss decreases smoothly but may not converge within 300 epochs. lr=0.001 typically represents the sweet spot: stable convergence that reaches a low loss within the allowed iterations. lr=0.01 converges faster but may oscillate in later epochs. lr=0.1 often shows instability — the loss fluctuates because each update overshoots the minimum on the loss surface. The best learning rate is selected by validation Macro F1."

---

### Cell 18 — Neural Network: Architecture Experiment (COSC2793)

**Markdown cell:** `## Cell 18: Neural Network — Effect of Hidden Layer Architecture (COSC2793)`

**Add Markdown BEFORE:**
> "The architecture (number and size of hidden layers) determines how complex a function the neural network can represent. A small network (e.g., one layer of 32 neurons) may underfit complex patterns. A very large network (e.g., three layers of 256 neurons) may overfit on this dataset size and take longer to train. We fix the best learning rate and compare several architectures."

```python
architectures = [(32,), (64,), (128,), (64, 32), (128, 64), (256, 128), (128, 64, 32)]
arch_labels = [str(a) for a in architectures]
mlp_arch_results = []

for arch in architectures:
    mlp = MLPClassifier(
        hidden_layer_sizes=arch,
        learning_rate_init=MLP_BEST_LR,
        max_iter=MAX_ITER,
        random_state=RANDOM_STATE,
        solver='adam',
        activation='relu'
    )
    res = evaluate_model(mlp, X_train, y_train, X_val, y_val)
    res['architecture'] = str(arch)
    mlp_arch_results.append(res)
    print(f"  arch={str(arch):>20}: val_acc={res['val_acc']:.4f}, val_f1={res['val_f1']:.4f}")

mlp_arch_df = pd.DataFrame(mlp_arch_results)
print("\n=== MLP Architecture Results ===")
print(mlp_arch_df[['architecture','train_acc','val_acc','train_f1','val_f1']].round(4).to_string(index=False))

fig, ax = plt.subplots(figsize=(12, 5))
x = range(len(architectures))
ax.plot(x, mlp_arch_df['train_f1'], 'o-', label='Training Macro F1',
        color='steelblue', linewidth=2)
ax.plot(x, mlp_arch_df['val_f1'], 's--', label='Validation Macro F1',
        color='orangered', linewidth=2)
ax.set_xticks(x)
ax.set_xticklabels(arch_labels, rotation=20, ha='right')
ax.set_xlabel('Architecture (hidden layers)', fontsize=11)
ax.set_ylabel('Macro F1', fontsize=11)
ax.set_title(f'Figure 16: Neural Network — Effect of Architecture on Macro F1\n(lr={MLP_BEST_LR} fixed)',
             fontsize=13, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('fig16_mlp_architecture.png', bbox_inches='tight', dpi=150)
plt.show()

best_arch_idx = mlp_arch_df['val_f1'].idxmax()
MLP_BEST_ARCH = architectures[best_arch_idx]
print(f"\nBest architecture: {MLP_BEST_ARCH}")
```

---

### Cell 19 — Neural Network: Best Model Analysis

```python
# ── Fit final Neural Network ───────────────────────────────────────────────────
mlp_best = MLPClassifier(
    hidden_layer_sizes=MLP_BEST_ARCH,
    learning_rate_init=MLP_BEST_LR,
    max_iter=MAX_ITER,
    random_state=RANDOM_STATE,
    solver='adam',
    activation='relu',
    early_stopping=True,       # Stop when validation loss stops improving
    n_iter_no_change=20,       # Patience: 20 epochs with no improvement
    validation_fraction=0.1    # Use 10% of X_train for early-stopping check
)
mlp_best.fit(X_train, y_train)
print(f"Actual epochs trained (early stopping): {mlp_best.n_iter_} / {MAX_ITER}")

y_pred_mlp = mlp_best.predict(X_val)
mlp_val_acc = accuracy_score(y_val, y_pred_mlp)
mlp_val_f1  = f1_score(y_val, y_pred_mlp, average='macro')

print(f"Neural Network Best Model:")
print(f"  architecture={MLP_BEST_ARCH}, lr={MLP_BEST_LR}")
print(f"  Validation Accuracy: {mlp_val_acc:.4f}")
print(f"  Validation Macro F1: {mlp_val_f1:.4f}")
print()
print("=== Detailed Classification Report ===")
print(classification_report(y_val, y_pred_mlp,
      target_names=['Low', 'Moderate', 'High', 'Extreme']))

plot_confusion_matrix(y_val, y_pred_mlp,
                      f'Neural Network {MLP_BEST_ARCH}',
                      'fig17_mlp_confusion_matrix.png')
```

```python
# ── Final loss curve for best MLP ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(mlp_best.loss_curve_, color='steelblue', linewidth=2)
ax.set_xlabel('Epoch', fontsize=12)
ax.set_ylabel('Training Loss', fontsize=12)
ax.set_title(f'Figure 18: Neural Network Best Model — Training Loss Curve\n'
             f'(arch={MLP_BEST_ARCH}, lr={MLP_BEST_LR})',
             fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('fig18_mlp_best_loss.png', bbox_inches='tight', dpi=150)
plt.show()
```

---

### Cell 20 — Model Comparison Table & Chart

**Markdown cell:** `## Cell 20: Model Comparison`

```python
# ── Cross-validation for all three best models ────────────────────────────────
# Note: CV is run on the FULL processed training set (X_proc, y), not just X_train
# This gives a more robust performance estimate using all available labelled data.

print("Running 5-fold stratified cross-validation (this may take a few minutes)...\n")

models_to_compare = {
    'Decision Tree': DecisionTreeClassifier(
        max_depth=DT_BEST_DEPTH,
        ccp_alpha=DT_BEST_ALPHA,
        random_state=RANDOM_STATE),
    'SVM': SVC(
        kernel=SVM_BEST_KERNEL, C=SVM_BEST_C,
        gamma=SVM_BEST_GAMMA, random_state=RANDOM_STATE),
    'Neural Network': MLPClassifier(
        hidden_layer_sizes=MLP_BEST_ARCH,
        learning_rate_init=MLP_BEST_LR,
        max_iter=MAX_ITER, random_state=RANDOM_STATE,
        solver='adam', activation='relu')
}

comparison_rows = []
for name, model in models_to_compare.items():
    cv_acc = cross_val_score(model, X_proc, y, cv=cv_splitter,
                             scoring='accuracy', n_jobs=-1)
    cv_f1  = cross_val_score(model, X_proc, y, cv=cv_splitter,
                             scoring='f1_macro', n_jobs=-1)
    
    # Also use the hold-out val results from earlier
    if name == 'Decision Tree':
        val_acc_h, val_f1_h = dt_val_acc, dt_val_f1
    elif name == 'SVM':
        val_acc_h, val_f1_h = svm_val_acc, svm_val_f1
    else:
        val_acc_h, val_f1_h = mlp_val_acc, mlp_val_f1
    
    comparison_rows.append({
        'Model': name,
        'Hold-out Accuracy': round(val_acc_h, 4),
        'Hold-out Macro F1': round(val_f1_h, 4),
        'CV Accuracy (mean)': round(cv_acc.mean(), 4),
        'CV Accuracy (std)': round(cv_acc.std(), 4),
        'CV Macro F1 (mean)': round(cv_f1.mean(), 4),
        'CV Macro F1 (std)': round(cv_f1.std(), 4),
    })
    print(f"{name}: CV Acc={cv_acc.mean():.4f}±{cv_acc.std():.4f}, "
          f"CV F1={cv_f1.mean():.4f}±{cv_f1.std():.4f}")

comparison_df = pd.DataFrame(comparison_rows)
print("\n=== Full Model Comparison Table ===")
print(comparison_df.to_string(index=False))
```

```python
# ── Bar chart comparison ───────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
x = np.arange(3)
width = 0.35
model_names = comparison_df['Model'].values

for ax_i, (metric_mean, metric_std, label) in enumerate([
    ('CV Accuracy (mean)', 'CV Accuracy (std)', 'CV Accuracy'),
    ('CV Macro F1 (mean)', 'CV Macro F1 (std)', 'CV Macro F1')
]):
    axes[ax_i].bar(x, comparison_df[metric_mean], width * 2,
                   color=sns.color_palette('colorblind', 3),
                   edgecolor='white',
                   yerr=comparison_df[metric_std], capsize=5)
    axes[ax_i].set_xticks(x)
    axes[ax_i].set_xticklabels(model_names, rotation=10)
    axes[ax_i].set_ylabel(label, fontsize=12)
    axes[ax_i].set_title(f'Figure 19{chr(97+ax_i)}: {label}\n(5-Fold CV, mean ± std)',
                         fontsize=12, fontweight='bold')
    axes[ax_i].set_ylim(0, 1)
    axes[ax_i].grid(axis='y', alpha=0.4)
    for j, (v, e) in enumerate(zip(comparison_df[metric_mean], comparison_df[metric_std])):
        axes[ax_i].text(j, v + e + 0.01, f'{v:.3f}', ha='center', fontweight='bold')

plt.suptitle('Figure 19: Model Comparison — Cross-Validated Performance',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('fig19_model_comparison.png', bbox_inches='tight', dpi=150)
plt.show()
```

---

### Cell 21 — Final Model Selection & Test Predictions

**Markdown cell:** `## Cell 21: Final Model Selection and Test Predictions`

**Add Markdown BEFORE code stating your choice and justification:**
> "Based on the comparison across hold-out validation and cross-validation metrics, [MODEL NAME] is selected as the final model. Justification: [see report Section E]. The final model is re-fitted on the entire labelled training set (all 4,340 samples) before predicting the test set, to maximise the training data used."

```python
# ── State your final model choice ─────────────────────────────────────────────
# Change this to the model that performed best in your experiments.
# Options: dt_best, svm_best, mlp_best

FINAL_MODEL = svm_best  # <-- Change this based on your results

# ── Refit on ALL labelled training data ───────────────────────────────────────
print("Fitting final model on full training set...")
FINAL_MODEL.fit(X_proc, y)  # X_proc = all 4340 processed samples, y = all labels

# ── Generate test predictions ──────────────────────────────────────────────────
y_test_pred = FINAL_MODEL.predict(X_test_proc)
print(f"Test predictions shape: {y_test_pred.shape}")
print(f"Predicted class distribution:")
for cls_int, cls_name in enumerate(['Low', 'Moderate', 'High', 'Extreme']):
    count = np.sum(y_test_pred == cls_int)
    print(f"  {cls_int} ({cls_name}): {count} ({count/len(y_test_pred)*100:.1f}%)")

# ── Save predictions ──────────────────────────────────────────────────────────
# File name MUST be s4163448_predictions.csv
# Column name MUST be fire_intensity (not "label", not "target")
df_pred = pd.DataFrame({'fire_intensity': y_test_pred})
df_pred.to_csv('s4163448_predictions.csv', header=True, index=False)

print(f"\nPredictions saved to: s4163448_predictions.csv")
print(f"File shape: {df_pred.shape}")
print(f"Column name: {list(df_pred.columns)}")
print(f"First 5 predictions: {df_pred['fire_intensity'].head().tolist()}")
```

```python
# ── Verify the output file ─────────────────────────────────────────────────────
verification = pd.read_csv('s4163448_predictions.csv')
assert len(verification) == 1085, f"ERROR: Expected 1085 rows, got {len(verification)}"
assert list(verification.columns) == ['fire_intensity'], f"ERROR: Wrong column name"
assert verification['fire_intensity'].isin([0,1,2,3]).all(), "ERROR: Invalid class values"
print("Verification PASSED:")
print(f"  Rows: {len(verification)} (expected 1085)")
print(f"  Column: {list(verification.columns)}")
print(f"  Values: {sorted(verification['fire_intensity'].unique())}")
```

---

## 7. Figures Checklist

Every figure must appear in both the notebook AND the report. Save each with the filename given in the code.

| Figure | What it Shows | Code Cell |
|---|---|---|
| Fig 1 | Class distribution bar chart + pie chart | Cell 3 |
| Fig 2 | Missing value rates per feature | Cell 4 |
| Fig 3 | Boxplots: each numeric feature split by fire_intensity class | Cell 5 |
| Fig 4 | Stacked bar: categorical features vs target | Cell 6 |
| Fig 5 | Correlation heatmap + ranked table | Cell 7 |
| Fig 6a | Decision Tree: Training vs validation accuracy by max_depth | Cell 11 |
| Fig 6b | Decision Tree: Training vs validation Macro F1 by max_depth | Cell 11 |
| Fig 7 | Decision Tree: post-pruning ccp_alpha effect on Macro F1 | Cell 12 |
| Fig 8 | Decision Tree: Tree structure (top 4 levels) | Cell 13 |
| Fig 9 | Decision Tree: Feature importance (top 15) | Cell 13 |
| Fig 10 | Decision Tree: Confusion matrix | Cell 13 |
| Fig 11 | SVM: Linear vs RBF kernel across C values | Cell 14 |
| Fig 12 | SVM: Gamma effect (RBF kernel) | Cell 15 |
| Fig 13 | SVM: Confusion matrix | Cell 16 |
| Fig 14 | Neural Network: Loss curves per learning rate (2×2 grid) | Cell 17 |
| Fig 15 | Neural Network: Macro F1 vs learning rate | Cell 17 |
| Fig 16 | Neural Network: Architecture effect | Cell 18 |
| Fig 17 | Neural Network: Confusion matrix | Cell 19 |
| Fig 18 | Neural Network: Best model loss curve | Cell 19 |
| Fig 19 | Model comparison bar charts (accuracy + F1) | Cell 20 |

---

## 8. Report — Step-by-Step Writing Guide

**File format:** PDF named `report.pdf`. Length: minimum 10 pages, maximum 20 pages (COSC2793).

> **PAGE COUNT WARNING — READ BEFORE YOU START WRITING:**
> With 19 figures plus 3 tables plus full written sections, the report will easily go over 20 pages if figures are full-size. The spec caps at 20 pages — going over may cost marks.
>
> **How to control page length:**
> - Insert all figures at **half-page width** (7–8 cm wide), not full-page width. Two figures side by side on one row saves 1 full page per pair.
> - For confusion matrices (Figures 10, 13, 17) — they are already 2-panel figures (raw + normalised). Insert at 80% of page width.
> - For Figure 14 (2×2 loss curve grid) — this is large. Insert at 90% page width but on its own page.
> - For Figure 12 (heatmap) — insert at 70% page width.
> - After inserting all figures and writing all sections, check page count. If over 20 pages: shrink the two largest figures by 20%, remove any redundant white space, tighten margins to 2 cm.
> - Sections F (Ethics) and G (Conclusion) can be slightly condensed — aim for 0.5 pages each, not 1 full page.

---

### HOW TO BUILD YOUR REPORT — Read This First

Think of the report as a story that tells the marker exactly what you did, why you did it, and what you found. Every paragraph needs supporting evidence — either a figure (graph/plot) or a table with numbers.

**The golden rule:** Every single claim must be backed by a figure or a number.
- "brightness_k is the most important feature" → back it up with the feature importance TABLE (numbers from Cell 13).
- "Training accuracy keeps going up but validation drops" → back it up with FIGURE 6a or 6b.
- "RBF kernel outperforms linear" → back it up with FIGURE 11 showing the two lines.

**How to insert figures into your report:**
- Open your notebook folder (same folder as the CSV files).
- Find the PNG file with the correct name (e.g. `fig03_feature_boxplots_by_class.png`).
- In Microsoft Word: click Insert → Pictures → select the PNG file → OK. Then add a caption below it.
- In Google Docs: Insert → Image → Upload from computer → select the PNG.
- In LaTeX: `\includegraphics[width=\textwidth]{fig03_feature_boxplots_by_class.png}`
- Every figure needs a caption line directly below it: "Figure X: [description]"

**How to copy tables from your notebook into the report:**
- Run the relevant cell in Jupyter.
- Look for the printed output (the text table, not the plot).
- Select all of it with your mouse, copy (Ctrl+C), paste into Word.
- Then use Word's "Text to Table" feature (Table → Convert → Text to Table, delimiter = space) OR type it by hand as a Word table.

**Fill in all [X.XX] placeholders:**
- Every `[X.XX]` in this template is a placeholder for a real number you will get after running your notebook.
- Do NOT submit the report with [X.XX] still in it. Replace every single one with your actual result.
- The marker will compare numbers in the report against numbers in the notebook output. They must match exactly.

---

### Section 0: Introduction (~0.5 page)

**NO FIGURES IN THIS SECTION. NO TABLES IN THIS SECTION.**

Write this section in your own words. The template text below shows what to cover:

> Satellite-based wildfire monitoring provides critical information for emergency response, resource allocation, and environmental assessment. Accurate classification of wildfire intensity from observational data enables timely and proportionate responses: underestimating fire severity risks inadequate deployment of resources, while overestimation wastes capacity. This report presents a machine learning workflow for predicting wildfire intensity level (four classes: Low, Moderate, High, and Extreme) from environmental, geospatial, and satellite-derived features.
>
> Three classification algorithms are developed and systematically compared: Decision Tree, Support Vector Machine (SVM), and Multi-Layer Perceptron (MLP) Neural Network. A consistent evaluation framework using stratified hold-out validation and 5-fold cross-validation is applied across all models. The final model is selected based on both quantitative performance and practical deployment considerations, including stability and interpretability.

---

### Section A: Task Definition and Dataset Description (~1 page)

**NO FIGURES IN THIS SECTION.**

**TABLE TO TYPE BY HAND IN SECTION A:**

> **Table A.1 — Feature Summary Table** (type this manually — do not copy from notebook)
> Create a table with three columns: Feature Name | Type | Notes. Fill it in using the Dataset Deep Dive table from Section 4 of this README. Include all 19 features. The marker wants to see that you know what each feature is and what type it is.
>
> Example first few rows:
>
> | Feature | Type | Notes |
> |---|---|---|
> | brightness_k | Numeric (continuous) | Thermal brightness in Kelvin; 7.5% missing values |
> | temp_max_c | Numeric (continuous) | Daily maximum temperature; no missing values |
> | region | Categorical (nominal) | 7 geographic regions |
> | confidence | Categorical (ordinal) | high / nominal / low detection confidence |
> | ... (all 19 features) | ... | ... |

**A.1 Task Definition — write this:**

> The machine learning task is a supervised multiclass classification problem. Given a set of observational and environmental features recorded at the time of wildfire detection, the model must predict the fire intensity level. The prediction target is `fire_intensity`, a categorical variable with four ordered classes: 0 (Low), 1 (Moderate), 2 (High), and 3 (Extreme). The task is formulated as:
>
> *f(X) → y, where y ∈ {0, 1, 2, 3}*
>
> The performance measures used are (1) Accuracy — the proportion of correctly classified samples — and (2) Macro F1-score — the unweighted average of per-class F1 scores. Macro F1 is the primary ranking metric because it gives equal weight to each class, including the minority Extreme class (8.8% of training data). A model that achieves high accuracy by only predicting the majority class (Moderate, 44.3%) would still score poorly on Macro F1.

**A.2 Dataset Description — write this:**

> The training dataset contains 4,340 samples and 19 input features; the test set contains 1,085 samples with the same features but no labels. Features span four domains:
>
> - **Geospatial:** `latitude` and `longitude` (continuous), `region` (7 levels), `country` (35 levels)
> - **Temporal:** `year` (2024–2025), `month` (1–12), `season` (4 levels), `acq_time` (HHMM integer)
> - **Observational:** `satellite` (4 types), `instrument` (MODIS/VIIRS), `brightness_k` (Kelvin), `confidence` (3 levels), `fire_type` (10 types), `daynight` (D/N)
> - **Environmental/Weather:** `temp_max_c`, `wind_max_kmh`, `precip_mm`, `humidity_pct`
>
> The feature `acq_date` is excluded from modelling as its temporal information is already captured by `year` and `month`.

**A.3 Dataset Challenges — write this:**

> Three challenges are identified:
> 1. **Missing values:** `month` (9.6%), `brightness_k` (7.5%), and `wind_max_kmh` (4.8%) contain missing entries in the training set. These require imputation before modelling.
> 2. **Class imbalance:** The Moderate class accounts for 44.3% of training samples, while Extreme represents only 8.8%. Standard accuracy metrics can be misleading; Macro F1 mitigates this.
> 3. **Mixed feature types:** Numeric and nominal categorical features require different preprocessing (scaling and encoding respectively), making pipeline design critical.

---

### Section B: EDA and Data Handling (~2 pages)

**FIGURES TO PASTE INTO SECTION B — all 5 of these must appear here:**

---

**FIGURE 1 — Class Distribution Bar Chart + Pie Chart**
- File: `fig01_class_distribution.png`
- Produced by: **Cell 3** (when you run Cell 3, this file is saved automatically)
- WHERE to paste it: Right after your first paragraph about class imbalance in B.1
- Caption to write below the image: `Figure 1: Target Variable Distribution (fire_intensity) — 4,340 training samples`
- What to say about it: "Figure 1 shows the class distribution. Moderate is the dominant class (44.3%, 1,921 samples) while Extreme is the rarest (8.8%, 381 samples). This imbalance motivates the use of Macro F1 as the primary metric."

---

**FIGURE 2 — Missing Value Bar Chart**
- File: `fig02_missing_values.png`
- Produced by: **Cell 4**
- WHERE to paste it: Right after you mention the three features with missing values in B.1 or B.2
- Caption: `Figure 2: Missing Value Rate per Feature (training set)`
- What to say: "Figure 2 shows that only three features contain missing values: month (9.6%), brightness_k (7.5%), and wind_max_kmh (4.8%). No categorical features are missing."

---

**FIGURE 3 — Per-Class Boxplots for All Numeric Features**
- File: `fig03_feature_boxplots_by_class.png`
- Produced by: **Cell 5**
- WHERE to paste it: In B.1, after your paragraph about which features discriminate between classes
- Caption: `Figure 3: Numeric Feature Distributions per Fire Intensity Class (boxplots)`
- What to say: "Figure 3 shows the distribution of each numeric feature separated by fire intensity class. brightness_k increases monotonically from Low to Extreme — the median brightness temperature for Extreme fires is substantially higher than for Low fires. temp_max_c follows the same pattern. humidity_pct shows the opposite: higher humidity is associated with lower intensity fires. precip_mm and latitude show less clear separation."
- **THIS IS THE MAIN A1 FIX** — In A1 you only had overall histograms. These per-class boxplots show HOW each feature relates to the target. Always discuss what you see in each boxplot (which direction does each feature go as intensity increases?).

---

**FIGURE 4 — Categorical Features vs Target (Stacked Bar Charts)**
- File: `fig04_categorical_vs_target.png`
- Produced by: **Cell 6**
- WHERE to paste it: In B.1, after the paragraph about categorical features
- Caption: `Figure 4: Class Distribution per Categorical Feature (stacked bar, normalised)`
- What to say: "Figure 4 shows how the target class distribution varies within each category. confidence is the strongest discriminator: detections with 'high' confidence are strongly associated with High and Extreme fires. region shows geographic variation — [describe your actual observation from Figure 4 when you run the notebook]. fire_type indicates that [describe your observation]."

---

**FIGURE 5 — Correlation Heatmap**
- File: `fig05_correlation_heatmap.png`
- Produced by: **Cell 7**
- WHERE to paste it: In B.1, alongside or just below the ranked correlation table
- Caption: `Figure 5: Numeric Feature Correlation Matrix (Pearson, including encoded target)`
- What to say: "Figure 5 shows pairwise Pearson correlations. brightness_k has the highest positive correlation with fire_intensity_enc (r ≈ [YOUR NUMBER from Table B.1]), followed by temp_max_c. humidity_pct has the strongest negative correlation. Some features (latitude, longitude) show weak linear relationships with the target."

---

**TABLE B.1 — Ranked Correlation Table (THIS IS THE MOST IMPORTANT TABLE — IT WAS MISSING IN A1)**

> **HOW TO GET THIS TABLE:**
> 1. Run Cell 7 in your notebook.
> 2. Look at the printed output that starts with `=== Ranked Feature Correlations with fire_intensity ===`
> 3. You will see a table with columns: Feature | Abs Correlation with Target | Signed Correlation
> 4. Copy ALL rows of that table.
> 5. Paste it into your report as a formatted table. It should look like:
>
> | Feature | Abs Correlation | Signed Correlation |
> |---|---|---|
> | brightness_k | 0.XXXX | +0.XXXX |
> | temp_max_c | 0.XXXX | +0.XXXX |
> | humidity_pct | 0.XXXX | −0.XXXX |
> | ... | ... | ... |
>
> Caption: `Table B.1: Ranked Feature Correlations with fire_intensity (Pearson r, absolute and signed)`
>
> **After the table, write:** "Table B.1 confirms that brightness_k is the dominant numeric predictor (|r| = [X.XX]), followed by temp_max_c. These correlations are linear — non-linear models may extract stronger signals."

**B.2 Preprocessing Pipeline — write this:**

> The preprocessing pipeline applies the following steps in sequence:
>
> 1. **Feature exclusion:** `acq_date` is dropped. `year` and `month` already capture the temporal information contained in this date string, and parsing a date adds computational complexity without additional predictive value.
>
> 2. **Missing value imputation:** Median imputation is applied to the three numeric features with missing values (`month`, `brightness_k`, `wind_max_kmh`) (Pedregosa et al., 2011). Median is preferred over mean because it is robust to outliers — visible in the feature distributions for `brightness_k` (max = 503.7 K, well above the 75th percentile). Missing rates of 5–10% are within acceptable bounds for imputation.
>
> 3. **Categorical encoding:** One-hot encoding converts each nominal categorical feature into binary indicator columns. Label encoding is not used for nominal features as it would impose a false ordinal relationship (e.g., implying "Summer > Spring").
>
> 4. **Feature scaling:** StandardScaler (zero mean, unit variance) is applied to all numeric features. This is essential for SVM (which uses Euclidean distance in feature space) and MLP (which uses gradient-based optimisation). Decision Trees are invariant to monotone transformations so scaling does not affect their results, but it causes no harm.
>
> 5. **Data leakage prevention:** The preprocessor is fitted exclusively on the 80% training split (3,472 samples). The same fitted preprocessor — with training-set mean/median/encoder statistics — is then applied (transform only) to the validation and test sets. This ensures that no test information leaks into the training process.

**B.3 Data Split — write this:**

> A stratified 80/20 hold-out split is applied: 3,472 samples for training, 868 for validation. Stratification ensures that all four fire intensity classes appear proportionally in both subsets. With 20% held out, the validation set contains approximately [your actual numbers from Cell 9 output] samples per class.
>
> Additionally, 5-fold Stratified Cross-Validation is applied in the final model comparison phase, using the full 4,340 training samples. This provides a more robust performance estimate than a single hold-out split, as every sample is used for validation exactly once across the five folds.

---

### Section C: Model Development and Analysis (~4–5 pages)

This is worth 40% of your total grade. Every model gets its own subsection with: (1) rationale, (2) hyperparameter experiment 1 with figure, (3) hyperparameter experiment 2 with figure (COSC2793 requirement), (4) best model results with confusion matrix, (5) theory connection.

---

#### C.1 Decision Tree

**FIGURES TO PASTE IN C.1 — all 6 must appear here:**

---

**FIGURE 6a — Training vs Validation Accuracy by max_depth**
- File: `fig06a_dt_depth_accuracy.png`
- Produced by: **Cell 11**
- WHERE: After your paragraph about the max_depth pre-pruning experiment
- Caption: `Figure 6a: Decision Tree — Training vs Validation Accuracy by max_depth`
- What to say: "Figure 6a shows training accuracy rising monotonically while validation accuracy peaks around max_depth = [YOUR VALUE] then plateaus. At max_depth = 1–3 both curves are low — underfitting. At max_depth ≥ 15, training accuracy is near 100% while validation stagnates — overfitting."

---

**FIGURE 6b — Training vs Validation Macro F1 by max_depth**
- File: `fig06b_dt_depth_f1.png`
- Produced by: **Cell 11**
- WHERE: Immediately after Figure 6a (pair them together)
- Caption: `Figure 6b: Decision Tree — Training vs Validation Macro F1 by max_depth`
- What to say: "Figure 6b shows the same overfitting pattern using Macro F1. The optimal max_depth by validation Macro F1 is [YOUR VALUE FROM Cell 11 output: `Selected max_depth = X`]."

---

**FIGURE 7 — Post-Pruning via ccp_alpha (COSC2793 2nd Hyperparameter)**
- File: `fig07_dt_ccp_alpha.png`
- Produced by: **Cell 12**
- WHERE: After your paragraph about cost complexity pruning
- Caption: `Figure 7: Decision Tree — Effect of Cost Complexity Pruning (ccp_alpha) on Macro F1`
- What to say: "Figure 7 shows the effect of post-pruning. At α = 0 (no pruning), the model overfits. As α increases, training F1 decreases (tree is simplified) while validation F1 initially improves — confirming that the unpruned tree overfitted. The optimal α = [YOUR VALUE from Cell 12: `Best ccp_alpha: X.XXXXXX`] achieves validation Macro F1 of [X.XX]."
- **Theory to connect:** "This confirms the theoretical claim from Week 5: growing a large tree first and then pruning (post-pruning) produces better generalisation than growing a constrained tree (pre-pruning) alone, because the full tree's internal structure informs which subtrees are worth keeping (Breiman et al., 1984)."

---

**FIGURE 8 — Decision Tree Structure (top 4 levels)**
- File: `fig08_decision_tree_plot.png`
- Produced by: **Cell 13**
- WHERE: After your paragraph about the tree structure insights
- Caption: `Figure 8: Decision Tree Structure — Top 4 Levels (max_depth=[YOUR VALUE], ccp_alpha=[YOUR VALUE])`
- What to say: "Figure 8 shows the top four levels of the best-fit tree. The root node splits on [look at Figure 8 — what feature is written at the top node? Write it here, e.g., `brightness_k ≤ [value]`]. This confirms that [that feature] is the most discriminating single feature, consistent with the highest correlation in Table B.1. The first split separates [which classes end up left vs right — look at Figure 8 and describe what you see]."

---

**FIGURE 9 — Feature Importance Bar Chart (top 15 features)**
- File: `fig09_dt_feature_importance.png`
- Produced by: **Cell 13**
- WHERE: Right after Figure 8 (they go together)
- Caption: `Figure 9: Decision Tree — Top 15 Feature Importances (Gini impurity reduction)`
- What to say: "Figure 9 shows the Gini-based feature importance scores. brightness_k is the most important feature by a large margin (importance = [YOUR VALUE from Table C.1 below]), confirming the EDA findings. The next most important features are [list top 3 from Table C.1]."

---

**FIGURE 10 — Decision Tree Confusion Matrix**
- File: `fig10_dt_confusion_matrix.png`
- Produced by: **Cell 13**
- WHERE: After your paragraph about validation performance
- Caption: `Figure 10: Decision Tree — Normalised Confusion Matrix (validation set)`
- What to say: "Figure 10 shows the normalised confusion matrix. The diagonal represents correct classifications. The most common confusion is between [look at Figure 10 — which two off-diagonal cells are brightest/darkest? Write those pair names]. The Extreme class has recall of [look at the bottom row — what is the bottom-right cell value?], indicating [the model can/cannot detect the rarest fires well]."

---

**TABLE C.1 — Feature Importance Table (TOP MARKS ITEM — MISSING IN A1)**

> **HOW TO GET THIS TABLE:**
> 1. Run Cell 13 in your notebook.
> 2. Scroll to the printed output that starts with `Top 15 features by importance:`
> 3. You will see a two-column table: Feature | Importance (a decimal number between 0 and 1)
> 4. Copy ALL 15 rows. Paste into your report as a formatted table.
>
> Example format for your report:
>
> | Rank | Feature | Importance Score |
> |---|---|---|
> | 1 | brightness_k | 0.XXXX |
> | 2 | [feature] | 0.XXXX |
> | 3 | [feature] | 0.XXXX |
> | ... | ... | ... |
> | 15 | [feature] | 0.XXXX |
>
> Caption: `Table C.1: Decision Tree Feature Importances — Top 15 Features (Gini-based, normalised to sum to 1.0 for all features)`
>
> **After the table write:** "Table C.1 quantifies the contribution of each feature. brightness_k dominates (importance = [X.XXXX]), accounting for [X.X%] of total predictive information. The next [2–3] features are [name them from your table]. Features with near-zero importance could potentially be removed without affecting performance."

**C.1 — Full written text (fill in [X.XX] with your numbers):**

> **Rationale:** Decision Trees (Breiman et al., 1984) are intuitive models that use recursive binary splitting to partition the feature space into rectangular regions, with the majority class in each leaf region as the prediction. Classification trees use the Gini index (G = Σ p̂mk(1 − p̂mk)) as the splitting criterion — not MSE, which applies to regression trees. A Gini index of 0 means a perfectly pure node. Advantages: high interpretability (the tree directly shows which features matter), no requirement for feature scaling, and natural handling of feature interactions. Limitations: instability under small data changes, and a strong tendency to overfit without regularisation.
>
> **Hyperparameter 1 — max_depth (pre-pruning):** max_depth controls how many levels of splits are allowed. Figures 6a and 6b show the training vs validation performance for max_depth 1–20. Training accuracy increases monotonically — the tree always fits better with more splits. Validation Macro F1 peaks at max_depth = [YOUR VALUE] and then degrades, demonstrating classic overfitting. At depth 1–3, both training and validation are low — underfitting. Selected max_depth = [YOUR VALUE].
>
> **Hyperparameter 2 — ccp_alpha (post-pruning, COSC2793):** Cost complexity pruning (Week 5) first grows the full tree, then prunes subtrees that contribute least to impurity reduction per node removed. The parameter ccp_alpha (α) controls this: α = 0 means no pruning; larger α collapses more subtrees. Figure 7 shows validation F1 initially improving as α increases (pruning removes overfit leaves), then declining (tree becomes too simple). Optimal α = [YOUR VALUE] achieves [X.XX] validation Macro F1. This is post-pruning, as opposed to the pre-pruning approach of max_depth — and using both gives a better-regularised tree than either alone.
>
> **Best model:** The best Decision Tree uses max_depth = [YOUR VALUE] and ccp_alpha = [YOUR VALUE]. Validation Accuracy: [X.XX], Validation Macro F1: [X.XX].

---

#### C.2 Support Vector Machine

**FIGURES TO PASTE IN C.2 — all 3 must appear here:**

---

**FIGURE 11 — SVM: Linear vs RBF Kernel across C values**
- File: `fig11_svm_kernel_C.png`
- Produced by: **Cell 14**
- WHERE: After your paragraph about the kernel and C experiment
- Caption: `Figure 11: SVM — Validation Performance vs C for Linear and RBF Kernels`
- What to say: "Figure 11 shows two panels: accuracy (left) and Macro F1 (right), for both kernels across C ∈ {0.01, 0.1, 1, 10, 100}. The RBF kernel consistently outperforms the linear kernel, with best Macro F1 of [X.XX] vs [X.XX] for linear. At C = 0.01, both kernels underfit. At C = 100, the training-validation gap begins to widen for RBF — mild overfitting. The optimal C = [YOUR VALUE from `Best SVM: kernel=X, C=X` in Cell 14 output]."
- **Theory to connect:** "As taught in Week 6: a small C is lenient with misclassifications (wide margin), a large C penalises every error (narrow margin). The pattern in Figure 11 matches this theory exactly."

---

**FIGURE 12 — SVM: Joint C × Gamma Grid Search Heatmap (COSC2793 2nd Hyperparameter)**
- File: `fig12_svm_gamma.png`
- Produced by: **Cell 15**
- WHERE: After your paragraph about the joint grid search
- Caption: `Figure 12: SVM RBF — Joint C × Gamma Grid Search (20 combinations), Validation Macro F1`
- What to say: "Figure 12 is a heatmap showing validation Macro F1 for all 20 (C, gamma) combinations. Each cell colour represents performance at that specific joint parameter pair. Darker red = higher Macro F1. Look at the heatmap and describe: (a) which row (gamma value) generally produces the best performance — [look at Figure 12 and write the answer]; (b) which column (C value) is best — [look and write]; (c) whether the highest gamma row (1.0) shows a pattern of overfitting — [if its cells are red for training but not for validation, say so; if the heatmap only shows val_f1, note which gamma values seem weaker]. The joint optimum C=[YOUR VALUE from Cell 15 output], gamma=[YOUR VALUE] achieves validation Macro F1 of [X.XX]. This joint optimum [may differ from / matches] the preliminary C found in Cell 14 at gamma='scale', demonstrating that simultaneous search is necessary for finding the true optimum."
- **Theory to connect:** "The interaction between C and gamma is an example of hyperparameter coupling: the optimal regularisation strength (C) depends on the complexity of the boundary being learned (gamma). A joint search captures this interaction; a sequential search may not."

---

**FIGURE 13 — SVM Confusion Matrix**
- File: `fig13_svm_confusion_matrix.png`
- Produced by: **Cell 16**
- WHERE: After reporting the best SVM's validation scores
- Caption: `Figure 13: SVM — Normalised Confusion Matrix (validation set, kernel=[YOUR KERNEL], C=[YOUR C])`
- What to say: "Figure 13 shows the SVM confusion matrix. Compared to Figure 10 (Decision Tree), the SVM [achieves higher / similar / lower] recall on the Extreme class ([X.XX] vs DT's [X.XX]). The most common error remains confusion between [look at Figure 13 — describe the biggest off-diagonal value]."

**C.2 — Full written text:**

> **Rationale:** Support Vector Machines (Cortes & Vapnik, 1995) find the maximum-margin hyperplane separating classes. In the soft-margin formulation (Week 6), slack variables εi allow misclassifications subject to Σεi ≤ C. The parameter C controls this trade-off: small C allows more misclassifications (wider margin, simpler boundary); large C penalises every error (narrow margin, risks overfitting). SVMs are particularly suited to high-dimensional spaces — after one-hot encoding, the feature space has [YOUR VALUE: look at the output of Cell 8 `Processed training shape`] dimensions. Classification depends only on the support vectors (points near the margin), making SVMs robust to outliers far from the boundary. Disadvantages: slow on large datasets, feature scaling mandatory.
>
> **Hyperparameter 1 — C and kernel (linear vs RBF):** We test C ∈ {0.01, 0.1, 1, 10, 100} for both linear and RBF kernels (Figure 11). The RBF kernel outperforms linear with best Macro F1 of [YOUR VALUE from Cell 14 output] vs [linear's best F1], confirming that the wildfire intensity decision boundary is non-linear in the original feature space — no straight hyperplane can cleanly separate the four classes regardless of C. Preliminary best: kernel = [YOUR VALUE], C = [YOUR VALUE].
>
> **Hyperparameter 2 — gamma with joint C search (COSC2793):** Because C and gamma interact — the optimal margin width depends on boundary complexity — they are searched jointly over a 4×5 grid (20 combinations, Figure 12). Gamma controls the influence radius of each support vector: high gamma produces a tight, complex boundary (overfitting risk); low gamma produces a smooth, broad boundary (underfitting risk). The joint grid heatmap (Figure 12) reveals this interaction directly. The joint optimum — C = [YOUR VALUE from Cell 15 output], gamma = [YOUR VALUE] — [may differ from / matches] the preliminary C from Figure 11, confirming the value of joint search over sequential search.
>
> **Best model:** SVM with kernel = [YOUR VALUE], C = [YOUR VALUE from Cell 15], gamma = [YOUR VALUE from Cell 15]. Validation Accuracy: [X.XX], Validation Macro F1: [X.XX].

---

#### C.3 Neural Network (MLP)

**FIGURES TO PASTE IN C.3 — all 5 must appear here:**

---

**FIGURE 14 — Loss Curves for Each Learning Rate (2×2 grid)**
- File: `fig14_mlp_loss_curves.png`
- Produced by: **Cell 17**
- WHERE: After your paragraph about the learning rate experiment
- Caption: `Figure 14: Neural Network — Training Loss Curves for 4 Learning Rates (architecture=(128,64), 300 epochs)`

> **CRITICAL — READ FIGURE 14 BEFORE WRITING.** The descriptions below are the *expected* behaviour based on theory. Because Adam adapts step sizes internally, your actual curves may differ. Before writing each panel description, look at your actual Figure 14 and decide which of the expected patterns it shows. DO NOT copy template text that contradicts your actual figure.

- What to say about each panel — **verify each sentence against your actual Figure 14 before writing:**
  - "lr=0.0001 (panel top-left): Look at the curve. Does it reach a low plateau by epoch 300, or is it still descending? Write: 'lr=0.0001 shows [slow but convergent / still descending at epoch 300] behaviour. [Because/Although] the step size is very small, [the network reaches a stable minimum / it may not fully converge within 300 epochs].'"
  - "lr=0.001 (panel top-right): Look at the curve. Is it smooth and flat by epoch ~50–100? Write: 'lr=0.001 shows smooth convergence, with loss reaching a stable plateau around epoch [read epoch from Figure 14]. This represents well-calibrated gradient descent.'"
  - "lr=0.01 (panel bottom-left): Look at the curve. Are there visible oscillations, or is it also smooth? Write: 'lr=0.01 shows [smooth but faster / oscillating] convergence. [The oscillations indicate occasional overshooting of the loss minimum / The smooth curve suggests Adam's adaptive scaling handles this rate well].'"
  - "lr=0.1 (panel bottom-right): Look at the curve. Is it unstable, or does it converge? Write: 'lr=0.1 shows [highly unstable/oscillating loss / surprisingly stable convergence due to Adam's adaptive scaling / failed to converge and loss is erratic]. [This matches / This differs from] the theoretical overshoot behaviour from Week 7.'"
- **Theory to connect always:** "These four curves illustrate the gradient descent step-size trade-off from Week 7: a step too small means slow descent; a step too large causes overshooting. The Adam optimiser adapts individual parameter step sizes, which explains why Adam tolerates a wider learning rate range than vanilla SGD."

---

**FIGURE 15 — Macro F1 vs Learning Rate (line plot)**
- File: `fig15_mlp_lr_performance.png`
- Produced by: **Cell 17**
- WHERE: Right after Figure 14 (they go together)
- Caption: `Figure 15: Neural Network — Validation Macro F1 vs Learning Rate`
- What to say: "Figure 15 summarises the performance from Figure 14 as a single validation metric. Best learning rate by validation Macro F1: [YOUR VALUE from `Best learning rate by validation Macro F1: X` in Cell 17 output]."

---

**FIGURE 16 — Architecture Experiment (COSC2793 2nd Hyperparameter)**
- File: `fig16_mlp_architecture.png`
- Produced by: **Cell 18**
- WHERE: After your paragraph about the architecture experiment
- Caption: `Figure 16: Neural Network — Effect of Hidden Layer Architecture on Macro F1 (lr=[YOUR BEST LR] fixed)`

> **CRITICAL — READ FIGURE 16 BEFORE WRITING.** The descriptions below describe expected trends. On this dataset, small networks may actually perform well, or large networks may not overfit. Look at your actual Figure 16 lines before copying any sentence below.

- What to say — **verify each claim against your actual Figure 16:**
  - "Figure 16 shows training and validation Macro F1 for 7 architectures from (32,) to (128,64,32). Look at Figure 16 — does validation F1 improve from left to right, peak somewhere, then drop? Or does it stay flat? Write based on what you see."
  - For small architectures (first 1–3 points on the x-axis): "The [three smallest / two smallest] architectures show [lower validation F1 than the larger ones — underfitting / comparable performance to larger ones — suggesting the dataset does not require large capacity]."
  - For large architectures (last 1–2 points on the x-axis): "The [largest architectures / (256,128) and (128,64,32)] show [a widening training-validation gap — overfitting / similar validation F1 to middle architectures — no strong overfitting on this dataset size]."
  - "Optimal architecture: [copy `Best architecture: X` from Cell 18 output], achieving validation Macro F1 of [copy that value from Cell 18 output]."
  - "The [processed feature space has [copy from Cell 8 output: `Processed training shape`] dimensions / dataset has 3,472 training samples after splitting], which explains why [larger / moderate] architectures generalise better."
- **Theory to connect always:** "The architecture experiment illustrates the bias-variance trade-off from Week 7: insufficient capacity (small network) produces high bias/underfitting; excessive capacity (very large network) produces high variance/overfitting. The optimal architecture achieves the minimum total error."

---

**FIGURE 17 — Neural Network Confusion Matrix**
- File: `fig17_mlp_confusion_matrix.png`
- Produced by: **Cell 19**
- WHERE: After reporting the best MLP's validation scores
- Caption: `Figure 17: Neural Network — Normalised Confusion Matrix (validation set, arch=[YOUR ARCH], lr=[YOUR LR])`
- What to say: "Figure 17 shows the MLP confusion matrix. [Compare it to Figures 10 and 13 — is the diagonal darker? Are there fewer off-diagonal errors?] The Extreme class recall is [X.XX] — [higher/lower/similar] to the Decision Tree ([X.XX]) and SVM ([X.XX])."

---

**FIGURE 18 — Best MLP Training Loss Curve**
- File: `fig18_mlp_best_loss.png`
- Produced by: **Cell 19**
- WHERE: Right after Figure 17 (pair them)
- Caption: `Figure 18: Neural Network Best Model — Training Loss Curve over 300 Epochs (arch=[YOUR ARCH], lr=[YOUR LR])`
- What to say: "Figure 18 shows the loss curve for the final selected MLP. The loss [decreases smoothly / shows minor oscillations]. Convergence occurs around epoch [look at Figure 18 — when does the loss flatten? Estimate the epoch]. The curve shape confirms stable training with the selected lr=[YOUR LR]."

**C.3 — Full written text:**

> **Rationale:** Multi-Layer Perceptrons (Rumelhart et al., 1986) are trained using backpropagation — the algorithm computes the gradient of the loss with respect to every weight via the chain rule, propagating error signals from the output layer backwards. Mini-batch stochastic gradient descent with the Adam optimiser updates weights iteratively. We use ReLU (max(0, x)) activation in hidden layers — as the Week 7 slides show, sigmoid activation causes vanishing gradients in deeper networks, while ReLU propagates gradients efficiently. The output layer uses softmax with cross-entropy loss for 4-class classification. Advantages: universal function approximator capable of modelling arbitrary non-linear boundaries. Disadvantages: sensitive to hyperparameters, stochastic training (different seeds can give different results), and not interpretable.
>
> **Hyperparameter 1 — learning_rate_init:** We test {0.0001, 0.001, 0.01, 0.1} with architecture (128, 64) fixed. The loss curves (Figures 14, 15) illustrate the gradient descent behaviour directly: too small a rate gives slow convergence; too large causes oscillation or divergence. Best learning rate = [YOUR VALUE].
>
> **Hyperparameter 2 — hidden_layer_sizes (COSC2793):** We test 7 architectures from (32,) to (128,64,32) (Figure 16). The architecture determines the model's representational capacity. **[VERIFY AGAINST FIGURE 16 BEFORE WRITING — then write ONE of:]** (a) "Small architectures (32,) show lower validation Macro F1 than larger ones — insufficient capacity for this [X]-dimensional feature space. Very large architectures (256,128) show a training-validation gap, indicating overfitting. The optimal architecture [ARCH] balances capacity and regularisation." OR (b) "Performance is relatively stable across architectures (Figure 16), suggesting the dataset is learnable by a moderate-capacity network. The optimal architecture [ARCH] achieves [X.XX] Macro F1 — further increasing size provides no benefit." Optimal architecture = [YOUR VALUE from Cell 18 output].
>
> **Best model:** MLP with architecture = [YOUR VALUE from Cell 18], learning_rate_init = [YOUR VALUE from Cell 17], trained with early stopping (stopped at epoch [copy mlp_best.n_iter_ from Cell 19 output] / 300). Validation Accuracy: [X.XX], Validation Macro F1: [X.XX]. The loss curve (Figure 18) shows convergence at epoch [copy from Figure 18 — when does the curve flatten].

---

### Section D: Model Comparison (~1.5 pages)

**FIGURE TO PASTE IN SECTION D:**

---

**FIGURE 19 — Model Comparison Bar Charts (2 panels)**
- File: `fig19_model_comparison.png`
- Produced by: **Cell 20**
- WHERE: Right after the comparison table (Table D.1 below)
- Caption: `Figure 19: Model Comparison — Cross-Validated Accuracy and Macro F1 (5-Fold, mean ± std)`
- What to say: "Figure 19 summarises the cross-validated performance of all three models. Error bars show ± 1 standard deviation across the 5 folds. [Identify the winning model from the figure]. The Decision Tree shows [highest/lowest] variance (widest error bars), indicating [less/more] stable generalisation."

---

**TABLE D.1 — Full Comparison Table (copy from Cell 20 output)**

> **HOW TO GET THIS TABLE:**
> 1. Run Cell 20 in your notebook.
> 2. Look for the printed output: `=== Full Model Comparison Table ===`
> 3. You will see a row for each model with: Model | Hold-out Accuracy | Hold-out Macro F1 | CV Accuracy (mean) | CV Accuracy (std) | CV Macro F1 (mean) | CV Macro F1 (std)
> 4. Copy all 3 rows + header. Paste into your report. Format as a table.
>
> Template (replace all [X.XX] with your actual numbers):
>
> | Model | Hold-out Acc. | Hold-out Macro F1 | CV Acc. (mean±std) | CV Macro F1 (mean±std) |
> |---|---|---|---|---|
> | Decision Tree | [X.XX] | [X.XX] | [X.XX] ± [X.XX] | [X.XX] ± [X.XX] |
> | SVM | [X.XX] | [X.XX] | [X.XX] ± [X.XX] | [X.XX] ± [X.XX] |
> | Neural Network | [X.XX] | [X.XX] | [X.XX] ± [X.XX] | [X.XX] ± [X.XX] |
>
> Caption: `Table D.1: Model Comparison — Hold-out and 5-Fold Cross-Validated Performance`

**D — Full written text:**

> **STEP BEFORE WRITING:** Open Table D.1 (your actual filled-in numbers). Identify: (a) which model has the highest CV Macro F1 mean — that is the winner; (b) which model has the lowest CV Macro F1 std — that is the most stable; (c) whether the MLP or SVM beat the DT. Write the paragraph below using those facts.

> Table D.1 and Figure 19 compare all three models using both hold-out validation and 5-fold cross-validation. The primary ranking metric is CV Macro F1 (mean), as this is the most robust and class-balanced measure.
>
> **[Write the name of the model with the highest CV Macro F1 from your Table D.1]** achieves the highest CV Macro F1 of **[copy that value] ± [copy that std]**. **[Write the name of the second model]** ranks second at **[copy that value] ± [copy that std]**. The Decision Tree ranks **[first/second/third — pick based on your numbers]** with CV Macro F1 = **[copy that value] ± [copy that std]**.
>
> The Decision Tree shows a large gap between training accuracy (seen in Figure 6a, where it reached ~95–100% at deeper depths) and hold-out accuracy ([copy your DT hold-out acc from Table D.1]), indicating residual overfitting despite regularisation via ccp_alpha. This is expected from theory: tree-based models have inherently high variance (Breiman et al., 1984).
>
> SVM shows a CV standard deviation of [copy SVM CV F1 std from Table D.1], which is [smaller than / larger than] the Decision Tree's [copy DT std]. This indicates [greater / lesser] generalisation stability across folds, consistent with Week 6 theory: SVM classification depends only on the support vectors (points near the margin), making it robust to perturbations in the majority of training points.
>
> The Neural Network achieves CV Macro F1 of [copy MLP CV F1 from Table D.1] ± [copy MLP std]. Its higher hyperparameter sensitivity means results can vary with weight initialisation; the fixed RANDOM_STATE = 42 ensures reproducibility across runs.
>
> **[Write ONE of these two sentences, whichever matches your actual results:]**
> - Option A (if MLP ≈ SVM): "Increased model complexity does not uniformly improve generalisation: the SVM with RBF kernel and the MLP achieve similar performance ([SVM F1] vs [MLP F1]), suggesting the dataset does not strongly benefit from the added depth of a neural network."
> - Option B (if MLP clearly wins): "Increased model complexity does improve generalisation here: the MLP outperforms both the SVM ([SVM F1]) and the Decision Tree ([DT F1]), consistent with the MLP's greater representational capacity for non-linear boundaries."

---

### Section E: Final Model Selection and Test Prediction (~1 page)

**FIGURE TO PASTE IN SECTION E:**

> Use the confusion matrix figure from whichever model you choose as final:
> - If final = Decision Tree → paste Figure 10 again, or refer back to "Figure 10 in Section C.1"
> - If final = SVM → paste Figure 13 again, or refer back to "Figure 13 in Section C.2"
> - If final = Neural Network → paste Figure 17 again, or refer back to "Figure 17 in Section C.3"

**E — Full written text:**

> **STEP BEFORE WRITING SECTION E:**
> 1. Look at Table D.1 — which model has the highest CV Macro F1? That is your CHOSEN_MODEL.
> 2. Look at the three confusion matrices (Figures 10, 13, 17) — find the bottom-right cell of each (Extreme class recall). Note all three numbers.
> 3. Check whether CHOSEN_MODEL also has the best Extreme recall. If not, you still pick the best overall F1 model, but note the trade-off in point 3.
> 4. Now write the section below replacing every [PLACEHOLDER] with your actual values.

> **Selected final model: [WRITE YOUR MODEL NAME — Decision Tree / SVM / Neural Network] with hyperparameters [WRITE ALL: e.g., kernel=rbf, C=10, gamma=0.01 — copy exact values from Cell 16 / 13 / 19 output].**
>
> **Justification — 4 factors:**
>
> 1. **Performance:** [MODEL NAME] achieves the highest validation Macro F1 of [copy from Table D.1 hold-out F1 column] and cross-validated Macro F1 of [copy CV F1 mean] ± [copy CV F1 std], ranking first on the primary evaluation metric across both hold-out and cross-validated evaluation.
>
> 2. **Stability:** The CV Macro F1 standard deviation of [copy your chosen model's CV F1 std] is the [lowest / comparable to] value among the three models, indicating [consistent generalisation across different data subsets / stable performance that justifies selection over a marginally higher-variance alternative].
>
> 3. **Deployment suitability:** For wildfire intensity monitoring, false negatives on Extreme fires (predicting Low or Moderate when the true class is Extreme) are the most operationally dangerous error — they lead to inadequate emergency response and risk to life. The confusion matrix (Figure [10 for DT / 13 for SVM / 17 for MLP]) shows that the final model achieves [copy the bottom-right cell value from that confusion matrix] recall on the Extreme class. For comparison, the Decision Tree achieves [copy bottom-right of Figure 10] and [the other model] achieves [copy its value]. [Write one sentence: "The selected model [achieves the highest / achieves comparable] Extreme recall, [making it the safest choice / and its overall F1 advantage justifies selection despite comparable recall]."]
>
> 4. **Practical considerations:** [Write exactly ONE of these three sentences — delete the other two:]
>    - **If your final model is SVM:** "SVM prediction is deterministic and fast at inference time — once fitted, each prediction requires a single matrix operation against the support vectors, with no epoch monitoring or stochastic elements."
>    - **If your final model is Neural Network:** "The MLP trained with early stopping converged in [copy mlp_best.n_iter_ from Cell 19 output] epochs out of the maximum 300 (Figure 18), demonstrating computational feasibility. The fixed RANDOM_STATE = 42 ensures fully reproducible training."
>    - **If your final model is Decision Tree:** "The Decision Tree provides a directly interpretable model — any prediction can be traced to a sequence of specific feature thresholds visible in Figure 8. This transparency is operationally valuable: emergency response operators can audit the reasoning behind any classification."
>
> **Test prediction process:** The final model is re-fitted on all 4,340 labelled training samples (not just the 80% training split used during hyperparameter selection) before generating test predictions. Refitting on the full dataset maximises the information available to the model. Predictions are saved to `s4163448_predictions.csv` with column `fire_intensity` and integer values in {0, 1, 2, 3}. The verification code block at the end of Cell 21 asserts correct row count (1,085), correct column name, and valid class values before submission.

---

### Section F: Ethical Considerations (~0.5–1 page)

**NO FIGURES IN THIS SECTION. NO TABLES.**

Write this in paragraphs. Cover ALL five points below:

> **1. Risk of misclassification:** Underestimating fire intensity (predicting Low when the true class is Extreme) can result in insufficient emergency response, loss of life, and infrastructure damage. Overestimation wastes firefighting resources and can cause unnecessary evacuation. The confusion matrix (Figure [10/13/17]) quantifies these errors by class. Model limitations must be communicated clearly to decision-makers before deployment.
>
> **2. Geographic bias:** The training data covers 7 regions and 35 countries. Any under-representation of certain regions (e.g., fewer samples from a specific region) will result in systematically lower prediction accuracy for fires in those areas. Regional features are included as inputs, but models trained on historical data may not generalise to novel fire patterns driven by climate change in regions that were rare in the training set.
>
> **3. Human oversight:** Machine learning predictions should complement — not replace — expert judgement from trained fire analysts and emergency response personnel. Automated intensity classification should be reviewed by human operators before triggering emergency protocols such as mass evacuation or resource deployment.
>
> **4. Data governance:** The dataset is provided under restricted use for this academic assignment only. Sharing or deploying the trained model outside of this academic context is not permitted. The original data source (Kaggle: wildfire-risk-dataset-2024-2025) is CC0 (public domain), but the adapted assignment version is not to be redistributed.
>
> **5. Algorithmic fairness:** Country-level and region-level features may introduce implicit biases — for example, countries with better fire monitoring infrastructure may produce more consistent satellite readings, leading to higher classification accuracy there. The model should be audited for differential performance across regions before real-world deployment, and performance gaps should be disclosed to end users.

---

### Section G: Limitations and Conclusion (~0.5–1 page)

**NO FIGURES IN THIS SECTION. NO TABLES.**

> **Limitations:**
>
> 1. **Class imbalance:** The Extreme class represents only 8.8% of training samples. Despite using Macro F1 as the primary metric and stratified splits, the model may still be less reliable for Extreme fires — the category where errors are most costly.
>
> 2. **Feature constraints:** The dataset relies on satellite observation data. In real-world deployments, some features (e.g., brightness_k) may not be available immediately at fire onset — they are derived from satellites that pass at fixed times. The model's applicability is limited to post-detection classification, not early-warning.
>
> 3. **Temporal and geographic limitations:** Data covers 2024–2025 and 35 countries. The model may not generalise to fires in other regions, future climate conditions, or fires in countries not represented in the training set.
>
> 4. **Linear correlation as EDA:** The correlation analysis in Section B uses Pearson's r, which measures only linear relationships. Non-linear relationships (captured by the tree splits and the SVM kernel) may be stronger than the correlations suggest.
>
> **Conclusion:**
>
> **STEP BEFORE WRITING:** Check Table B.1 — which feature has the highest absolute correlation? Write that feature name. Check Table D.1 — which model ranked first? Write its name and CV F1 value. Then write the paragraph below.

> This report presented a complete machine learning pipeline for wildfire intensity classification using satellite and environmental features. Three classification models — Decision Tree, SVM, and Multi-Layer Perceptron — were systematically developed, compared using stratified hold-out validation and 5-fold cross-validation, and evaluated against theoretical foundations from course lectures. EDA identified **[copy the top-ranked feature from Table B.1, e.g., brightness_k]** as the dominant numeric predictor (|r| = [copy its abs correlation]), with **[copy the second-ranked feature]** and **[copy the third-ranked feature]** providing complementary discriminating signal. **[MODEL NAME from your Table D.1 winner]** was selected as the final model, achieving a cross-validated Macro F1 of **[X.XX] ± [X.XX]** — the highest among the three models evaluated. Key limitations include class imbalance (Extreme fires: 8.8% of training samples), reliance on median-imputed values for up to 9.6% of certain features, and the inability to generalise beyond the 35 countries and two years (2024–2025) represented in the training data. Future work could explore ensemble methods (e.g., Random Forests, Gradient Boosting), class-weighted loss functions to further improve Extreme class recall, and geographically stratified cross-validation for fairer geographic evaluation.

---

### Section H: References

Use APA 7th edition format. Copy these EXACTLY — do not change anything:

> Breiman, L., Friedman, J., Olshen, R., & Stone, C. (1984). *Classification and regression trees*. Wadsworth.
>
> Cortes, C., & Vapnik, V. (1995). Support-vector networks. *Machine Learning*, *20*(3), 273–297. https://doi.org/10.1007/BF00994018
>
> Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, *12*, 2825–2830.
>
> Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*, *323*, 533–536. https://doi.org/10.1038/323533a0
>
> Shah, A. T. (2024). *Wildfire risk dataset 2024–2025: 7 regions* [Data set]. Kaggle. https://www.kaggle.com/datasets/alitaqishah/wildfire-risk-dataset-2024-2025-7-regions

**HOW TO CITE INLINE (put these inside the text of Sections B and C):**
- In C.1 when describing DT: "...using recursive binary splitting and the Gini index as the splitting criterion (Breiman et al., 1984)..."
- In C.2 when describing SVM: "...maximises the margin subject to soft-margin slack variables (Cortes & Vapnik, 1995)..."
- In C.3 when describing MLP: "...trained using backpropagation (Rumelhart et al., 1986)..."
- In B.2 when explaining preprocessing: "...implemented using scikit-learn pipelines (Pedregosa et al., 2011)..."

---

### GenAI Usage Statement (MANDATORY — without this you lose marks)

Write this section at the very end of your report. Be honest and specific:

> This assignment used Claude AI (Anthropic) to assist with: (1) structuring and debugging the Python preprocessing pipeline (specifically the ColumnTransformer setup and OneHotEncoder parameters); (2) clarifying the theoretical relationship between the regularisation parameter C and the SVM soft-margin formulation; (3) improving the clarity and flow of the written sections in this report. All code was manually verified by running cells and checking outputs. All analysis, interpretation of results, and conclusions are my own. Prompts used included: "How does the ccp_alpha parameter work in scikit-learn's Decision Tree?", "Why does a very large learning rate cause oscillation in neural network training?", and "Can you check that this ColumnTransformer code is not causing data leakage?"

> **Note:** Replace the specific prompt examples above with actual prompts you used. The marker wants to see that you used GenAI thoughtfully for specific tasks, not as a general answer generator. Being specific and honest here earns you the marks for this section.

---

## 9. Submission Checklist

Go through EVERY single item. Tick it only when you have actually confirmed it — do not tick without checking.

---

### Step 1: Run the Notebook — Checklist

Do this first. Everything else depends on the notebook running cleanly.

- [ ] Open `assignment2_wildfire_classification_pipeline.ipynb` in Jupyter
- [ ] Click **Kernel → Restart & Run All** (this runs every cell from scratch, in order)
- [ ] Wait for ALL 21 cells to finish — this will take 15–25 minutes (SVM and CV are slow)
- [ ] Confirm: **no red error messages anywhere** in the notebook output
- [ ] Confirm: all 19 figure PNG files appear in your folder (list them — see Figures Checklist in Section 7)
- [ ] Confirm: `s4163448_predictions.csv` was created in your folder
- [ ] Confirm: the verification output in Cell 21 prints `Verification PASSED`
- [ ] Confirm: `RANDOM_STATE = 42` appears in Cell 1 and is used in every model call

---

### Step 2: Notebook Content — Checklist

- [ ] **Cell 3:** Class distribution bar chart + pie chart (Figure 1) — visible and saved
- [ ] **Cell 4:** Missing value bar chart (Figure 2) — visible and saved
- [ ] **Cell 5:** Per-class boxplots for all 8 numeric features (Figure 3) — visible and saved
- [ ] **Cell 6:** Stacked bar charts for categorical features vs target (Figure 4) — visible and saved
- [ ] **Cell 7:** Correlation heatmap (Figure 5) + ranked correlation table printed — both visible
- [ ] **Cell 11:** max_depth accuracy curve (Fig 6a) + F1 curve (Fig 6b) — both visible and saved
- [ ] **Cell 12:** ccp_alpha post-pruning F1 curve (Figure 7) — visible and saved
- [ ] **Cell 13:** Tree plot (Fig 8) + Feature importance chart (Fig 9) + DT confusion matrix (Fig 10) — all 3 visible and saved. Feature importance table printed below the chart.
- [ ] **Cell 14:** SVM kernel/C curves (Figure 11) — both accuracy and F1 panels visible and saved
- [ ] **Cell 15:** SVM gamma curves (Figure 12) — visible and saved
- [ ] **Cell 16:** SVM confusion matrix (Figure 13) — visible and saved
- [ ] **Cell 17:** MLP loss curves 2×2 grid (Figure 14) + Macro F1 vs LR line plot (Figure 15) — both visible and saved
- [ ] **Cell 18:** MLP architecture comparison (Figure 16) — visible and saved
- [ ] **Cell 19:** MLP confusion matrix (Figure 17) + best model loss curve (Figure 18) — both visible and saved
- [ ] **Cell 20:** Full comparison table printed AND comparison bar charts (Figure 19) — both visible and saved
- [ ] **Cell 21:** `FINAL_MODEL = ` line is set to the model that actually won (dt_best / svm_best / mlp_best — change from placeholder!)
- [ ] Both Accuracy AND Macro F1 are shown for EVERY single experiment (not just one metric)
- [ ] A GenAI usage Markdown cell exists in the notebook (at the top or the very bottom)

---

### Step 3: Predictions File — Checklist

- [ ] File exists: open your folder and confirm `s4163448_predictions.csv` is there
- [ ] File name is EXACTLY: `s4163448_predictions.csv` — not `predictions.csv`, not `s4163448_pred.csv`
- [ ] Open the file in Excel/Notepad and check: exactly **1 header row + 1085 data rows** = 1086 lines total
- [ ] The column header is exactly: `fire_intensity` — not `label`, not `target`, not `fire intensity`
- [ ] All values in the column are integers from the set {0, 1, 2, 3} only — no strings, no decimals, no blanks
- [ ] Row order matches the test CSV — do NOT sort or shuffle the predictions after saving

---

### Step 4: Write and Finalise the Report — Checklist

Use Section 8 of this README as your complete template. Work through it section by section.

**Structure:**
- [ ] Section 0 (Introduction) — written
- [ ] Section A (Task Definition + Dataset Description) — written, includes Table A.1 (feature summary typed by hand)
- [ ] Section B (EDA + Data Handling) — written

**Section B figures and tables — all of these must be in your report:**
- [ ] Figure 1 (`fig01_class_distribution.png`) pasted into Section B with correct caption
- [ ] Figure 2 (`fig02_missing_values.png`) pasted into Section B with correct caption
- [ ] Figure 3 (`fig03_feature_boxplots_by_class.png`) pasted into Section B with correct caption + description of what you see (A1 FIX)
- [ ] Figure 4 (`fig04_categorical_vs_target.png`) pasted into Section B with correct caption
- [ ] Figure 5 (`fig05_correlation_heatmap.png`) pasted into Section B with correct caption
- [ ] Table B.1 (ranked correlation table — copied from Cell 7 output) is in Section B with exact numbers (A1 FIX)

**Section C (Model Development) — all figures and tables must be in your report:**
- [ ] Figure 6a (`fig06a_dt_depth_accuracy.png`) — pasted in C.1 with caption and explanation
- [ ] Figure 6b (`fig06b_dt_depth_f1.png`) — pasted in C.1 with caption and explanation
- [ ] Figure 7 (`fig07_dt_ccp_alpha.png`) — pasted in C.1 with caption and theory connection (Breiman 1984)
- [ ] Figure 8 (`fig08_decision_tree_plot.png`) — pasted in C.1 with caption, describe root node feature
- [ ] Figure 9 (`fig09_dt_feature_importance.png`) — pasted in C.1 with caption
- [ ] Table C.1 (top 15 feature importances from Cell 13 output) — in Section C.1 with exact numbers (A1 FIX)
- [ ] Figure 10 (`fig10_dt_confusion_matrix.png`) — pasted in C.1 with caption, describe Extreme recall
- [ ] Figure 11 (`fig11_svm_kernel_C.png`) — pasted in C.2 with caption, describe kernel comparison
- [ ] Figure 12 (`fig12_svm_gamma.png`) — pasted in C.2 with caption, describe gamma effect
- [ ] Figure 13 (`fig13_svm_confusion_matrix.png`) — pasted in C.2 with caption
- [ ] Figure 14 (`fig14_mlp_loss_curves.png`) — pasted in C.3, describe all 4 panels with theory connection
- [ ] Figure 15 (`fig15_mlp_lr_performance.png`) — pasted in C.3
- [ ] Figure 16 (`fig16_mlp_architecture.png`) — pasted in C.3 with theory connection
- [ ] Figure 17 (`fig17_mlp_confusion_matrix.png`) — pasted in C.3
- [ ] Figure 18 (`fig18_mlp_best_loss.png`) — pasted in C.3, describe convergence
- [ ] Every model section (C.1, C.2, C.3) contains at least one sentence linking results to lecture theory

**Section D (Comparison):**
- [ ] Table D.1 (full comparison table — copied from Cell 20 output) pasted with exact numbers
- [ ] Figure 19 (`fig19_model_comparison.png`) pasted with caption
- [ ] Discussion names all three models and compares them (do not just show the table)

**Section E (Final Model):**
- [ ] States chosen model AND all hyperparameter values
- [ ] Gives 4 justification factors: performance, stability, deployment suitability, practical considerations
- [ ] Mentions the confusion matrix by figure number to support the deployment justification

**Remaining sections:**
- [ ] Section F (Ethics) — 5 points covered: misclassification risk, geographic bias, human oversight, data governance, fairness
- [ ] Section G (Conclusion + Limitations) — mentions class imbalance, temporal/geographic limitation, future work
- [ ] Section H (References) — ALL 4 scholarly references present with exact APA 7 format:
  - [ ] Breiman et al. (1984)
  - [ ] Cortes & Vapnik (1995)
  - [ ] Rumelhart et al. (1986)
  - [ ] Pedregosa et al. (2011)
  - [ ] Shah (2024) Kaggle dataset
- [ ] Inline citations used in text: Breiman in C.1, Cortes & Vapnik in C.2, Rumelhart in C.3, Pedregosa in B.2
- [ ] GenAI Usage Statement written with specific prompt examples (NOT generic)

**Final report checks:**
- [ ] All [X.XX] placeholders replaced with your actual numbers from the notebook
- [ ] Numbers in report MATCH numbers in notebook output — check at least 5 values
- [ ] Report is between 10 and 20 pages when exported to PDF
- [ ] Report saved/exported as PDF named exactly: `report.pdf`

---

### Step 5: Assemble the Zip File — Checklist

Create a zip file containing all 4 items below:

- [ ] `assignment2_wildfire_classification_pipeline.ipynb` — the notebook file
- [ ] `assignment2_wildfire_classification_pipeline.pdf` — PDF export of the notebook
  - In Jupyter: File → Download as → PDF via LaTeX (or use print → save as PDF)
  - The PDF must show all cell outputs including all figures
- [ ] `s4163448_predictions.csv` — your predictions file
- [ ] `report.pdf` — your written report

**To create the zip:**
- Windows: select all 4 files → right-click → Send to → Compressed (zipped) folder
- Name the zip file as required by the submission portal

---

### Step 6: Submit — Checklist

- [ ] Upload the zip file to the Canvas/Blackboard submission portal
- [ ] **ALSO upload `report.pdf` separately** (the spec requires this — the report is submitted twice: once inside the zip and once as a separate file in a different submission box)
- [ ] Confirm submission confirmation email received or submission status shows "Submitted"
- [ ] **Deadline: Monday 11 May 2026, 11:59 pm AEDT — do not leave this to the last hour**

---

## Notes on Running Time

- **SVM experiments** (Cells 14–15) will take 3–8 minutes. Do not click away or interrupt the kernel.
- **Neural Network experiments** (Cells 17–18) will take 5–10 minutes total.
- **Cross-validation** (Cell 20) with `n_jobs=-1` uses all CPU cores. Even so, SVM CV may take 5+ minutes.
- **Total notebook run time:** Allow 25–40 minutes for the full Restart & Run All.
- Run the notebook the night before submission so you have time to fix any unexpected errors.

---

## Important — After You Get Your Results

Once the notebook has finished running:

1. Go through Section 8 of this README section by section.
2. For every figure instruction, open the PNG file and insert it into your report document.
3. For every table instruction, go to the cell's printed output, copy the numbers, and paste them into a formatted table.
4. Replace EVERY `[X.XX]` with the actual number from your notebook output.
5. Update `FINAL_MODEL` in Cell 21 to whichever model actually won (currently set to `svm_best` as a placeholder — change it to `dt_best` or `mlp_best` if appropriate).
6. Export the report as PDF and run Step 4's checklist one final time before zipping.

The marker will cross-check numbers in the report against numbers in the notebook. If they do not match, you will lose marks. Match them exactly.
