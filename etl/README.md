# UrbanNexus – ETL Pipeline

This module is responsible for ingesting, validating, transforming, and loading
urban analytics data into the UrbanNexus database.

---

## 📥 Data Sources

| Domain  | Source Type | Notes                           |
| ------- | ----------- | ------------------------------- |
| Weather | Synthetic   | Generated for demo consistency  |
| AQI     | Synthetic   | Constrained to realistic ranges |
| Traffic | Synthetic   | Peak-hour weighted              |
| Health  | Derived     | Computed from AQI + Weather     |

> ⚠️ No raw health data is ingested. Health risk is always derived.

---

## 🔄 ETL Flow

1. **Extract**
   - Load raw datasets (CSV / generator output)
   - Enforce schema presence (no missing columns)

2. **Validate**
   - Type checks (numeric, categorical)
   - Range validation (e.g., AQI 0–500)
   - Null thresholds enforced
   - Pipeline fails fast on invalid data

3. **Transform**
   - Normalize units
   - Aggregate time windows where required
   - Compute derived metrics:
     - `health_risk_index`

4. **Load**
   - Truncate-and-load strategy
   - Idempotent runs
   - Transaction-safe inserts

---

## 🧮 Health Risk Index

Health Risk is derived using:

- AQI severity
- Temperature stress
- Humidity stress

No circular dependencies exist.

---

## ✅ Data Quality Guarantees

- No silent coercion
- No partial loads
- Deterministic synthetic data
- SQL sanity checks post-load

---
