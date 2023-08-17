from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="c0nygre",
    database="portfolio"
)

@app.route('/products', methods=['GET'])
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


@app.route('/products', methods=['GET'])
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
def getAllProducts():
    cursor = db.cursor()
    query = """SELECT id, holdingName, dateOfPurchase, priceAtPurchase, currentPrice, qty FROM stocks UNION 
    SELECT id, holdingName, dateOfPurchase, priceAtPurchase, currentPrice, qty FROM bonds UNION 
    SELECT id, holdingName, dateOfPurchase, exchAtPurchase*qty AS priceAtPurchase, currentValue, qty FROM cash"""
    cursor.execute(query)
    allProducts = cursor.fetchall()
    return jsonify(allProducts)

if __name__ = '__main__':
    app.run()
    
