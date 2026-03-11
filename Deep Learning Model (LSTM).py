import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# ------------------------
# DOWNLOAD DATA
# ------------------------

ticker = "AAPL"

data = yf.download(ticker, start="2015-01-01")

# Fix multi-index issue
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)

close_prices = data["Close"]

# ------------------------
# SCALE DATA
# ------------------------

scaler = MinMaxScaler(feature_range=(0,1))

scaled_data = scaler.fit_transform(close_prices.values.reshape(-1,1))

# ------------------------
# CREATE TRAINING DATA
# ------------------------

window = 20

X = []
y = []

for i in range(window, len(scaled_data)):
    X.append(scaled_data[i-window:i])
    y.append(scaled_data[i])

X = np.array(X)
y = np.array(y)

# ------------------------
# BUILD LSTM MODEL
# ------------------------

model = Sequential()

model.add(LSTM(64, return_sequences=True, input_shape=(X.shape[1],1)))
model.add(LSTM(32))
model.add(Dense(1))

model.compile(
    optimizer="adam",
    loss="mean_squared_error"
)

# ------------------------
# TRAIN MODEL
# ------------------------

model.fit(
    X,
    y,
    epochs=10,
    batch_size=32
)

print("Model training complete")

# ------------------------
# PREDICT NEXT PRICE
# ------------------------

last_20_days = scaled_data[-window:]

last_20_days = last_20_days.reshape(1,window,1)

prediction = model.predict(last_20_days)

predicted_price = scaler.inverse_transform(prediction)

print("Predicted next price:", predicted_price[0][0])

import matplotlib.pyplot as plt

predictions = model.predict(X)

predictions = scaler.inverse_transform(predictions)
actual = scaler.inverse_transform(y)

plt.plot(actual,label="Actual")
plt.plot(predictions,label="Predicted")

plt.legend()
plt.show()