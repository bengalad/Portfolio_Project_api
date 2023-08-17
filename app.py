from flask import Flask, jsonify, request
import mysql.connector
import yfinance as yf
import pandas as pd

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="c0nygre",
    database="portfolio"
)

@app.route('/products/<string:ticker>', methods=['GET'])
def get_historical_prices(ticker):
    # Retrieve the item with the given ticker from yahoo finance
    product = yf.Ticker(ticker)
    
    # getting historical market data
    hist = product.history(period="1mo")
    
    if not hist.empty:
        # Return the item as JSON
        return hist.to_json()
    else:
        return jsonify({"Error":"Ticker data not found"}), 404
    

if __name__ == '__main__':
    app.run()