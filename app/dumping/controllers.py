from flask import Blueprint, Response, request, json, g
from datetime import datetime
from functools import wraps
from decimal import Decimal
from pytz import timezone
import logging
import os, string, re, sys, decimal
import mysql.connector

# MODULE
dumping = Blueprint("dumping", __name__)

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
@dumping.route("/dbmysql", methods=["GET"])
@customMiddleware
def dbmysql():
    try: 
        startingId = request.args.get('startingId')

        # Get status data
        cursorSelectCarro = g.mydb.cursor()
        cursorSelectCarro.execute(" \
            SELECT api_carro.id, api_marca.nome, api_carro.nome \
              FROM api_marca \
              JOIN api_carro ON api_carro.marca_id = api_marca.id \
             WHERE api_carro.id > {};".format(startingId) \
        )
        myresult = cursorSelectCarro.fetchall()

        # Var dump
        stringDump = "INSERT INTO table_name (campo1, campo2, campo3) VALUES "

        # Format result
        for carro in myresult:
            # Values
            carroId = str(carro[0])
            carroMarca = str(carro[1]).replace("'", "\\'")
            carroModelo = str(carro[2]).replace("'", "\\'")

            # Concatenate
            stringDump += "(" + carroId + ", '" + carroMarca  + "', '" + carroModelo + "'),"

        # Return data
        returnData = json.dumps({ "data": stringDump, "message": "Status data are at data property" })
        return Response(returnData, status=200, mimetype="application/json")
    except Exception as e:  
        # log
        logging.error("An exception happened", exc_info=True)

        # Return data
        returnData = json.dumps({ "data": None, "message": "Something went wrong!" })
        return Response(returnData, status=500, mimetype="application/json")
