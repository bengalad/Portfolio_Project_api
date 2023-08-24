from flask import Flask, jsonify, request
import mysql.connector
import yfinance as yf
from datetime import date
from dateutil import relativedelta
from flask_cors import CORS

# Create the application instance and set the static folder so i don't have to put the path to the static folder in the URL
app = Flask(__name__, static_url_path='/../Portfolio_Project_ui', static_folder='static')

# add cors support so i can use this with a frontend
CORS(app, crossorigin=True, resources="*")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="c0nygre",
    database="portfolio"
)

# Endpoint to create a new stock
@app.route('/stocks', methods=['POST'])
def create_stock():
    db.reconnect(attempts=1, delay=0)
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']
    ticker = request.json['ticker']
    cursor = db.cursor()
   
    cursor.execute("INSERT INTO stocks (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, ticker) VALUES (%s, %s, %s, %s, %s, %s, %s )",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, ticker))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Stock added successfully'})


# Endpoint to create a new bond
@app.route('/bonds', methods=['POST'])
def create_bond():
    db.reconnect(attempts=1, delay=0)
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']
    parValue = request.json['parValue']     
    maturityDate = request.json['maturityDate']
    coupon = request.json['coupon']
    discountRate = request.json['discountRate']

    cursor = db.cursor()
   
    cursor.execute("INSERT INTO bonds (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, parValue, maturityDate, coupon, discountRate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, parValue, maturityDate, coupon, discountRate))
   
    db.commit()
    cursor.close()
    return jsonify({'message': 'Bond added successfully'})


# Endpoint to create a new cash
@app.route('/cash', methods=['POST'])
def create_cash():
    db.reconnect(attempts=1, delay=0)
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    exchAtPurchase = request.json['exchAtPurchase']
    qty = request.json['qty']
    exchCurrent = request.json['exchCurrent']
    currentValue = request.json['currentValue']
    ticker = request.json['ticker']
    
    cursor = db.cursor()
   
    cursor.execute("INSERT INTO cash (id, holdingName, dateOfPurchase, exchAtPurchase, exchCurrent, qty, currentValue, ticker) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (id, holdingName, dateOfPurchase, exchAtPurchase, exchCurrent, qty, currentValue, ticker))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Cash added successfully'})

 
@app.route('/products/totalvalue', methods=['GET'])
def gettotalvalue():
    # Calculates the current total value of the portfolio
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor()
    cursor.execute('''SELECT SUM(qty*price) as totalValue FROM
                        (SELECT cash.id, cash.qty, cash.exchCurrent AS price FROM cash
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
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor()
    cursor.execute('''SELECT SUM(qty*currentPrice) as totalStocks FROM stocks''')
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)


@app.route('/products/totalbonds', methods=['GET'])
def gettotalbonds():
    # Calculates the current total value of all bonds
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor()
    cursor.execute('''SELECT SUM(qty*currentPrice) as totalBonds FROM bonds''')
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)


@app.route('/products/totalcash', methods=['GET'])
def gettotalcash():
    # Calculates the current total value of all cash
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor()
    cursor.execute('''SELECT SUM(qty*exchCurrent) as totalCash FROM cash''')
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)


@app.route('/products/initialvalue', methods=['GET'])
def getinitialvalue():
    # Calculates the initial total value of the portfolio
    db.reconnect(attempts=1, delay=0)
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
    db.reconnect(attempts=1, delay=0)
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

@app.route('/products/stocks/<int:item_id>', methods=['DELETE'])
def delete_stocks(item_id):
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor(buffered=True)
    cursor.execute("DELETE FROM stocks WHERE id=%s",
                   (item_id,))
    db.commit()
    cursor.close()
    return jsonify({"Message":"Stocks item deleted successfully"})

@app.route('/products/bonds/<int:item_id>', methods=['DELETE'])
def delete_bonds(item_id):
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor(buffered=True)
    cursor.execute("DELETE FROM bonds WHERE id=%s",
                   (item_id,))
    db.commit()
    cursor.close()
    return jsonify({"Message":"Bonds item deleted successfully"})

@app.route('/products/cash/<int:item_id>', methods=['DELETE'])
def delete_cash(item_id):
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor(buffered=True)
    cursor.execute("DELETE FROM cash WHERE id=%s",
                   (item_id,))
    db.commit()
    cursor.close()
    return jsonify({"Message":"Cash item deleted successfully"})
        
        
# Endpoint to update an existing bond
@app.route('/bonds/<id>', methods=['PUT'])
def update_bond(id):
    db.reconnect(attempts=1, delay=0)
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']
    parValue = request.json['parValue']     
    maturityDate = request.json['maturityDate']
    coupon = request.json['coupon']
    discountRate = request.json['discountRate']

    cursor = db.cursor()
   
    cursor.execute("UPDATE bonds SET id= %s, holdingName= %s, dateOfPurchase= %s, priceAtPurchase= %s, qty= %s, CurrentPrice= %s, parValue= %s, maturityDate= %s, coupon=%s, discountRate=%s WHERE id = %s",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, parValue, maturityDate,coupon, discountRate, id))
   
    db.commit()
    cursor.close()
    return jsonify({'message': 'Bond updated successfully'})


# Endpoint to update an existing stock
@app.route('/stocks/<id>', methods=['PUT'])
def update_stocks(id):
    db.reconnect(attempts=1, delay=0)
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    priceAtPurchase = request.json['priceAtPurchase']
    qty = request.json['qty']
    currentPrice = request.json['currentPrice']
    ticker = request.json['ticker']
    cursor = db.cursor()
   
   
   
    cursor.execute("UPDATE stocks SET id= %s, holdingName= %s, dateOfPurchase= %s, priceAtPurchase= %s, qty= %s, currentPrice= %s, ticker=%s WHERE id = %s",
                   (id, holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, ticker, id))
    

    db.commit()
    cursor.close()
    return jsonify({'message': 'Stock updated successfully'})



# Endpoint to update an existing cash
@app.route('/cash/<id>', methods=['PUT'])
def update_cash(id):
    db.reconnect(attempts=1, delay=0)
    id = request.json['id']
    holdingName = request.json['holdingName']
    dateOfPurchase = request.json['dateOfPurchase']
    exchAtPurchase = request.json['exchAtPurchase']
    qty = request.json['qty']
    exchCurrent = request.json['exchCurrent']
    currentValue = request.json['currentValue']
    ticker = request.json['ticker']
    

    cursor = db.cursor()
   
    cursor.execute("UPDATE cash SET id= %s, holdingName= %s, dateOfPurchase= %s, exchAtPurchase= %s, qty= %s, exchCurrent= %s, currentValue= %s, ticker=%s WHERE id = %s",
                   (id, holdingName, dateOfPurchase, exchAtPurchase, exchCurrent, qty, currentValue, ticker, id))
    

    db.commit()
    cursor.close()
    return jsonify({'message': 'Cash updated successfully'})


@app.route('/refresh/stocks', methods=['GET'])
def refreshStocks():
    # get tickers from the stocks table 
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor()
    query = "SELECT ticker FROM stocks"
    cursor.execute(query)
    tickers = cursor.fetchall()
    # cursor.close()
    for i in tickers:
        # get information for this product from yahoo
        ticker = i[0]
        tick = yf.Ticker(ticker)
        info = tick.info
        price = info['currentPrice']
        # get the product information from the database using the ticker
        # cursor = db.cursor()
        query = "SELECT * FROM stocks WHERE ticker = %s"
        cursor.execute(query, (ticker,))
        product = cursor.fetchall()[0]
        # cursor.close()
        # # updating the price in the specific product table 
        # cursor = db.cursor()
        stockQuery = "UPDATE stocks SET currentPrice = %s WHERE id = %s"
        cursor.execute(stockQuery, (price, product[0])) 
        db.commit()
        # cursor.close()
    cursor.close()
    return jsonify("Page refreshed successfully")

@app.route('/refresh/cash', methods=['GET'])
def refreshCash():
    # get tickers from the cash table 
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor()
    query = "SELECT ticker FROM cash"
    cursor.execute(query)
    tickers = cursor.fetchall()
    # cursor.close()
    for i in tickers:
        # get information for this product from yahoo
        ticker = i[0]
        tick = yf.Ticker(ticker)
        info = tick.info
        rate = info['ask']
        # get the product information from the database using the ticker
        # cursor = db.cursor()
        query = "SELECT * FROM cash WHERE ticker = %s";
        cursor.execute(query, (ticker,))
        product = cursor.fetchall()[0]
        # cursor.close()
        # # updating the price in the specific product table 
        # cursor = db.cursor()
        cashQuery = "UPDATE cash SET exchCurrent = %s, currentValue=qty*%s WHERE id = %s"
        cursor.execute(cashQuery, (rate, rate, product[0])) 
        db.commit()
        # cursor.close()
    cursor.close()
    return jsonify("Page refreshed successfully")

@app.route('/refresh/bonds', methods=['GET'])
def refreshBonds():
    # Get bonds from table 
    db.reconnect(attempts=1, delay=0)
    cursor = db.cursor()
    query = "SELECT * FROM bonds"
    cursor.execute(query)
    bonds = cursor.fetchall()
    # cursor.close()
    for i in bonds:
        # store all necessary values for the calculation
        purchasePrice = i[3]
        bondPrice = purchasePrice
        # cursor = db.cursor()
        # update database with the information
        bondQuery = "UPDATE bonds SET currentPrice = %s WHERE id = %s"
        cursor.execute(bondQuery, (bondPrice, i[0])) 
        db.commit()
        # cursor.close()
    cursor.close()
    return jsonify("Page refreshed successfully")
            
if __name__ == '__main__':
    app.debug = True
    app.run()
    
