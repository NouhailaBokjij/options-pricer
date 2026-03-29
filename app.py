import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from black_scholes import bs_price, greeks, binomial_price

st.set_page_config(page_title="Options Pricer", page_icon="📈", layout="wide")
st.title("📈 Options Pricer — Black-Scholes & Binomial")
st.caption("Projet personnel — MS Finance & Gestion des Risques | ENSAE Paris")

# --- Sidebar : paramètres ---
st.sidebar.header("Paramètres")
S     = st.sidebar.slider("Spot S",               10,  500, 100)
K     = st.sidebar.slider("Strike K",             10,  500, 100)
T     = st.sidebar.slider("Maturité T (ans)",    0.1,  3.0, 1.0, step=0.1)
r     = st.sidebar.slider("Taux sans risque (%)", 0.0, 10.0, 5.0) / 100
sigma = st.sidebar.slider("Volatilité σ (%)",     1.0, 80.0, 20.0) / 100
opt   = st.sidebar.radio("Type", ["call", "put"])
american = st.sidebar.checkbox("Option américaine (binomial)")

# --- Prix ---
bs   = bs_price(S, K, T, r, sigma, opt)
bin_ = binomial_price(S, K, T, r, sigma, N=100, option_type=opt, american=american)
g    = greeks(S, K, T, r, sigma, opt)

col1, col2, col3 = st.columns(3)
col1.metric("Prix Black-Scholes",      f"{bs:.4f} €")
col2.metric("Prix Binomial (N=100)",   f"{bin_:.4f} €")
col3.metric("Écart BS vs Binomial",    f"{abs(bs - bin_):.6f} €")

# --- Greeks ---
st.subheader("Greeks")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Delta Δ", g["Delta"])
c2.metric("Gamma Γ", g["Gamma"])
c3.metric("Vega  ν", g["Vega"])
c4.metric("Theta Θ", g["Theta"])

# --- Surface de prix ---
st.subheader("Prix en fonction du spot et de la volatilité")
spots  = np.linspace(50, 150, 40)
sigmas = np.linspace(0.05, 0.60, 40)
Z = np.array([[bs_price(s, K, T, r, v, opt) for v in sigmas] for s in spots])

fig, ax = plt.subplots(figsize=(8, 4))
cp = ax.contourf(sigmas * 100, spots, Z, levels=20, cmap="RdYlGn")
fig.colorbar(cp, ax=ax, label="Prix de l'option (€)")
ax.set_xlabel("Volatilité σ (%)")
ax.set_ylabel("Spot S")
ax.set_title(f"Surface de prix — {opt.upper()} (K={K}, T={T})")
st.pyplot(fig)

# --- Valeur intrinsèque vs valeur temps ---
st.subheader("Valeur intrinsèque vs valeur temps")
spots2 = np.linspace(50, 200, 200)
prices = [bs_price(s, K, T, r, sigma, opt) for s in spots2]
if opt == "call":
    intrinsic = np.maximum(spots2 - K, 0)
else:
    intrinsic = np.maximum(K - spots2, 0)
time_value = np.array(prices) - intrinsic

fig2, ax2 = plt.subplots(figsize=(8, 3))
ax2.plot(spots2, prices,    label="Prix total",         color="#2196F3")
ax2.plot(spots2, intrinsic, label="Valeur intrinsèque", color="#4CAF50", linestyle="--")
ax2.fill_between(spots2, intrinsic, prices, alpha=0.15, color="#FF9800", label="Valeur temps")
ax2.axvline(K, color="gray", linestyle=":", linewidth=1, label=f"Strike K={K}")
ax2.axvline(S, color="red",  linestyle=":", linewidth=1, label=f"Spot S={S}")
ax2.set_xlabel("Spot S")
ax2.set_ylabel("Prix (€)")
ax2.legend(fontsize=8)
ax2.set_title(f"Décomposition du prix — {opt.upper()}")
st.pyplot(fig2)

st.caption("Black-Scholes (1973) | Cox-Ross-Rubinstein (1979)")