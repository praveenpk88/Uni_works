# Wildfire Intensity Classification Report

Student: Praveen Kumar Saravanan (s4163448)  
Course: COSC2793  
Assessment: Assignment 2  
Date: 20 Apr 2026

## 1. Introduction
This report presents a machine learning workflow for multiclass classification of wildfire intensity using satellite and environmental features. The objective is to compare Decision Tree, Support Vector Machine (SVM), and Neural Network models under a consistent evaluation framework and justify a final model for test-set prediction.

## 2. Task Definition and Dataset Description
### 2.1 Prediction Task
- Task type: Supervised multiclass classification.
- Target: fire_intensity.
- Class definitions: 0 (Low), 1 (Moderate), 2 (High), 3 (Extreme).

### 2.2 Dataset Summary
- Training file: wildfire_cls_train_full.csv.
- Test file: wildfire_cls_test_features.csv.
- Feature groups:
  - Geospatial: latitude, longitude, region, country.
  - Temporal: acq_date, acq_time, year, month, season, daynight.
  - Fire observation and context: fire_type, satellite, instrument, brightness_k, confidence.
  - Weather proxies: temp_max_c, wind_max_kmh, precip_mm, humidity_pct.

### 2.3 Dataset Challenges
- Missing values in selected numeric and/or categorical features.
- Mixed feature types requiring encoding and scaling.
- Potential class imbalance across intensity classes.
- Possible multicollinearity among weather and thermal variables.

## 3. Exploratory Data Analysis and Data Handling
### 3.1 EDA Findings
- Class distribution summary and imbalance observations.
- Correlation patterns among numeric features.
- Correlations between candidate predictors and target.
- Key observations affecting modelling choices.

### 3.2 Preprocessing Pipeline
- Missing value handling:
  - Numeric: median imputation.
  - Categorical: most-frequent imputation.
- Encoding:
  - One-hot encoding for categorical features.
- Scaling:
  - Standardization for numeric features.
- Feature engineering:
  - acq_date conversion to day-of-year and week-of-year (if applied).

### 3.3 Data Split and Evaluation Protocol
- Hold-out split ratio and random seed.
- Stratification strategy.
- Cross-validation design.
- Main metrics: Accuracy and Macro F1.

## 4. Model Development and In-depth Analysis
## 4.1 Decision Tree
### 4.1.1 Rationale
Explain why Decision Tree is suitable and limitations for this dataset.

### 4.1.2 Hyperparameter Experiments
- Required: max_depth.
- Additional (COSC2793): min_samples_leaf or equivalent.
- Include performance curve(s) and table.

### 4.1.3 Tree Visualization and Insights
- Include tree plot.
- Discuss major splitting features and interpretation.
- Discuss signs of underfitting/overfitting.

## 4.2 Support Vector Machine (SVM)
### 4.2.1 Rationale
Explain strengths and weaknesses of SVM for mixed wildfire data.

### 4.2.2 Hyperparameter Experiments
- Required: C.
- Required comparison: linear vs RBF kernels.
- Additional (COSC2793): gamma or another relevant parameter.
- Include curve/heatmap and quantitative table.

### 4.2.3 Behavioral Analysis
- Effect of C on train vs validation performance.
- Effect of kernel complexity on generalization and stability.

## 4.3 Neural Network
### 4.3.1 Rationale
Explain why MLP is considered and practical limitations.

### 4.3.2 Hyperparameter Experiments
- Required: learning_rate_init.
- Additional (COSC2793): hidden_layer_sizes (or similar).
- Include result table.

### 4.3.3 Loss-Curve and Convergence Analysis
- Include training loss curves across epochs.
- Discuss convergence stability across learning rates.
- Identify underfitting/overfitting patterns.

## 5. Model Comparison
- Compare Decision Tree, SVM, and Neural Network using consistent metrics.
- Present comparison table (Val Accuracy, Val Macro F1, CV metrics).
- Explain which models are more sensitive to hyperparameters.
- Discuss whether increased complexity improved generalization.
- Connect observations to theoretical expectations.

## 6. Final Model Selection, Justification, and Evaluation
- State selected model and final hyperparameters.
- Justify selection beyond raw performance:
  - Stability.
  - Interpretability.
  - Computational cost.
  - Generalization profile.
- Show final validation confusion matrix and class-wise behavior.
- Describe process to generate test predictions.

## 7. Ethical Considerations and Professional Responsibilities
- Risks of false negatives and false positives in wildfire response.
- Potential regional/country bias and fairness concerns.
- Responsible use, human oversight, and monitoring after deployment.
- Data governance and permitted-use constraints.

## 8. Limitations and Future Improvements
- Data limitations and feature constraints.
- Potential improvements within or beyond current scope.
- Suggested future experiments.

## 9. Conclusion
Summarize key findings, selected model, and practical adequacy.

## 10. References
- Course materials (Weeks 1-8).
- Scikit-learn documentation.
- Dataset reference (assignment-provided adaptation source).

## 11. GenAI Usage Statement
State what tools were used, with prompt summaries and usage purpose:
- Debugging code.
- Clarifying concepts.
- Improving writing quality.
