#!/usr/bin/python3
from flask import Response, Flask, render_template, stream_with_context
from flask_restful import Resource, Api
from flask_wtf import FlaskForm

import theft
import theft_2
import time


'''
creting routes for the templates
'''

app = Flask(__name__, static_url_path='/static')


def login():
    return(render_template("page-1.html"))


@app.route("/store-selection")
def store():
    return(render_template("page-2.html"))


@app.route("/gate-selection")
def gate():
    return(render_template("page-3.html"))


@app.route("/monitoring-exit", methods=['GET', 'POST'])
def home():
    pics = theft.get_pic()
    return(render_template("page-4.html", pics=pics))


@app.route("/monitoring-restroom", methods=['GET', 'POST'])
def home_2():
    pics = theft_2.get_pic()
    return(render_template("page-4.html", pics=pics))


if __name__ == "__main__":
    app.run(debug=True)
