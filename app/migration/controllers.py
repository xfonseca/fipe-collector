from flask import Blueprint, Response, request, json, g
from datetime import datetime
from functools import wraps
from decimal import Decimal
from pytz import timezone
import logging
import os, string, re, sys, decimal

# MODULE MIGRATION
migration = Blueprint("migration", __name__)

#
# Creates a coefficient table
#
@migration.route("/table-create/", methods=["GET"])
def tableCreate():
    # Return data
    return Response('ok', status=200, mimetype="application/json")