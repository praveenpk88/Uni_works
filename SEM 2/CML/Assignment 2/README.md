# Assignment 2 - Wildfire Intensity Classification (COSC2793)

Student: Praveen Kumar Saravanan (s4163448)  
Course: COSC2793 - Computation Machine Learning  
Assessment: Assignment 2

## Project Overview
This project builds and compares three classification models to predict wildfire intensity classes from environmental, temporal, geospatial, and satellite-derived features.

Target variable:
- fire_intensity (4 classes): Low, Moderate, High, Extreme

Models implemented:
- Decision Tree
- Support Vector Machine (SVM)
- Neural Network (MLP)

The workflow includes:
- Data loading and inspection
- Missing-value handling
- Feature preprocessing (imputation, one-hot encoding, scaling)
- Hyperparameter analysis for all three models
- Hold-out and cross-validation evaluation
- Visual analysis (performance curves, heatmaps, confusion matrix, MLP loss curves)
- Final model selection and test-set prediction export

## Folder Contents
- assignment2_wildfire_classification_pipeline.ipynb: Main notebook (code, plots, analysis)
- report.md: Report structure/template for written submission
- wildfire_cls_train_full.csv: Training dataset with labels
- wildfire_cls_test_features.csv: Test dataset without labels

## Requirements
Recommended Python version:
- Python 3.11+ (works with current local notebook kernel setup)

Python packages:
- numpy
- pandas
- matplotlib
- seaborn
- scikit-learn

If needed, install with:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

## How to Run
1. Open assignment2_wildfire_classification_pipeline.ipynb in Jupyter/VS Code.
2. Ensure the two dataset CSV files are in the same folder as the notebook.
3. Run all cells from top to bottom.
4. Review model comparison outputs and selected final model.
5. Confirm predictions CSV is generated.

## Evaluation Design
The notebook uses a consistent framework across models:
- Stratified hold-out split (train/validation)
- 5-fold Stratified Cross-Validation on training data
- Metrics:
  - Accuracy
  - Macro F1-score

Primary model ranking metric:
- Validation Macro F1

## Hyperparameter Experiments (COSC2793 requirements)
- Decision Tree:
  - max_depth
  - min_samples_leaf
- SVM:
  - kernel (linear vs rbf)
  - C
  - gamma (rbf)
- Neural Network (MLP):
  - learning_rate_init
  - hidden_layer_sizes

## Output Files
Main expected output after full notebook run:
- s4163448_predictions.csv

Expected CSV format:
- Exactly one column named fire_intensity
- One prediction per row in the same order as wildfire_cls_test_features.csv

## Submission Checklist
Before submission, verify:
- Notebook is complete and all required analyses/plots are present.
- PDF export of the notebook matches notebook content.
- Predictions file exists and format is correct:
  - file name: s4163448_predictions.csv
  - column name: fire_intensity
- Final report is complete and addresses rubric criteria.
- GenAI usage declaration is included in the report.

## Notes
- Keep random_state fixed for reproducibility.
- Do not reorder test rows before prediction export.
- Ensure all comparisons are done under the same preprocessing/evaluation framework for fairness.
