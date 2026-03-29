import numpy as np
from scipy.stats import norm

def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def bs_price(S, K, T, r, sigma, option_type="call"):
    _d1 = d1(S, K, T, r, sigma)
    _d2 = d2(S, K, T, r, sigma)
    if option_type == "call":
        price = S * norm.cdf(_d1) - K * np.exp(-r * T) * norm.cdf(_d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-_d2) - S * norm.cdf(-_d1)
    return price

def greeks(S, K, T, r, sigma, option_type="call"):
    _d1 = d1(S, K, T, r, sigma)
    _d2 = d2(S, K, T, r, sigma)
    delta = norm.cdf(_d1) if option_type == "call" else -norm.cdf(-_d1)
    gamma = norm.pdf(_d1) / (S * sigma * np.sqrt(T))
    vega  = S * norm.pdf(_d1) * np.sqrt(T) / 100
    theta_call = (- (S * norm.pdf(_d1) * sigma) / (2 * np.sqrt(T))
                  - r * K * np.exp(-r * T) * norm.cdf(_d2))
    theta = theta_call if option_type == "call" else (
            theta_call + r * K * np.exp(-r * T))
    theta = theta / 365
    return {"Delta": round(delta, 4),
            "Gamma": round(gamma, 4),
            "Vega":  round(vega,  4),
            "Theta": round(theta, 4)}

def binomial_price(S, K, T, r, sigma, N=100, option_type="call", american=False):
    dt = T / N
    u  = np.exp(sigma * np.sqrt(dt))
    d  = 1 / u
    p  = (np.exp(r * dt) - d) / (u - d)
    ST = np.array([S * u**j * d**(N - j) for j in range(N + 1)])
    if option_type == "call":
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)
    for i in range(N - 1, -1, -1):
        payoff = np.exp(-r * dt) * (p * payoff[1:i+2] + (1 - p) * payoff[0:i+1])
        if american:
            ST = np.array([S * u**j * d**(i - j) for j in range(i + 1)])
            intrinsic = np.maximum(ST - K, 0) if option_type == "call" else np.maximum(K - ST, 0)
            payoff = np.maximum(payoff, intrinsic)
    return round(payoff[0], 4)