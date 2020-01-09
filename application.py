import os
import csv

from cs50 import SQL
from datetime import datetime
from helpers import resultsTable
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET","POST"])
def search():

    if request.method == "POST":

        searchQuery = request.form.get("query")

        results = resultsTable(searchQuery)

        new_table = results["table"]
        new_number_results = results["rowcount"]

        return {"table":new_table, "number_results":new_number_results}

    else:

        searchQuery = ""

        results = resultsTable(searchQuery)

        table = results["table"]
        number_results = results["rowcount"]

        return render_template("explore.html", table=table, number_results=number_results)

@app.route("/product")
def product():

    return render_template("product.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return (e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
