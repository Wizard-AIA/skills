---
name: time-series-forecasting
description: Principles for time-series decomposition, seasonality modeling, baseline benchmarking, and out-of-sample validation
tags: [time-series, forecasting, trend, seasonality, statsmodels]
version: 1.0
---

## When to use this

Any analytical inquiry requiring historical trend decomposition, forward projections, seasonality modeling, or forecasting future intervals. "Forecast sales for next month", "is there weekly seasonality in revenue", "project quarterly churn rate".

The code snippets below use `"date"` and `"value"` as representative column names. Always substitute the actual time and metric columns from the dataset.

## 1. Ensure monotonic datetime index and uniform frequency

Before fitting any statistical model, verify that dates are parsed, ordered chronologically, and resampled to a consistent frequency:

```python
df["date"] = pd.to_datetime(df["date"])
ts = df.set_index("date")["value"].sort_index()

# Ensure uniform sampling frequency (e.g. daily 'D', monthly 'MS', weekly 'W')
ts = ts.asfreq("D").interpolate(method="time")
```

## 2. Benchmark against simple naive baselines

Never report advanced model forecasts without comparing them against a trivial baseline (e.g., Seasonal Naive or Last Observed Value):

```python
# Naive baseline (last value)
naive_forecast = ts.iloc[-1]

# Seasonal naive baseline (lag-7 or lag-12)
seasonal_naive_forecast = ts.iloc[-7]
```

## 3. Decompose trend, seasonality, and residual variance

Inspect whether variance expands with level (multiplicative) or remains constant (additive):

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Decompose time series
decomposition = seasonal_decompose(ts, model="additive", period=7)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid
```

## 4. Rigorous out-of-sample backtesting

Do not evaluate model metrics on random train/test splits. Always split temporally to prevent future data leakage:

```python
cutoff = int(len(ts) * 0.8)
train, test = ts.iloc[:cutoff], ts.iloc[cutoff:]

# Fit exponential smoothing or ARIMA on training portion only
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(train, seasonal_periods=7, trend="add", seasonal="add").fit()
predictions = model.forecast(len(test))

# Evaluate MAPE and RMSE
rmse = np.sqrt(np.mean((test - predictions) ** 2))
mape = np.mean(np.abs((test - predictions) / test)) * 100
```

## 5. What to report

1. The detected seasonality period (e.g., 7-day cyclicality, 12-month seasonality).
2. The directional trend (annualized growth / decline rate).
3. Forecast numbers along with calculated confidence intervals (80% and 95% bounds).
4. Out-of-sample accuracy metric (RMSE/MAPE) compared against the baseline.
