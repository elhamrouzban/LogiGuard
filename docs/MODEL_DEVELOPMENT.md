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


### Model Timing Comparison

Training and prediction times were measured on the same machine using the same prepared training and validation datasets.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | Train Time (s) | Prediction Time (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.701 | 0.836 | 0.561 | 0.671 | 0.743 | 0.119 | 0.00058 |
| Decision Tree | 0.634 | 0.663 | 0.670 | 0.666 | 0.631 | 1.667 | 0.00375 |
| Random Forest | 0.704 | 0.790 | 0.621 | 0.696 | 0.762 | 83.850 | 1.06424 |
| XGBoost | 0.710 | 0.806 | 0.616 | 0.698 | 0.764 | 0.245 | 0.00990 |

These timings are based on single runs and should be treated as development-time measurements rather than stable benchmark results. A repeated timing benchmark can be performed later if computational performance becomes part of final model selection.

### Initial timing results show that XGBoost provides the strongest validation performance among the screened models while remaining substantially faster to train than the default Random Forest.



# Model Tunings

## Hyperparameter Tuning

Hyperparameter tuning was performed using the training set for fitting and the validation set for model selection.

Configurations were ranked primarily by validation ROC-AUC.

The test set remained untouched during tuning and model selection.


### XGBoost Tuning

A grid of 32 hyperparameter configurations was evaluated.

The tuning search completed in approximately `8.13 seconds`.

Best configuration by validation ROC-AUC:

- `n_estimators = 200`
- `max_depth = 5`
- `learning_rate = 0.05`
- `min_child_weight = 1`
- `subsample = 1.0`
- `colsample_bytree = 0.8`

Best tuned XGBoost results:

| Metric | Train | Validation |
|---|---:|---:|
| Accuracy | 0.720 | 0.718 |
| Precision | 0.858 | 0.845 |
| Recall | 0.587 | 0.592 |
| F1-score | 0.697 | 0.696 |
| ROC-AUC | 0.807 | 0.771 |

Timing for the selected configuration:

- Training time: `0.361 s`
- Validation prediction time: `0.0138 s`

Compared with the default XGBoost model, tuning improved validation Accuracy, Precision, and ROC-AUC while slightly reducing Recall and F1.

The train-validation ROC-AUC gap decreased substantially compared with the default XGBoost model, indicating improved generalization and reduced overfitting.


### Random Forest Tuning

A grid of 18 hyperparameter configurations was evaluated.

Best configuration by validation ROC-AUC:

- `n_estimators = 200`
- `max_depth = 20`
- `min_samples_leaf = 5`
- `max_features = "sqrt"`

Best tuned Random Forest results:

| Metric | Train | Validation |
|---|---:|---:|
| Accuracy | 0.718 | 0.719 |
| Precision | 0.858 | 0.848 |
| Recall | 0.583 | 0.590 |
| F1-score | 0.694 | 0.696 |
| ROC-AUC | 0.856 | 0.770 |

Timing for the selected configuration:

- Training time: `1.707 s`
- Validation prediction time: `0.0778 s`

The default Random Forest achieved perfect training performance, indicating severe overfitting.

After tuning, training ROC-AUC decreased from approximately `1.000` to `0.856`, while validation ROC-AUC improved from approximately `0.762` to `0.770`.

This substantially reduced the train-validation gap and improved generalization, although some remaining ROC-AUC gap indicates residual overfitting.



### Decision Tree Tuning

A grid of 72 hyperparameter configurations was evaluated.

The tuning search completed in approximately `18.04 seconds`.

Best configuration by validation ROC-AUC:

- `max_depth = 5`
- `max_features = None`
- `min_samples_leaf = 5`
- `min_samples_split = 2`

Best tuned Decision Tree results:

| Metric | Train | Validation |
|---|---:|---:|
| Accuracy | 0.719 | 0.718 |
| Precision | 0.857 | 0.846 |
| Recall | 0.584 | 0.590 |
| F1-score | 0.695 | 0.695 |
| ROC-AUC | 0.776 | 0.767 |

Timing for the selected configuration:

- Training time: `0.115 s`
- Validation prediction time: `0.0019 s`

The default unrestricted Decision Tree showed severe overfitting, with perfect training performance and substantially weaker validation performance.

After tuning, the train-validation ROC-AUC gap decreased to approximately `0.008`, while validation ROC-AUC improved from approximately `0.631` to `0.767`.

The tuned Decision Tree therefore generalized much better than the default model and showed that the poor initial result was largely caused by excessive model complexity.


### Tuning Strategy

Logistic Regression was retained as the untuned baseline model.

The three tree-based candidate models were initially evaluated using their default or near-default configurations before hyperparameter tuning.

Initial validation ROC-AUC results were approximately:

- Logistic Regression: `0.743`
- Decision Tree: `0.631`
- Random Forest: `0.762`
- XGBoost: `0.764`

XGBoost showed the strongest initial validation performance, while Random Forest was very close and therefore remained a competitive candidate.

The default Decision Tree performed substantially worse on validation and achieved perfect training performance, indicating severe overfitting. It was therefore given a controlled tuning step to determine whether reducing model complexity could improve generalization.

Hyperparameter tuning was therefore applied to:

- XGBoost, because it was the strongest initial candidate.
- Random Forest, because its initial performance was very close to XGBoost.
- Decision Tree, because its poor validation result appeared to be caused by excessive model complexity and severe overfitting.

Logistic Regression was not tuned because its role in the project is to provide a simple, interpretable baseline against which the more complex candidate models can be compared.

This strategy avoids assuming that default hyperparameters represent the full potential of each candidate algorithm while preserving a stable baseline for comparison.


### Final Tuned Model Comparison

The untuned Logistic Regression baseline was compared with the best tuned configurations of Decision Tree, Random Forest, and XGBoost.

| Model | Validation Accuracy | Precision | Recall | F1 | ROC-AUC | Training Time | Prediction Time |
|---|---:|---:|---:|---:|---:|---:|---:|
| Logistic Regression (Baseline) | 0.701 | 0.836 | 0.561 | 0.671 | 0.743 | 0.119 s | 0.0006 s |
| Tuned Decision Tree | 0.718 | 0.846 | 0.590 | 0.695 | 0.767 | 0.115 s | 0.0019 s |
| Tuned Random Forest | 0.719 | 0.848 | 0.590 | 0.696 | 0.770 | 1.707 s | 0.0778 s |
| Tuned XGBoost | 0.718 | 0.845 | 0.592 | 0.696 | 0.771 | 0.361 s | 0.0138 s |

The three tuned tree-based models achieved very similar validation performance.

XGBoost achieved the highest validation ROC-AUC (`0.771`) and slightly higher Recall (`0.592`) than the other tuned candidates.

Random Forest achieved slightly higher Accuracy and Precision, but required more training and prediction time.

The tuned Decision Tree produced validation performance close to the ensemble models while being computationally inexpensive and showing the smallest train-validation ROC-AUC gap.

Logistic Regression remained useful as a fast and interpretable baseline but showed lower validation ROC-AUC and F1 than the tuned candidate models.


No final production model is selected solely from this table. Model selection must also consider generalization, threshold behavior, operational trade-offs, and the business cost of false positives and false negatives.



### XGBoost Second-Stage Tuning

A second-stage XGBoost tuning pass was performed to refine the search around the best configuration found during the first tuning stage.

The second-stage search focused on narrower ranges around the previous best values and, for the first time, explicitly compared multiple `colsample_bytree` values.

Best Stage 2 configuration by validation ROC-AUC:

- `n_estimators = 150`
- `max_depth = 5`
- `learning_rate = 0.07`
- `min_child_weight = 1`
- `subsample = 1.0`
- `colsample_bytree = 0.7`

Stage 2 results:

| Metric | Train | Validation |
|---|---:|---:|
| Accuracy | 0.721 | 0.718 |
| Precision | 0.858 | 0.844 |
| Recall | 0.588 | 0.592 |
| F1-score | 0.698 | 0.696 |
| ROC-AUC | 0.808 | 0.772 |

Timing for the selected Stage 2 configuration:

- Training time: `0.291 s`
- Validation prediction time: `0.0113 s`

Compared with the first-stage tuned XGBoost model:

| Metric | Stage 1 | Stage 2 |
|---|---:|---:|
| Validation Accuracy | 0.7184 | 0.7180 |
| Validation Precision | 0.8451 | 0.8442 |
| Validation Recall | 0.5918 | 0.5918 |
| Validation F1 | 0.6961 | 0.6958 |
| Validation ROC-AUC | 0.7715 | 0.7717 |
| Train-Validation ROC-AUC Gap | 0.0356 | 0.0360 |
| Training Time | 0.361 s | 0.291 s |
| Prediction Time | 0.0138 s | 0.0113 s |

Stage 2 produced a very small improvement in validation ROC-AUC while preserving the same Recall and reducing computational cost.

The overall predictive performance of Stage 1 and Stage 2 remained effectively very similar.

Stage 2 was retained as the primary XGBoost candidate because it achieved the highest validation ROC-AUC, preserved Recall, and required fewer trees with lower training and prediction time.

No further hyperparameter tuning stage was performed because the second-stage improvement was marginal, suggesting diminishing returns from additional tuning on the same validation set.


## Model Selection Analysis

After hyperparameter tuning, the untuned Logistic Regression baseline was compared with the tuned Decision Tree, Random Forest, and XGBoost models.

The tuned tree-based models produced very similar validation performance.

XGBoost was selected as the primary candidate for threshold tuning because it provided the strongest overall balance of:

- highest validation ROC-AUC (`0.771`)
- slightly higher validation Recall (`0.592`)
- validation F1 comparable to the other tuned models (`0.696`)
- substantially lower training and prediction cost than Random Forest
- a smaller train-validation ROC-AUC gap than Random Forest

Decision Tree remained a strong secondary candidate because it showed very good generalization and very low computational cost, although its validation ROC-AUC was slightly lower.

Random Forest remained competitive but showed a larger train-validation ROC-AUC gap and higher computational cost.

Logistic Regression was retained as the baseline and was not selected for further threshold optimization.

Based on the full comparison, including second-stage XGBoost refinement, the Stage 2 tuned XGBoost model was selected as the primary model for the next development stage.

This selection was based on its validation ROC-AUC, competitive Recall and F1, moderate train-validation gap, and relatively low computational cost.

The selected model will next undergo threshold tuning before final evaluation on the untouched test set.



## Selected Model Threshold Analysis

After selecting the Stage 2 tuned XGBoost model as the primary model candidate, a threshold analysis was performed on the validation set.

The model itself was not retrained during this stage. Instead, the predicted probabilities produced by the selected XGBoost model were kept fixed, and different classification thresholds were applied to understand how the operating point affects Precision, Recall, F1 score, False Positives, and False Negatives.

Because LogiGuard is designed as an exception-management system, the main objective of threshold tuning was to detect a larger proportion of truly late orders while keeping the number of false alerts at a reasonable level.

An initial threshold sweep was performed from `0.30` to `0.60` in increments of `0.05`. This analysis showed that lower thresholds significantly increased Recall and reduced False Negatives, but also increased the number of False Positive alerts.

The initial sweep also showed that model behavior changed substantially around the `0.40–0.45` region. Therefore, a more detailed threshold analysis was performed between `0.35` and `0.45` using increments of `0.01`.

### Refined Threshold Results

| Threshold | Precision | Recall | F1 | False Positives | False Negatives | True Positives | True Negatives |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.35 | 0.598 | 0.902 | 0.719 | 3256 | 526 | 4849 | 1232 |
| 0.36 | 0.606 | 0.885 | 0.719 | 3098 | 617 | 4758 | 1390 |
| 0.37 | 0.611 | 0.869 | 0.718 | 2973 | 704 | 4671 | 1515 |
| 0.38 | 0.623 | 0.851 | 0.720 | 2764 | 801 | 4574 | 1724 |
| 0.39 | 0.640 | 0.818 | 0.718 | 2471 | 976 | 4399 | 2017 |
| 0.40 | 0.681 | 0.764 | 0.720 | 1920 | 1269 | 4106 | 2568 |
| 0.41 | 0.754 | 0.678 | 0.714 | 1189 | 1731 | 3644 | 3299 |
| 0.42 | 0.798 | 0.630 | 0.704 | 858 | 1988 | 3387 | 3630 |
| 0.43 | 0.820 | 0.608 | 0.698 | 718 | 2106 | 3269 | 3770 |
| 0.44 | 0.831 | 0.601 | 0.698 | 656 | 2144 | 3231 | 3832 |
| 0.45 | 0.836 | 0.597 | 0.697 | 629 | 2166 | 3209 | 3859 |

### Selected Operating Threshold

Based on the refined threshold analysis, `0.40` was selected as the operating threshold for the Stage 2 XGBoost model.

At this threshold, the validation performance was:

- Precision: `0.681`
- Recall: `0.764`
- F1: `0.720`
- True Positives: `4106`
- False Positives: `1920`
- False Negatives: `1269`
- True Negatives: `2568`

At the default threshold of `0.50`, the model achieved a Recall of `0.592` with `2194` False Negatives.

By lowering the threshold from `0.50` to `0.40`, the model identified `925` additional truly late orders and reduced the number of False Negatives from `2194` to `1269`.

This improvement comes with an increase in False Positive alerts from `587` to `1920`.

For the current LogiGuard exception-management objective, this trade-off was considered acceptable because the system is intended to surface potentially high-risk orders for operational review rather than automatically execute decisions.

The selected operating threshold is therefore:

`0.40`

The test set remained untouched throughout model selection and threshold tuning and will only be used for the final model evaluation.