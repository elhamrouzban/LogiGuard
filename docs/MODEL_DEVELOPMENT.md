# Model Development and Evaluation

This document records the Week 2 model development and validation results for LogiGuard.

## Baseline Reference — Logistic Regression

Validation results:

- Accuracy: `0.701`
- Precision: `0.836`
- Recall: `0.561`
- F1-score: `0.671`
- ROC-AUC: `0.743`

The Logistic Regression model is used as the baseline reference for Week 2 model comparisons.

## Decision Tree

Validation results:

- Accuracy: `0.634`
- Precision: `0.663`
- Recall: `0.670`
- F1-score: `0.666`
- ROC-AUC: `0.631`

Training results:

- Accuracy: `1.000`
- Precision: `1.000`
- Recall: `1.000`
- F1-score: `1.000`
- ROC-AUC: `1.000`

The unrestricted Decision Tree shows severe overfitting: it fits the training data perfectly but generalizes much more poorly to the validation set.

Compared with Logistic Regression, it achieves higher recall but lower Accuracy, Precision, F1-score, and ROC-AUC.

## Random Forest

Validation results:

- Accuracy: `0.704`
- Precision: `0.790`
- Recall: `0.621`
- F1-score: `0.696`
- ROC-AUC: `0.762`

Training results:

- Accuracy: `1.000`
- Precision: `1.000`
- Recall: `1.000`
- F1-score: `1.000`
- ROC-AUC: `1.000`

The Random Forest also shows overfitting, with perfect training performance and lower validation performance.

However, it currently provides the strongest validation performance among the evaluated models, with the highest F1-score and ROC-AUC so far.


## XGBoost

Validation results:

- Accuracy: `0.710`
- Precision: `0.806`
- Recall: `0.616`
- F1-score: `0.698`
- ROC-AUC: `0.764`

Training results:

- Accuracy: `0.760`
- Precision: `0.867`
- Recall: `0.664`
- F1-score: `0.752`
- ROC-AUC: `0.866`

XGBoost currently provides the strongest validation performance among the evaluated models, with the highest Accuracy, F1-score, and ROC-AUC.

The gap between training and validation performance indicates some overfitting, but it is substantially less severe than the unrestricted Decision Tree and Random Forest.


## Model Comparison

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.701 | 0.836 | 0.561 | 0.671 | 0.743 |
| Decision Tree | 0.634 | 0.663 | 0.670 | 0.666 | 0.631 |
| Random Forest | 0.704 | 0.790 | 0.621 | 0.696 | 0.762 |
| XGBoost | 0.710 | 0.806 | 0.616 | 0.698 | 0.764 |

Current observations:

- Logistic Regression remains the baseline reference and has the highest precision.
- Decision Tree has the highest recall but shows severe overfitting.
- Random Forest improves recall, F1-score, and ROC-AUC over the baseline, but also shows severe overfitting.
- XGBoost currently has the strongest overall validation performance, with the highest Accuracy, F1-score, and ROC-AUC.
- Random Forest and XGBoost are the main candidates for hyperparameter tuning.

### Random Forest and XGBoost are the main candidates for hyperparameter tuning.