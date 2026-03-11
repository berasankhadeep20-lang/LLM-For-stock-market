import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

ticker = "AAPL"

data = yf.download(ticker, start="2015-01-01")

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)

# Features
data["return"] = data["Close"].pct_change()
data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()
data["volatility"] = data["return"].rolling(20).std()
data["momentum"] = data["Close"] - data["Close"].shift(10)
data["volume_change"] = data["Volume"].pct_change()

data["future_return"] = data["Close"].shift(-5) / data["Close"] - 1

data = data.dropna()

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

model = RandomForestRegressor(n_estimators=200)
model.fit(X, y)

def realtime_prediction():

    new_data = yf.download(ticker, period="3mo", interval="1d")

    if isinstance(new_data.columns, pd.MultiIndex):
        new_data.columns = new_data.columns.droplevel(1)

    new_data["return"] = new_data["Close"].pct_change()
    new_data["MA20"] = new_data["Close"].rolling(20).mean()
    new_data["MA50"] = new_data["Close"].rolling(50).mean()
    new_data["volatility"] = new_data["return"].rolling(20).std()
    new_data["momentum"] = new_data["Close"] - new_data["Close"].shift(10)
    new_data["volume_change"] = new_data["Volume"].pct_change()

    new_data = new_data.dropna()

    latest = new_data[features].tail(1)

    prediction = model.predict(latest)[0]

    risk = new_data["volatility"].iloc[-1]

    print("Predicted 5-day return:", prediction)
    print("Estimated risk:", risk)

    realtime_prediction()

import schedule
import time

schedule.every(5).minutes.do(realtime_prediction)

while True:
    schedule.run_pending()
    time.sleep(1)