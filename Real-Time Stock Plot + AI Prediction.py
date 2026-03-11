import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

from sklearn.ensemble import RandomForestRegressor

# -------------------------
# STOCK LIST
# -------------------------

stocks = ["AAPL","MSFT","TSLA","AMZN","NVDA"]

features = [
    "return",
    "MA20",
    "MA50",
    "volatility",
    "momentum",
    "volume_change"
]

# -------------------------
# TRAIN MODEL
# -------------------------

train_stock = "AAPL"

data = yf.download(train_stock, start="2015-01-01")

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)

data["return"] = data["Close"].pct_change()
data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()
data["volatility"] = data["return"].rolling(20).std()
data["momentum"] = data["Close"] - data["Close"].shift(10)
data["volume_change"] = data["Volume"].pct_change()

data["future_return"] = data["Close"].shift(-5)/data["Close"] - 1

data = data.dropna()

X = data[features]
y = data["future_return"]

model = RandomForestRegressor(n_estimators=200)
model.fit(X,y)

print("Model trained")

# -------------------------
# REAL TIME ANALYSIS
# -------------------------

def analyze_stock(ticker):

    data = yf.download(ticker, period="5d", interval="5m")

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

    print("\nStock:", ticker)
    print("Predicted Return:", prediction)
    print("Estimated Risk:", risk)

    # -------------------------
    # PLOT STOCK PRICE
    # -------------------------

    plt.figure(figsize=(10,5))

    plt.plot(data["Close"], label="Price")

    plt.plot(data["MA20"], label="MA20")

    plt.title(f"{ticker} Real-Time Price")

    plt.legend()

    plt.show()


# -------------------------
# RUN ANALYSIS
# -------------------------

for stock in stocks:

    analyze_stock(stock)

while True:

    for stock in stocks:
        analyze_stock(stock)

    time.sleep(6)