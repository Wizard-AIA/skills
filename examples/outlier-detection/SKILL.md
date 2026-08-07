---
name: outlier-detection
description: Choosing a detection method that matches the data's actual distribution, and deciding what to do with a flagged point
tags: [outliers, anomaly-detection, statistics, data-quality]
version: 1.0
---

## When to use this

Any question that involves "find the outliers," "are there any anomalies,"
or a modeling task where extreme values are silently distorting a mean, a
regression coefficient, or a scaler. The snippets below name their column
`"value"` — substitute the real column name from the data in front of you.

## The method has to match the distribution — check first

The two most common methods answer different questions and give visibly
different results on skewed data:

- **Z-score** assumes the data is roughly normal. On a skewed distribution
  (income, latency, most count data) it under-flags outliers on the long
  tail and over-flags them on the short side, because it's measuring
  distance from a mean that skew has already pulled off-center.
- **IQR (interquartile range)** makes no distributional assumption — it's
  based on quartiles, so it's the safer default when you haven't checked the
  shape yet.

```python
from scipy import stats

# Quick skew check before picking a method
skewness = df["value"].skew()
is_roughly_normal = abs(skewness) < 0.5
```

If `is_roughly_normal` is false, prefer IQR over Z-score, or transform the
data (a log transform is the usual first move for right-skewed data) before
using Z-score.

## IQR method

```python
q1, q3 = df["value"].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df["value"] < lower) | (df["value"] > upper)]
```

`1.5` is the conventional multiplier; `3.0` is the common choice for
flagging only "extreme" outliers rather than all mild ones — state which one
you used, since the two give substantially different counts on the same
data.

## Z-score method (normal-ish data only)

```python
z_scores = stats.zscore(df["value"].dropna())
outliers = df.loc[df["value"].dropna().index[abs(z_scores) > 3]]
```

`3` standard deviations is conventional; note explicitly that `dropna()`
happened before scoring, or the index alignment between `z_scores` and `df`
silently breaks on any missing values.

## A flagged point is not automatically wrong

The step after detection is a judgment call, and it changes the answer more
than the detection method does:

- **A data error** (a typo, a unit mismatch, a sensor fault) — correct it or
  drop it, and say which.
- **A real extreme value** (a genuine top customer, a real fraud case) — this
  is often the most important row in the dataset, not noise to remove.
  Dropping it silently because it's statistically an outlier can delete the
  actual finding.

Never drop flagged points without stating how many were removed and why —
this is exactly the kind of silent decision Wizard's own trust layer
surfaces alongside an answer, and a skill should hold itself to the same
standard.

## What to report

- which method was used (IQR or Z-score) and its threshold (1.5/3.0 IQR
  multiplier, or 3 standard deviations)
- how many points were flagged, as a count and a percentage of the dataset
- for each flagged point (or a representative sample, if there are many):
  data error vs. real extreme value, and what was done about it
- the count actually removed, if any were — never silently filtered
