from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    #user="root",
    #password="c0nygre",
    #database="conygre"
)