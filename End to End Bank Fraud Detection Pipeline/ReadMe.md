
```markdown
# 🏦 End-to-End Bank Fraud Detection Web App

**An end-to-end machine learning pipeline and Streamlit web application designed to detect fraudulent financial transactions.**

This project analyzes a massive dataset of 6.3 million transactions, tackling extreme class imbalance (0.13% fraud rate) through optimized sampling, feature engineering, and threshold tuning. By shifting the focus from vanity metrics (accuracy) to the **Precision-Recall AUC**, the deployed XGBoost model provides high-quality, actionable fraud alerts for investigative teams, reducing false alarms and investigator fatigue.

---

## 📖 Table of Contents
- [Business Context](#-business-context)
- [Dataset](#-dataset)
- [Exploratory Data Analysis (EDA)](#-exploratory-data-analysis-eda)
- [Feature Engineering](#-feature-engineering)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [Validation & Threshold Tuning](#-validation--threshold-tuning)
- [Streamlit Web Application](#-streamlit-web-application)
- [Repository Structure](#-repository-structure)
- [Installation & Usage](#-installation--usage)
- [Authors & Acknowledgments](#-authors--acknowledgments)

---

## 💼 Business Context

Fraud is often characterized as an **"Invisible Tax,"** costing organizations approximately 5% of their annual revenue. Traditional rule-based systems fail because fraud is a complex diagnostic problem defined by four pillars:
1. **Rarity:** Fraud accounts for 1% or less of total transactions.
2. **Concealment:** Bad actors intentionally mimic normal customer behavior.
3. **Evolution:** Fraudsters constantly update methods to bypass static rules.
4. **Networked Activity:** Coordinated attacks leverage multiple accounts.

Machine learning scales in response to this complexity, capturing hidden patterns and generating precise probability scores rather than rigid binary rules.

---

## 📊 Dataset

The project utilizes the [Kaggle Fraud Detection Dataset](https://www.kaggle.com/datasets/amanalisiddiqui/fraud-detection-dataset), containing **6,362,620 financial transactions** and 11 unique features.

**Key Features:**
* `step`: Portions of time (temporal proxy).
* `type`: Transaction category (CASH-IN, CASH-OUT, DEBIT, PAYMENT, TRANSFER).
* `amount`: Total currency involved.
* `oldbalanceOrg` / `newbalanceOrig`: Source account balance before/after.
* `oldbalanceDest` / `newbalanceDest`: Target account balance before/after.
* `isFraud`: The target variable (1 = Fraud, 0 = Legitimate).

---

## 🔍 Exploratory Data Analysis (EDA)

EDA revealed critical patterns that guided the modeling strategy:
* **Risk Concentration:** While `CASH_OUT` and `PAYMENT` dominate overall volume, fraudulent activity is heavily concentrated in `TRANSFER` and `CASH_OUT` categories.
* **Amount Characteristics:** For transactions under 50k, fraudulent cases show significantly higher median values and broader interquartile ranges than legitimate ones.
* **Class Imbalance:** Only ~8,200 transactions (0.13%) are fraudulent. Accuracy is misleading; success is measured via Precision-Recall (PR) AUC.

---

## 🛠 Feature Engineering

To capture the true "Money Momentum" and flow of funds, the following features were engineered:
* **Balance Difference:** Replaced redundant balance columns (which showed 0.98+ correlation) to capture actual fund flow.
* **Hour of Day:** Extracted from the `step` column to test for high-risk temporal windows (e.g., 00:00–05:00).
* **Anomalies:** Flagged over 1 million instances of accounts being drained to exactly zero immediately after a transfer.

---

## ⚙️ Machine Learning Pipeline

A robust `Scikit-Learn` pipeline was built to prevent data leakage and ensure reproducibility.

### Preprocessing
* **Dropped:** `nameOrig`, `nameDest`, `step`, and `isFlaggedFraud` (non-predictive or redundant).
* **Scaling:** `StandardScaler` applied to numerical values.
* **Encoding:** `OneHotEncoder` applied to the categorical `type` column.
* **Data Split:** 70% Training / 30% Testing.

### Models Evaluated
| Model | Role | Imbalance Strategy | Key Characteristic |
| :--- | :--- | :--- | :--- |
| **Logistic Regression** | Interpretable baseline | `class_weight='balanced'` | Linear decision boundaries. |
| **Random Forest** | Non-linear pattern | `class_weight='balanced'` | Tree ensembles with depth limits. |
| **XGBoost (Winner)** | Gradient boosted rank | `scale_pos_weight` | Excels at ranking rare events, highest PR-AUC. |

---

## 🎯 Validation & Threshold Tuning

Rather than relying on the default 0.5 probability threshold, the model's threshold was mathematically tuned to **0.91 confidence** to align with operational reality.

**Business Impact of 0.91 Threshold:**
* **Overall Accuracy:** 94.40%
* **Recall (Fraud Capture):** ~90% (Captures 90% of fraudulent revenue).
* **Operational Efficiency:** Automatically clears 1.27 million legitimate transactions, providing investigators with a manageable, high-quality alert list and reducing false positives.

---

## 🖥 Streamlit Web Application

The final pipeline is deployed as a real-time Streamlit web application designed for bank tellers and fraud investigation teams. Users can input transaction details (type, amount, balances) and receive real-time fraud probability predictions.

**To run the app:**
```bash
streamlit run fraud_detection.py
```

---

## 📁 Repository Structure

```text
├── 20260601 Predicting the next job title.ipynb  # Jupyter Notebook containing EDA, Feature Engineering, and Model Training
├── fraud_detection.py                            # Streamlit application script for real-time inference
├── fraud_detection_pipeline.pickle               # Serialized Scikit-Learn/XGBoost pipeline
├── DEDA Fraud Detection Courselet Handout.pdf    # Comprehensive technical handout
├── DEDA Fraud Detection Courselet.pdf            # Presentation slides
└── README.md                                     # Project documentation
```

*(Note: The dataset is not included in this repository due to size. Please download it directly from [Kaggle](https://www.kaggle.com/datasets/amanalisiddiqui/fraud-detection-dataset)).*

---

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install required dependencies:**
   ```bash
   pip install numpy pandas matplotlib seaborn scikit-learn xgboost streamlit joblib
   ```

3. **Run the Streamlit App:**
   Ensure `fraud_detection_pipeline.pickle` is in the same directory, then run:
   ```bash
   streamlit run fraud_detection.py
   ```

---

## 👥 Authors & Acknowledgments

**Authors:**
* **Gurpreet Singh** (gurpreet.singh@student.hu-berlin.de) - *Submitter & Developer*
* **Prof. Dr. Wolfgang Karl Härdle** - *Supervisor*

**Institution:**  
Humboldt University of Berlin — DEDA-HUB-Quantlets | theIDA.net — Quantinar.com

**Libraries Used:**  
`Numpy`, `Pandas`, `Matplotlib`, `Seaborn`, `Scikit-Learn`, `XGBoost`, `Streamlit`, `Joblib`

**Version:** 1.0  
**Created On:** 2026-06-29
```
