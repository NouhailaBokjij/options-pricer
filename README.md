# Options Pricer — Black-Scholes & Binomial

An interactive web page for pricing financial options using two classic
quantitative finance methods, built from scratch in Python.

## Overview

This project answers a fundamental question in quantitative finance:
**how much is an option worth today?**

It implements and compares two landmark pricing models side by side,
with real-time interactive visualizations.

## Methods Implemented

### 1. Black-Scholes Formula (1973)
Closed-form analytical solution for European options:

- **Call** : C = S·N(d1) - K·e^(-rT)·N(d2)
- **Put**  : P = K·e^(-rT)·N(-d2) - S·N(-d1)

Where :
- d1 = [ln(S/K) + (r + σ²/2)·T] / (σ·√T)
- d2 = d1 - σ·√T

### 2. Binomial Tree — Cox-Ross-Rubinstein (1979)
Numerical method that discretizes time into N=100 steps.
Supports both **European and American** options (early exercise).

## Greeks

| Greek | Meaning | Formula |
|-------|---------|---------|
| Delta Δ | Sensitivity to underlying price | ∂C/∂S = N(d1) |
| Gamma Γ | Rate of change of Delta | ∂²C/∂S² |
| Vega ν | Sensitivity to volatility (+1%) | S·N'(d1)·√T / 100 |
| Theta Θ | Time decay (per calendar day) | ∂C/∂T / 365 |

## Visualizations

- **Price surface** — option price as a function of spot and volatility
- **Intrinsic vs time value** decomposition across all spot prices
- **Real-time comparison** between Black-Scholes and Binomial prices

## Getting Started
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Tech Stack

| Tool | Usage |
|------|-------|
| Python 3.13 | Core language |
| NumPy / SciPy | Mathematical computations |
| Matplotlib | Visualizations |
| Streamlit | Interactive web interface |

## References

- Black, F. & Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities*. Journal of Political Economy.
- Cox, J., Ross, S. & Rubinstein, M. (1979). *Option Pricing: A Simplified Approach*. Journal of Financial Economics.
