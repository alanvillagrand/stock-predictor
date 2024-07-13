from flask import Flask, request, jsonify, render_template
import yfinance as yf
from sklearn.linear_model import LinearRegression
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    ticker = data['ticker']
    stock_data = yf.download(ticker, start='2010-01-01', end='2020-01-01')
    stock_data['Returns'] = stock_data['Adj Close'].pct_change()
    stock_data['MA10'] = stock_data['Adj Close'].rolling(window=10).mean()
    stock_data['MA50'] = stock_data['Adj Close'].rolling(window=50).mean()
    stock_data = stock_data.dropna()

    features = stock_data[['MA10', 'MA50', 'Returns']]
    target = stock_data['Adj Close']

    model = LinearRegression()
    model.fit(features[:-1], target[:-1])

    prediction = model.predict(features[-1:])
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
