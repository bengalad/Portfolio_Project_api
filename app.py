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

# Endpoint to create a new stock
@app.route('/stocks', methods=['POST'])
def create_stock():
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']
    parValue = request.json['parValue']     
    maturityDate = request.json['maturityDate']

    cursor = db.cursor()
   
    cursor.execute("INSERT INTO stocks (id, holdingName, dateOfPurchase, priceAtPurchase, qty, CurrentPrice, parValue, maturityDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, parValue, maturityDate))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Bond added successfully'})


# Endpoint to create a new bond
@app.route('/bonds', methods=['POST'])
def create_bond():
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']

    cursor = db.cursor()
   
    cursor.execute("INSERT INTO bonds (id, holdingName, dateOfPurchase, priceAtPurchase, qty, CurrentPrice) VALUES (%s, %s, %s, %s, %s, %s)",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Bond added successfully'})


# Endpoint to create a new cash
@app.route('/cash', methods=['POST'])
def create_cash():
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    exchAtPurchase = request.json['exchAtPurchase']
    qty = request.json['qty']
    exchCurrent = request.json['exchCurrent']
    currentValue = request.json['currentValue']
    

    cursor = db.cursor()
   
    cursor.execute("INSERT INTO cash (id, holdingName, dateOfPurchase, exchAtPurchase, exchCurrent, qty, currentValue) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (id, holdingName, dateOfPurchase, exchAtPurchase, exchCurrent, qty, currentValue))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Cash added successfully'})

    
@app.route('/products/totalvalue', methods=['GET'])
def gettotalvalue():
    # Calculates the current total value of the portfolio
    cursor = db.cursor()
    cursor.execute('''SELECT SUM(qty*price) as totalValue FROM
                        (SELECT cash.id, cash.qty, cash.currentValue AS price FROM cash
                        UNION
                        SELECT bonds.id, bonds.qty, bonds.currentPrice AS price FROM bonds
                        UNION
                        SELECT stocks.id, stocks.qty, stocks.currentPrice AS price FROM stocks) as combinedTable''')
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)


@app.route('/products/initialvalue', methods=['GET'])
def getinitialvalue():
    # Calculates the current total value of the portfolio
    cursor = db.cursor()
    cursor.execute('''SELECT SUM(qty*price) as initialValue FROM
                        (SELECT cash.id, cash.qty, cash.exchAtPurchase AS price FROM cash
                        UNION
                        SELECT bonds.id, bonds.qty, bonds.priceAtPurchase AS price FROM bonds
                        UNION
                        SELECT stocks.id, stocks.qty, stocks.priceAtPurchase AS price FROM stocks) as combinedTable''')
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)

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

@app.route('/products/stocks/<int:item_id>', methods=['DELETE'])
def delete_stocks(item_id):
    
    cursor = db.cursor(buffered=True)
    cursor.execute("DELETE FROM stocks WHERE id=%s",
                   (item_id,))
    db.commit()
    cursor.close()
    return jsonify({"Message":"Stocks item deleted successfully"})

@app.route('/products/bonds/<int:item_id>', methods=['DELETE'])
def delete_bonds(item_id):
    
    cursor = db.cursor(buffered=True)
    cursor.execute("DELETE FROM bonds WHERE id=%s",
                   (item_id,))
    db.commit()
    cursor.close()
    return jsonify({"Message":"Bonds item deleted successfully"})

@app.route('/products/cash/<int:item_id>', methods=['DELETE'])
def delete_cash(item_id):
    
    cursor = db.cursor(buffered=True)
    cursor.execute("DELETE FROM cash WHERE id=%s",
                   (item_id,))
    db.commit()
    cursor.close()
    return jsonify({"Message":"Cash item deleted successfully"})

if __name__ == '__main__':
    app.debug = True
    app.run()
    
