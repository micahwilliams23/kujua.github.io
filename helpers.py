import os
import csv

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

def resultsTable(searchQuery):

    # get data from database
    db = SQL("sqlite:///scrape/food.db")
    products = db.execute("SELECT * FROM cereal WHERE product_name LIKE :sq", sq="%"+searchQuery+"%")
    rowcount = len(products)

    # create empty list to hold code for table
    table = open("scrape/kellogg/table.txt", "w")

    table.write("<div class='row row-cols-xl-4 row-cols-lg-3 row-cols-md-2 explore-row'>")

    for row in range(rowcount):
        # make table elements
        table.write(
            f"<div class='col' id='explore-result-box'><div class='explore-table-element'><div>"+
                # add product image
                "<img class='explore-product-image' src='"+products[row]["product_image_link"]+"'>"+
                # add product name
                "<text class='explore-product-name'>"+products[row]["product_name"]+"</text>"+
            "</div></div></div>")

    table.write("</div>")

    table.close()

    # prepare text to send to template
    table_txt = open("scrape/kellogg/table.txt", "r")
    table = table_txt.read()
    table_txt.close()

    return {"table":table, "rowcount":rowcount}