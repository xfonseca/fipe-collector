from flask import Blueprint, Response, request, json, g
from datetime import datetime
from functools import wraps
from decimal import Decimal
from pytz import timezone
import logging
import os, string, re, sys, decimal
import mysql.connector
import requests

# MODULE COLLECT
collect = Blueprint("collect", __name__)

#
# Creates a coefficient table
#
@collect.route("/marca", methods=["GET"])
def marca():
    try: 
        # MySQL Connection
        mydb = mysql.connector.connect(
            host=os.environ["MYSQL_HOST"],
            user=os.environ["MYSQL_USER"],
            passwd=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
        )
        mycursor = mydb.cursor()

        # Get data
        r = requests.get("http://fipeapi.appspot.com/api/1/carros/marcas.json")
        marcas = r.json()

        # Sql insert
        sqlInsert = "INSERT INTO api_marca (id, nome, status) VALUES (%s, %s, %s)"
        sqlInsertItems = []

        # Iterate returned data to add "marcas" to sql insert
        for marca in marcas:
            sqlInsertItems.append((marca["id"], marca["fipe_name"], 0))

        # Execute insert
        mycursor.executemany(sqlInsert, sqlInsertItems)
        mydb.commit()

        # Return data
        insertedRows = str(mycursor.rowcount)
        returnData = json.dumps({"message": "{} inserted rows".format(insertedRows), "data": marcas})
        return Response(returnData, status=200, mimetype="application/json")
    except Exception as e:  
        # log
        logging.error("An exception happened", exc_info=True)

        # Return data
        returnData = json.dumps({ "data": None, "message": "Something went wrong!" })
        return Response(returnData, status=500, mimetype="application/json")
