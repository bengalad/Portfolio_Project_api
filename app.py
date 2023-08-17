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
<<<<<<< HEAD

# Endpoint to create a new stock
@app.route('/stocks', methods=['POST'])
def create_stock():
    
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']


    cursor = db.cursor()
   
    cursor.execute("INSERT INTO stocks (id, holdingName, dateOfPurchase, priceAtPurchase, qty, CurrentPrice) VALUES (%s, %s, %s, %s, %s, %s)",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice))
    
    db.commit()
    cursor.close()
    return jsonify({'message': 'Stock added successfully'})


# Endpoint to create a new bond
@app.route('/bonds', methods=['POST'])
def create_bond():
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']
    parValue = request.json['parValue']     
    maturityDate = request.json['maturityDate']

    cursor = db.cursor()
   
    cursor.execute("INSERT INTO bonds (id, holdingName, dateOfPurchase, priceAtPurchase, qty, CurrentPrice, parValue, maturityDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, parValue, maturityDate))
   
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

=======
>>>>>>> 2b4b8ca2d17545bbaced23f58263657bdc7545c0
    
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


@app.route('/products/totalstocks', methods=['GET'])
def gettotalstocks():
    # Calculates the current total value of all stocks
    cursor = db.cursor()
    cursor.execute('''SELECT SUM(qty*currentPrice) as totalStocks FROM stocks''')
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)


@app.route('/products/totalbonds', methods=['GET'])
def gettotalbonds():
    # Calculates the current total value of all bonds
    cursor = db.cursor()
    cursor.execute('''SELECT SUM(qty*currentPrice) as totalBonds FROM bonds''')
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)


@app.route('/products/totalcash', methods=['GET'])
def gettotalcash():
    # Calculates the current total value of all cash
    cursor = db.cursor()
    cursor.execute('''SELECT SUM(qty*currentValue) as totalCash FROM cash''')
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)


@app.route('/products/initialvalue', methods=['GET'])
def getinitialvalue():
    # Calculates the initial total value of the portfolio
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
<<<<<<< HEAD
    
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
        
        
        
# Endpoint to update an existing bond
@app.route('/bonds/<id>', methods=['PUT'])
def update_bond(id):
    
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']
    parValue = request.json['parValue']     
    maturityDate = request.json['maturityDate']

    cursor = db.cursor()
   
    cursor.execute("UPDATE bonds SET id= %s, holdingName= %s, dateOfPurchase= %s, priceAtPurchase= %s, qty= %s, CurrentPrice= %s, parValue= %s, maturityDate= %s WHERE id = %s",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, parValue, maturityDate, id))
   
    db.commit()
    cursor.close()
    return jsonify({'message': 'Bond updated successfully'})


# Endpoint to update an existing stock
@app.route('/stocks/<id>', methods=['PUT'])
def update_stocks(id):
    
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']
    cursor = db.cursor()
   
   
   
    cursor.execute("UPDATE stocks SET id= %s, holdingName= %s, dateOfPurchase= %s, priceAtPurchase= %s, qty= %s, CurrentPrice= %s WHERE id = %s",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, id))
    

    db.commit()
    cursor.close()
    return jsonify({'message': 'Stock updated successfully'})



# Endpoint to update an existing stock
@app.route('/cash/<id>', methods=['PUT'])
def update_cash(id):
    
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    exchAtPurchase = request.json['exchAtPurchase']
    qty = request.json['qty']
    exchCurrent = request.json['exchCurrent']
    currentValue = request.json['currentValue']
    

    cursor = db.cursor()
   
    cursor.execute("UPDATE cash SET id= %s, holdingName= %s, dateOfPurchase= %s, exchAtPurchase= %s, qty= %s, exchCurrent= %s, currentValue= %s WHERE id = %s",
                   (id, holdingName, dateOfPurchase, exchAtPurchase, exchCurrent, qty, currentValue, id))
    

    db.commit()
    cursor.close()
    return jsonify({'message': 'Cash updated successfully'})


=======
>>>>>>> 2b4b8ca2d17545bbaced23f58263657bdc7545c0

if __name__ == '__main__':
    app.run()
    
