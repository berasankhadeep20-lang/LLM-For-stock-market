import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# -------------------------
# 1 Download stock data
# -------------------------

ticker = "AAPL"

data = yf.download(ticker, start="2015-01-01", end="2024-01-01")

# Fix multi-index columns
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)

# -------------------------
# 2 Feature Engineering
# -------------------------

data["return"] = data["Close"].pct_change()

data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()

data["volatility"] = data["return"].rolling(20).std()

data["momentum"] = data["Close"] - data["Close"].shift(10)

data["volume_change"] = data["Volume"].pct_change()

# -------------------------
# 3 Prediction Target
# -------------------------

data["future_return"] = data["Close"].shift(-5) / data["Close"] - 1

data = data.dropna()

# -------------------------
# 4 Feature Selection
# -------------------------

features = [
    "return",
    "MA20",
    "MA50",
    "volatility",
    "momentum",
    "volume_change"
]

X = data[features]
y = data["future_return"]

# -------------------------
# 5 Train Test Split
# -------------------------

split = int(len(data) * 0.8)

X_train = X[:split]
X_test = X[split:]

y_train = y[:split]
y_test = y[split:]

# -------------------------
# 6 Train ML Model
# -------------------------

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

# -------------------------
# 7 Model Prediction
# -------------------------

predictions = model.predict(X_test)

mse = mean_squared_error(y_test, predictions)

print("Model Error (MSE):", mse)

# -------------------------
# 8 Risk Prediction
# -------------------------

latest_volatility = data["volatility"].iloc[-1]

print("Estimated Risk (volatility):", latest_volatility)

# -------------------------
# 9 Backtesting Setup
# -------------------------

test_data = data.iloc[split:].copy()

test_data["predicted_return"] = predictions

# Trading rule
test_data["signal"] = 0
test_data.loc[test_data["predicted_return"] > 0, "signal"] = 1

# -------------------------
# 10 Strategy Returns
# -------------------------

test_data["actual_return"] = test_data["Close"].pct_change()

test_data["strategy_return"] = (
    test_data["signal"].shift(1) * test_data["actual_return"]
)

# -------------------------
# 11 Cumulative Returns
# -------------------------

test_data["market_cumulative"] = (
    1 + test_data["actual_return"]
).cumprod()

test_data["strategy_cumulative"] = (
    1 + test_data["strategy_return"]
).cumprod()

# -------------------------
# 12 Performance Metrics
# -------------------------

market_return = test_data["market_cumulative"].iloc[-1] - 1
strategy_return = test_data["strategy_cumulative"].iloc[-1] - 1

print("Market Return:", market_return)
print("Strategy Return:", strategy_return)

# Sharpe ratio

sharpe = (
    test_data["strategy_return"].mean() /
    test_data["strategy_return"].std()
)

print("Sharpe Ratio:", sharpe)

# Maximum Drawdown

rolling_max = test_data["strategy_cumulative"].cummax()

drawdown = (
    test_data["strategy_cumulative"] - rolling_max
) / rolling_max

print("Max Drawdown:", drawdown.min())

# -------------------------
# 13 Plot Backtest Results
# -------------------------

plt.figure(figsize=(10,5))

plt.plot(
    test_data["market_cumulative"],
    label="Market"
)

plt.plot(
    test_data["strategy_cumulative"],
    label="ML Strategy"
)

plt.title("Backtesting Results")

plt.legend()

plt.show()

# -------------------------
# 14 Future Prediction
# -------------------------

latest_features = X.tail(1)

predicted_return = model.predict(latest_features)

print("Predicted 5-day return:", predicted_return[0])