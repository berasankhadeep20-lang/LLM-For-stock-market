<h1 align="center">📈 AI Stock Prediction & Trading Dashboard</h1>

<p align="center">
A Machine Learning based stock analysis system that performs 
<strong>real-time market analysis, risk prediction, return forecasting, and trading signal detection</strong>.
</p>

<hr>

<h2>🚀 Project Overview</h2>

<p>
This project builds a <strong>Machine Learning powered stock analysis system</strong> using Python.
It downloads real market data, extracts financial indicators, predicts future returns,
estimates risk, and visualizes results through an interactive web dashboard.
</p>

<p>
The system automatically:
</p>

<ul>
<li>Fetches real-time stock data</li>
<li>Extracts financial indicators</li>
<li>Predicts stock returns using Machine Learning</li>
<li>Calculates market risk (volatility)</li>
<li>Detects Buy / Sell / Hold signals</li>
<li>Displays interactive charts in a browser dashboard</li>
</ul>

<hr>

<h2>🧠 Machine Learning Model</h2>

<p>
The prediction model uses a <b>Random Forest Regressor</b> trained on historical stock data.
</p>

<p>The model learns relationships between financial indicators and future stock returns.</p>

<p><strong>Features used in the model:</strong></p>

<ul>
<li>Daily Returns</li>
<li>20-day Moving Average (MA20)</li>
<li>50-day Moving Average (MA50)</li>
<li>Volatility</li>
<li>Momentum</li>
<li>Volume Change</li>
</ul>

<p>
The model predicts the <strong>expected 5-day return</strong> of a stock.
</p>

<hr>

<h2>📊 Features</h2>

<ul>
<li>📡 Real-time stock data analysis</li>
<li>🤖 Machine Learning price prediction</li>
<li>⚠ Risk estimation using volatility</li>
<li>📈 Interactive price charts</li>
<li>📊 Moving average trend analysis</li>
<li>💰 Automatic Buy / Sell / Hold signal detection</li>
<li>🌐 Live dashboard running in a web browser</li>
</ul>

<hr>

<h2>🖥 Dashboard</h2>

<p>
The project includes a live web dashboard built using Plotly Dash.
</p>

<p>The dashboard displays:</p>

<ul>
<li>Interactive stock charts</li>
<li>Predicted return values</li>
<li>Estimated market risk</li>
<li>Buy / Sell trading signals</li>
</ul>

<p>
Charts automatically update with live market data.
</p>

<hr>

<h2>⚙ Technologies Used</h2>

<ul>
<li>Python</li>
<li>Pandas</li>
<li>NumPy</li>
<li>Scikit-Learn</li>
<li>Plotly</li>
<li>Dash</li>
<li>Yahoo Finance API</li>
</ul>

<hr>

<h2>📦 Installation</h2>

<p>Clone the repository:</p>

<pre>
git clone https://github.com/yourusername/stock-ai-dashboard.git
cd stock-ai-dashboard
</pre>

<p>Install dependencies:</p>

<pre>
pip install dash plotly yfinance pandas numpy scikit-learn
</pre>

<hr>

<h2>▶ Running the Project</h2>

<p>Run the dashboard:</p>

<pre>
python stock_dashboard.py
</pre>

<p>Open your browser and go to:</p>

<pre>
http://127.0.0.1:8050
</pre>

<hr>

<h2>📂 Project Structure</h2>

<pre>
stock-ai-dashboard/
│
├── data_download.py
├── model_training.py
├── realtime_prediction.py
├── backtesting.py
├── stock_dashboard.py
│
└── README.md
</pre>

<hr>

<h2>📊 Example Output</h2>

<ul>
<li>Predicted Return: 0.008</li>
<li>Risk (Volatility): 0.011</li>
<li>Signal: BUY</li>
</ul>

<hr>

<h2>⚠ Disclaimer</h2>

<p>
This project is for <strong>educational and research purposes only</strong>.
It should not be used as financial advice or for real trading decisions.
Stock markets involve risk and unpredictable behavior.
</p>

<hr>

<h2>👨‍💻 Author</h2>

<p>
<strong>Sankhadeep Bera</strong>
</p>

<p>
YouTube: <a href="https://youtube.com/@05sankhadeepbera78">@05sankhadeepbera78</a>
</p>

<hr>

<h2>⭐ If you like this project</h2>

<p>
Give the repository a ⭐ on GitHub!
</p>