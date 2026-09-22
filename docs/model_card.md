# RetailOps AI — ML Model Card

## 1. Purpose

RetailOps AI uses machine learning and statistical methods to support
e-commerce operations teams in identifying unusual business behavior,
forecasting marketplace performance, and prioritizing orders with elevated
late-delivery risk.

The models provide decision support and should not be treated as autonomous
business decision makers.

---

## 2. Anomaly Detection

### Purpose

Identify unusual changes in marketplace KPIs that may require investigation.

### Metrics

- Revenue
- Order volume
- Late-delivery rate
- Average review score
- Negative-review rate

### Method

Rolling historical Z-score detection.

The current month is excluded from its own historical baseline to reduce
look-ahead bias.

### Output

Anomalies include:

- direction
- business impact
- severity

### Limitations

Statistical anomalies do not automatically imply business problems or causal
relationships.

An anomaly should trigger investigation rather than automatic action.

---

## 3. Revenue Forecasting

### Purpose

Estimate near-term marketplace revenue for planning.

### Models Evaluated

- Naive previous-period baseline
- Holt exponential smoothing

### Validation

Models were evaluated using a chronological holdout period rather than a
random train/test split.

### Results

Naive baseline:

- MAE: approximately R$43,232
- RMSE: approximately R$63,300
- MAPE: approximately 4.94%

Holt exponential smoothing:

- MAPE: approximately 27.41%

### Model Selection

The naive baseline was retained because it substantially outperformed the
more complex trend model on the temporal holdout period.

This demonstrates that increased model complexity does not necessarily
improve forecasting performance.

### Limitations

The dataset contains only about 20 reliable monthly observations, which
limits the reliability of more complex time-series models.

---

## 4. Late-Delivery Risk Model

### Purpose

Prioritize orders that may warrant operational investigation for elevated
late-delivery risk.

### Model

Class-weighted Logistic Regression.

### Target

`is_late`

- 0 = delivered on or before estimated delivery date
- 1 = delivered after estimated delivery date

### Validation Strategy

Chronological split:

- Training data: historical orders before June 2018
- Test data: June–August 2018

This better represents deployment than a random split.

### Important Features

Examples include:

- estimated delivery window
- historical seller late-delivery rate
- historical seller order volume
- order characteristics
- customer state

### Leakage Prevention

Information unavailable at prediction time is excluded.

Examples of prohibited features:

- actual delivery date
- delivery duration
- actual delay
- review score
- review text

### Performance

Approximate temporal holdout performance:

- ROC-AUC: 0.706
- Recall at 0.50 threshold: 81%
- Precision at 0.50 threshold: 9%

An operational threshold of approximately 0.60 provides a more balanced
screening trade-off:

- Recall: approximately 54%
- Precision: approximately 10%

### Intended Use

The model should be used for:

- risk screening
- prioritizing operational investigations
- identifying orders that may warrant additional attention

### Not Intended For

The model should not be used to:

- guarantee whether an order will arrive late
- automatically penalize sellers
- automatically cancel orders
- make consequential decisions without human review

---

## 5. Probability Interpretation

The model's raw probability outputs are not currently probability-calibrated.

Therefore, values should be interpreted as relative risk scores rather than
literal real-world probabilities.

For example, a model score of 0.90 should not be communicated as:

> "There is a 90% chance this order will be late."

Instead:

> "This order has a high model-estimated delivery-risk score and may warrant
> investigation."

---

## 6. Geographic Features

Customer state is used as a predictive feature and some geographic categories
receive relatively strong model coefficients.

These coefficients represent statistical associations in this historical
dataset.

They must not be interpreted as evidence that geography causes delivery
problems.

Geographic signals should not independently drive consequential decisions.

---

## 7. Dataset Limitations

The project uses the historical Olist Brazilian e-commerce dataset.

Important limitations include:

- historical data from 2017–2018
- Brazilian marketplace context
- anonymized marketplace data
- changing seller and logistics behavior over time
- potential distribution shift in modern e-commerce environments

Model performance should not be assumed to generalize to another marketplace
without retraining and evaluation.

---

## 8. Human Oversight

RetailOps AI is designed as a decision-support system.

The intended workflow is:

Data → Analytics / ML → AI Explanation → Human Review → Business Action

AI-generated recommendations and ML risk signals should support human
investigation rather than automatically trigger consequential actions.