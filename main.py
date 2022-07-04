import datetime
import pprint
import random, string
import requests
import pandas as pd

from http import HTTPStatus

import numpy

from flask import Flask, request, jsonify, Response
from webargs import validate, fields
from webargs.flaskparser import use_kwargs

if __name__ == "__main__":
    app = Flask(__name__)

@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handler(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ['Invalid request.'])

    if headers:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
            headers
        )
    else:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
        )

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

@app.route("/generate_password_lesson3")
@use_kwargs(
    {
        'length': fields.Int(
            missing=10,
            validate=[validate.Range(min=8, max=100)]
        )
    },
    location='query'
)



def generate_password_lesson3(length):
    # length = request.args.get('length', '10')
    #
    # max_limit = request.args.get('max_limit', '10')
    #
    # try:
    #     float_length = float(length)
    # except ValueError:
    #     return "ERROR: should be a float"
    # print(float_length)
    #
    # if not length.isdigit():
    #     return "ERROR: should be a digit"
    #
    # length = int(length)
    #
    # if not 8 < length < 100:
    #     return "ERROR: should be in range [8, 100]"

    # string
    # limits
    # empty



    return "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length))

@app.route('/get_astronauts')
def get_astronauts():
    url = 'http://api.open-notify.org/astros.json'
    result = requests.get(url, {})
    if result.status_code not in (HTTPStatus.OK, ):
        return Response(
            'ERROR: Something went wrong',
            status=result.status_code
        )
    result = result.json()
    statistics = {}
    for entry in result.get('people', {}):
        statistics[entry['craft']] = statistics.get(entry['craft'], 0) + 1

    pprint.pprint(statistics)
    return statistics


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

if __name__ == "__main__":
    app.run(port=5001, debug=True)