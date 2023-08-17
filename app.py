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

# Gets a table of all stocks, bonds and cash showing ID, Name, Date of purchase, 
# price at purchase, current value and quantity 
@app.route('/products', methods=['GET'])
def getAllProducts():
    cursor = db.cursor()
    query = """SELECT id, holdingName, dateOfPurchase, priceAtPurchase, currentPrice, qty FROM stocks UNION 
    SELECT id, holdingName, dateOfPurchase, priceAtPurchase, currentPrice, qty FROM bonds UNION 
    SELECT id, holdingName, dateOfPurchase, exchAtPurchase*qty AS priceAtPurchase, currentValue, qty FROM cash"""
    cursor.execute(query)
    allProducts = cursor.fetchall()
    cursor.close()
    return jsonify(allProducts)

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
    
# [('AMAZ',), ('GOOG',), ('EUR',)]
@app.route('/refresh', methods=['GET'])
def refreshData():
    cursor = db.cursor()
    query = "SELECT ticker FROM holdings"
    cursor.execute(query)
    tickers = cursor.fetchall()
    for i in tickers:
        ticker = i[0]
        info = yf.Ticker(ticker)

if __name__ == '__main__':
    app.debug = True
    app.run()
    
