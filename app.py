from flask import Flask, request, jsonify, render_template
import yfinance as yf
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ticker = request.form['ticker']
    data = yf.download(ticker, start='2010-01-01', end='2020-01-01')
    data['Returns'] = data['Adj Close'].pct_change()
    data['MA10'] = data['Adj Close'].rolling(window=10).mean()
    data['MA50'] = data['Adj Close'].rolling(window=50).mean()
    data = data.dropna()

    features = data[['MA10', 'MA50', 'Returns']]
    target = data['Adj Close']

    model = LinearRegression()
    model.fit(features[:-1], target[:-1])

    prediction = model.predict(features[-1:])
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
