from flask import Blueprint, Response, request, json, g
from datetime import datetime
from functools import wraps
from decimal import Decimal
from pytz import timezone
import logging
import os, string, re, sys, decimal
import mysql.connector

# MODULE MIGRATION
migration = Blueprint("migration", __name__)

# DECORATOR
def customMiddleware(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # MySQL Connection
        g.mydb = mysql.connector.connect(
            host=os.environ["MYSQL_HOST"],
            user=os.environ["MYSQL_USER"],
            passwd=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
        )
        return f(*args, **kwargs)
    return wrap

#
# Creates a coefficient table
#
@migration.route("/table-create", methods=["GET"])
@customMiddleware
def tableCreate():
    try: 
        # Connection
        mycursor = g.mydb.cursor()

        # Drop tables if exists
        mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        mycursor.execute("DROP TABLE IF EXISTS api_marca")
        mycursor.execute("DROP TABLE IF EXISTS api_carro")
        mycursor.execute("DROP TABLE IF EXISTS api_detalhe")
        # mycursor.execute("DROP TABLE IF EXISTS proces_aux")
        # mycursor.execute("DROP TABLE IF EXISTS proces_carro")

        # Create tables
        mycursor.execute("CREATE TABLE api_marca (id INT(11) NOT NULL, nome VARCHAR(255) NOT NULL, status TINYINT(1) DEFAULT 0 NOT NULL, PRIMARY KEY (id))")
        mycursor.execute("CREATE TABLE api_carro (id INT(11) NOT NULL, nome VARCHAR(500) NOT NULL, marca_id INT(11) NOT NULL, status TINYINT(1) DEFAULT 0 NOT NULL, PRIMARY KEY (id), CONSTRAINT `fk_carro_marca` FOREIGN KEY (marca_id) REFERENCES api_marca(id))")
        mycursor.execute("CREATE TABLE api_detalhe (id VARCHAR(50) NOT NULL, ano INT(4) DEFAULT NULL, fipe VARCHAR(20) DEFAULT NULL, preco NUMERIC DEFAULT NULL, carro_id INT(11) NOT NULL, CONSTRAINT `fk_detalhe_carro` FOREIGN KEY (carro_id) REFERENCES api_carro(id))")
        # mycursor.execute("CREATE TABLE proces_aux (id INT(11) NOT NULL AUTO_INCREMENT, `key` VARCHAR(100) NOT NULL, value1 VARCHAR(500) NOT NULL, value2 VARCHAR(500), PRIMARY KEY (id))")
        # mycursor.execute("CREATE TABLE proces_carro (id INT(11) NOT NULL, original_marca VARCHAR(255) NOT NULL, original_carro VARCHAR(500) NOT NULL, proces_marca VARCHAR(255) NOT NULL, proces_modelo VARCHAR(255) NOT NULL, proces_versao VARCHAR(255) NOT NULL, PRIMARY KEY (id))")

        # Return data
        returnData = json.dumps({ "data": None, "message": "The tables has been successfully created!" })
        return Response(returnData, status=200, mimetype="application/json")
    except Exception as e:  
        # log
        logging.error("An exception happened", exc_info=True)

        # Return data
        returnData = json.dumps({ "data": None, "message": "Something went wrong!" })
        return Response(returnData, status=500, mimetype="application/json")
