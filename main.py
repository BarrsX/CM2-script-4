import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm


# Black-Scholes model for European option
def european_option_price(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        price = S * stats.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * stats.norm.cdf(
            d2, 0.0, 1.0
        )
    elif option_type == "put":
        price = K * np.exp(-r * T) * stats.norm.cdf(-d2, 0.0, 1.0) - S * stats.norm.cdf(
            -d1, 0.0, 1.0
        )
    return price


# Binomial Tree model for American option
def american_option_price(S, K, T, r, sigma, N, option_type="call"):
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    price_tree = np.zeros([N + 1, N + 1])
    for i in range(N + 1):
        for j in range(i + 1):
            if option_type == "call":
                price_tree[j, i] = max(S * (u ** (i - j)) * (d**j) - K, 0)
            elif option_type == "put":
                price_tree[j, i] = max(K - S * (u ** (i - j)) * (d**j), 0)
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            price_tree[j, i] = np.exp(-r * dt) * (
                p * price_tree[j, i + 1] + (1 - p) * price_tree[j + 1, i + 1]
            )
    return price_tree[0, 0]


# Monte Carlo simulation for option prices
def simulate_option_prices(S, K, T, r, sigma, num_simulations, option_type="call"):
    prices = []
    for _ in range(num_simulations):
        ST = S * np.exp(
            (r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * np.random.standard_normal()
        )
        if option_type == "call":
            prices.append(max(ST - K, 0))
        elif option_type == "put":
            prices.append(max(K - ST, 0))
    return np.array(prices)


# QQ plot
def qq_plot(data):
    sm.qqplot(data, line="s")
    plt.show()


# Simulate option prices
simulated_prices = simulate_option_prices(
    S=100, K=100, T=1, r=0.05, sigma=0.2, num_simulations=10000
)

# QQ plot
qq_plot(simulated_prices)
