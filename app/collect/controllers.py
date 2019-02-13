from flask import Blueprint, Response, request, json, g
from datetime import datetime
from functools import wraps
from decimal import Decimal
from pytz import timezone
import logging
import os, string, re, sys, decimal
import requests
import time
import mysql.connector

# MODULE COLLECT
collect = Blueprint("collect", __name__)

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
# Collect "marca"
#
@collect.route("/marca", methods=["GET"])
@customMiddleware
def marca():
    try: 
        mycursor = g.mydb.cursor()

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
        g.mydb.commit()

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

#
# Collect "carro"
#
@collect.route("/carro", methods=["GET"])
@customMiddleware
def carro():
    try: 
        # Variable to store collected data
        collectedMarcas = []

        # Get stored "marca" in database to search "carro" of each one
        cursosSelectMarca = g.mydb.cursor()
        cursosSelectMarca.execute("SELECT id, nome FROM api_marca WHERE status = 0")
        myresult = cursosSelectMarca.fetchall()
        
        # Interate each "marca" to get its "carros"
        for marca in myresult:
            marcaId = marca[0]
            marcaName = marca[1]

            # Get data
            r = requests.get("http://fipeapi.appspot.com/api/1/carros/veiculos/{}.json".format(marcaId))
            carros = r.json()

            # Check if the request limit has been exceeded
            if (r.status_code == 403):
                print("--- REQUESTS LIMIT EXCEEDED ---")

                # sleep 1 minute to start again
                time.sleep( 61 )
                print("--- I'M BACK ---")

                # Try again
                r = requests.get("http://fipeapi.appspot.com/api/1/carros/veiculos/{}.json".format(marcaId))
                carros = r.json()


            # Sql insert
            sqlInsert = "INSERT INTO api_carro (id, nome, marca_id, status) VALUES (%s, %s, %s, %s)"
            sqlInsertItems = []

            # Iterate returned data to add "carro" to sql insert
            for carro in carros:
                sqlInsertItems.append((carro["id"], carro["fipe_name"], marcaId, 0))

            # Execute insert
            cursosInsertCarro = g.mydb.cursor()
            cursosInsertCarro.executemany(sqlInsert, sqlInsertItems)

            if (cursosInsertCarro.rowcount > 0):
                # Append to collected "maca"
                collectedMarcas.append(marcaName)

                # Save status
                cursosUpdateMarca = g.mydb.cursor()
                cursosUpdateMarca.execute("UPDATE api_marca SET `status` = 1 WHERE id = {}".format(marcaId))
                g.mydb.commit()

        # Return data
        returnData = json.dumps({"message": "Collected \"marca\" at data property", "data": collectedMarcas})
        return Response(returnData, status=200, mimetype="application/json")
    except Exception as e:  
        # Log
        logging.error("An exception happened", exc_info=True)

        # Delete uncompleted "marca"
        cursosDeleteUncompletedMarca = g.mydb.cursor()
        cursosDeleteUncompletedMarca.execute("DELETE FROM api_carro WHERE marca_id IN (SELECT id FROM api_marca WHERE status = 0)")
        g.mydb.commit()

        # Return data
        returnData = json.dumps({ "data": None, "message": "Something went wrong!" })
        return Response(returnData, status=500, mimetype="application/json")
