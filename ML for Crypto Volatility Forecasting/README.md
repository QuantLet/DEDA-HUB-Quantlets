<div style="margin: 0; padding: 0; text-align: center; border: none;">
<a href="https://quantlet.com" target="_blank" style="text-decoration: none; border: none;">
<img src="https://github.com/StefanGam/test-repo/blob/main/quantlet_design.png?raw=true" alt="Header Image" width="100%" style="margin: 0; padding: 0; display: block; border: none;" />
</a>
</div>

```
Name of Quantlet: BTC and ETH Realized Volatility Forecasting using Machine Learning

Description: Implementation notebook for forecasting Bitcoin (BTC-USD) realized volatility using different machine learning methods. To prevent temporal data leakage from rolling and lagged features, the pipeline implements a custom Blocked and Purged Time-Series Cross-Validation strategy. The framework generates out-of-fold (OOF) predictions from diverse statistical and machine learning base models—including a Naive baseline, GARCH(1,1), Random Forest, XGBoost, and a Long Short-Term Memory (LSTM) recurrent neural network. A Ridge Regression model serves as the meta-learner for the extended code, blending the individual models' strengths to achieve superior predictive accuracy. The project evaluates performance using RMSE, MAE, and R² metrics, and visualizes model performance comparison alongside the final stacked time-series outputs.

Keywords: volatility forecasting, realized volatility, Bitcoin, BTC-USD, stacking ensemble, meta-learner, Ridge regression, GARCH, LSTM, XGBoost, Random Forest, time-series cross-validation, purged cross-validation, data leakage, out-of-fold predictions, financial econometrics, machine learning in finance, performance benchmarking, visualization

Author: Oliver Viñamata Høyrup

Submitted By: Oliver Viñamata Høyrup

Submitted To: DEDA-Seminar_Courselet

Institution: Humboldt University of Berlin

Email: oliver.vinamata.hoyrup@student.hu-berlin.de

Created On: 2026-06-25

Code Files: `Machine Learning for Cryptocurrency Volatility Forecasting.ipynb`

Data Files: BTC-USD historical price and volume data (log returns and realized volatility calculated in-notebook)

Output Files: Inline notebook outputs (`btc_stacking_timeseries.png`, `btc_full_comparison_with_stacking.png`, model coefficients, and error metrics table)

Libraries: `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `tensorflow`, `xgboost`, `arch`

Programming_Language: Python

Quantlet Class: Application Quantlet

Quantlet Type: Time-Series Analysis, Machine Learning, Financial Econometrics, Visualization

Version: 1.0

```
