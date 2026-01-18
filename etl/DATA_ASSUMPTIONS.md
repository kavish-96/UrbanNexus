---

## 📄 `DATA_ASSUMPTIONS.md`

```md
# UrbanNexus – Data Assumptions & Limitations

This document clarifies assumptions made in the UrbanNexus data layer.

---

## 1. Synthetic Data

The following datasets are synthetic:

- Weather
- AQI
- Traffic

They are generated to:

- Match real-world ranges
- Preserve logical correlations
- Support demo and evaluation use cases

They are **not** real-time or city-specific.

---

## 2. Health Risk Index

- No real health records are used
- Health risk is a **composite indicator**, not a diagnosis
- Derived exclusively from:
  - AQI
  - Weather conditions

Purpose: trend indication, not medical guidance.

---

## 3. Temporal Assumptions

- Data represents hourly snapshots
- Aggregations assume uniform distribution within windows
- No historical drift modeling

---

## 4. Limitations

- Not suitable for policy enforcement
- Not calibrated against hospital data
- Synthetic correlations may oversimplify reality

---

## 5. Intended Use

- Urban analytics visualization
- Comparative trend analysis
- Educational / demo scenarios
