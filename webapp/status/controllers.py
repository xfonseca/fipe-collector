from flask import Blueprint, Response, request, json, g
from datetime import datetime
from functools import wraps
from decimal import Decimal
from pytz import timezone
import logging
import os, string, re, sys, decimal
import mysql.connector

# MODULE
status = Blueprint("status", __name__)

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
@status.route("/collect", methods=["GET"])
@customMiddleware
def collect():
    try: 
        # Get status data
        cursorSelectStatus = g.mydb.cursor()
        cursorSelectStatus.execute(" \
            SELECT api_marca.id, \
                   api_marca.nome, \
                   CASE WHEN api_marca.status = 1 THEN 100 ELSE 0 END AS status_carro, \
                   ROUND(SUM(CASE WHEN api_carro.status = 1 THEN 1 ELSE 0 END) / COUNT(api_carro.id) * 100) AS status_detalhe \
              FROM api_marca \
              LEFT JOIN api_carro \
                ON marca_id = api_marca.id \
             GROUP BY api_marca.id, api_marca.nome, api_marca.status;" \
        )
        myresult = cursorSelectStatus.fetchall()

        # Format result
        statusMarca = []
        counter = sumStatusCarro = sumStatusDetalhe = 0
        for marca in myresult:
            statusMarca.append({
                "marca_id": str(marca[0]),
                "marca_nome": str(marca[1]),
                "status_carro": int(marca[2]) if marca[2] else 0,
                "status_detalhe": int(marca[3]) if marca[3] else 0
            })

            # To calculate general status
            counter += 1
            sumStatusCarro += int(marca[2]) if marca[2] else 0
            sumStatusDetalhe += int(marca[3]) if marca[3] else 0

        # General status
        statusGeral = {
            "carro": round(sumStatusCarro / counter) if statusMarca else 0,
            "detalhe": round(sumStatusDetalhe / counter) if statusMarca else 0,
        }

        status = {
            "geral": statusGeral,
            "marca": statusMarca
        }

        # Return data
        returnData = json.dumps({ "data": status, "message": "Status data are at data property" })
        return Response(returnData, status=200, mimetype="application/json")
    except Exception as e:  
        # log
        logging.error("An exception happened", exc_info=True)

        # Return data
        returnData = json.dumps({ "data": None, "message": "Something went wrong!" })
        return Response(returnData, status=500, mimetype="application/json")
