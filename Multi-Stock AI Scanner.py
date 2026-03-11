import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# ---------------------
# STOCK LIST
# ---------------------

stocks = [
    "AAPL",
    "MSFT",
    "TSLA",
    "AMZN",
    "NVDA",
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS"
]

features = [
    "return",
    "MA20",
    "MA50",
    "volatility",
    "momentum",
    "volume_change"
]

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=6,
    random_state=42
)

# ---------------------
# TRAIN MODEL USING FIRST STOCK
# ---------------------

train_stock = stocks[0]

data = yf.download(train_stock, start="2015-01-01")

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)

data["return"] = data["Close"].pct_change()
data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()
data["volatility"] = data["return"].rolling(20).std()
data["momentum"] = data["Close"] - data["Close"].shift(10)
data["volume_change"] = data["Volume"].pct_change()

data["future_return"] = data["Close"].shift(-5) / data["Close"] - 1

data = data.dropna()

X = data[features]
y = data["future_return"]

model.fit(X, y)

print("Model trained.")

# ---------------------
# STOCK SCANNER
# ---------------------

results = []

for ticker in stocks:

    try:

        data = yf.download(ticker, period="3mo")

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)

        data["return"] = data["Close"].pct_change()
        data["MA20"] = data["Close"].rolling(20).mean()
        data["MA50"] = data["Close"].rolling(50).mean()
        data["volatility"] = data["return"].rolling(20).std()
        data["momentum"] = data["Close"] - data["Close"].shift(10)
        data["volume_change"] = data["Volume"].pct_change()

        data = data.dropna()

        latest = data[features].tail(1)

        prediction = model.predict(latest)[0]

        risk = data["volatility"].iloc[-1]

        results.append({
            "Stock": ticker,
            "Predicted_Return": prediction,
            "Risk": risk
        })

    except:
        print("Error with", ticker)

# ---------------------
# RANK STOCKS
# ---------------------

results_df = pd.DataFrame(results)

results_df["Score"] = results_df["Predicted_Return"] / results_df["Risk"]

results_df = results_df.sort_values(
    by="Score",
    ascending=False
)

print("\nTop Opportunities:\n")

print(results_df)