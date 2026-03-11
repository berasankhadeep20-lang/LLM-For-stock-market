# ------------------------------
# IMPORT LIBRARIES
# ------------------------------

import yfinance as yf
import pandas as pd
import numpy as np

from scipy.optimize import minimize
import matplotlib.pyplot as plt
import plotly.express as px

# ------------------------------
# STOCK LIST
# ------------------------------

stocks = [
"AAPL",
"MSFT",
"NVDA",
"TSLA",
"AMZN"
]

# ------------------------------
# DOWNLOAD DATA
# ------------------------------

data = yf.download(stocks, start="2018-01-01")["Close"]

# ------------------------------
# CALCULATE RETURNS
# ------------------------------

returns = data.pct_change().dropna()

# ------------------------------
# EXPECTED RETURNS & COVARIANCE
# ------------------------------

mean_returns = returns.mean()

cov_matrix = returns.cov()

# ------------------------------
# PORTFOLIO PERFORMANCE FUNCTION
# ------------------------------

def portfolio_performance(weights):

    portfolio_return = np.sum(mean_returns * weights)

    portfolio_std = np.sqrt(
        np.dot(weights.T,
        np.dot(cov_matrix, weights))
    )

    return portfolio_return, portfolio_std


# ------------------------------
# NEGATIVE SHARPE RATIO
# ------------------------------

def negative_sharpe(weights):

    ret, std = portfolio_performance(weights)

    sharpe = ret / std

    return -sharpe


# ------------------------------
# CONSTRAINTS
# ------------------------------

num_assets = len(stocks)

constraints = (
{'type':'eq','fun': lambda x: np.sum(x)-1}
)

bounds = tuple((0,1) for asset in range(num_assets))

initial_weights = num_assets * [1./num_assets]

# ------------------------------
# OPTIMIZATION
# ------------------------------

optimal = minimize(
negative_sharpe,
initial_weights,
method='SLSQP',
bounds=bounds,
constraints=constraints
)

optimal_weights = optimal.x

# ------------------------------
# DISPLAY RESULTS
# ------------------------------

print("\nOptimal Portfolio Allocation\n")

for i, stock in enumerate(stocks):

    print(stock,":",round(optimal_weights[i]*100,2),"%")

ret, risk = portfolio_performance(optimal_weights)

print("\nExpected Portfolio Return:", round(ret*100,2),"%")
print("Portfolio Risk (Volatility):", round(risk*100,2),"%")
print("Sharpe Ratio:", round(ret/risk,2))

# ------------------------------
# PORTFOLIO PIE CHART
# ------------------------------

fig = px.pie(
names=stocks,
values=optimal_weights,
title="Optimized Portfolio Allocation"
)

fig.show()