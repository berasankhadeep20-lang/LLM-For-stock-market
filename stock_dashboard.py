import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

# -------------------------
# TRAIN MODEL
# -------------------------

ticker = "AAPL"

data = yf.download(ticker, start="2015-01-01")

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
model.fit(X,y)

print("Model trained")

# -------------------------
# DASH APP
# -------------------------

app = dash.Dash(__name__)

app.layout = html.Div([
    
    html.H1("AI Stock Trading Dashboard"),
    
    dcc.Dropdown(
        id="stock-picker",
        options=[
            {"label":"Apple","value":"AAPL"},
            {"label":"Microsoft","value":"MSFT"},
            {"label":"Tesla","value":"TSLA"},
            {"label":"Amazon","value":"AMZN"},
            {"label":"Nvidia","value":"NVDA"},
        ],
        value="AAPL"
    ),

    dcc.Graph(id="price-chart"),

    html.Div(id="prediction-output"),

    dcc.Interval(
        id="update",
        interval=60*1000,  # update every 60 seconds
        n_intervals=0
    )
])

# -------------------------
# UPDATE DASHBOARD
# -------------------------

@app.callback(
    [Output("price-chart","figure"),
     Output("prediction-output","children")],
    
    [Input("stock-picker","value"),
     Input("update","n_intervals")]
)

def update_dashboard(stock, n):

    data = yf.download(stock, period="3mo", interval="1h")

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

    # -------------------------
    # BUY SELL SIGNAL
    # -------------------------

    if prediction > 0.01:
        signal = "BUY"
    elif prediction < -0.01:
        signal = "SELL"
    else:
        signal = "HOLD"

    # -------------------------
    # PLOTLY CHART
    # -------------------------

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        name="Price"
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["MA20"],
        name="MA20"
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["MA50"],
        name="MA50"
    ))

    fig.update_layout(
        title=f"{stock} Price Chart",
        xaxis_title="Time",
        yaxis_title="Price"
    )

    text = f"""
    Predicted Return: {prediction:.4f}
    Risk (Volatility): {risk:.4f}
    Signal: {signal}
    """

    return fig, text

# -------------------------
# RUN SERVER
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)