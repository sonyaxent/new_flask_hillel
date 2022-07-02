import datetime
import random, string
import pandas as pd
import csv
import numpy

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/now")
def get_time():
    return f'Current time {datetime.datetime.now()}'

@app.route("/generate_password")
def generate_password():
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    password = ""
    for index in range(10, 20):
        password = password + random.choice(characters)
    return f'Password generated: {password}'

@app.route("/average_parameters")
def get_average_parameters():
    col_names = [
        'Id',
        'Height',
        'Weight'
    ]

    df = pd.read_csv('hw.csv', names=col_names, skiprows=[0])

    average_height = round(numpy.mean(df.Height), 2)
    average_weight = round(numpy.mean(df.Weight), 2)
    return f'<p>The average height is {average_height}. The average weight is {average_weight}</p>'

app.run(port=5001, debug=True)