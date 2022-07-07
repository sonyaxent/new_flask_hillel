# coding=utf-8

import datetime
import pprint
import random
import string
from http import HTTPStatus

import numpy

import pandas as pd
import requests
from flask import Flask, jsonify, Response
from webargs import validate, fields
from webargs.flaskparser import use_kwargs
from faker import Faker
from datetime import datetime

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
    return f'Password: {password}'

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



@app.route("/average_parameters")
def get_average_parameters():
    col_names = [
        'Id',
        'Height',
        'Weight'
    ]

    df = pd.read_csv('hw.csv', names=col_names, skiprows=[0])

    average_height = pd.Series.mean(df.Height)
    average_weight = pd.Series.mean(df.Weight)
    return f'<p>The average height is {round(average_height, 2)}. The average weight is {round(average_weight, 2)}</p>'

@app.route('/generate_students')
@use_kwargs(
    {
        'count': fields.Int(
            missing=10,
            validate=[validate.Range(min=1, max=1000)]
        )
    },
    location='query'
)
def generate_students(count):
    faker = Faker("EN")
    student_data = {}
    for i in range(0, count):
        student_data[i] = {}
        student_data[i]['Name'] = faker.name()
        student_data[i]['Email'] = faker.email()
        student_data[i]['Password'] = faker.password()
        student_data[i]['Date of birth'] = faker.date_between_dates(date_start=datetime(1985, 1, 1), date_end=datetime(2001, 1, 1)).year
    df = pd.DataFrame.from_dict(student_data)
    df.to_csv(r'generate_students.csv', index=False, header=True)
    see = pd.read_csv(r'generate_students.csv')
    return see.to_dict()

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

@app.route('/get_bitcoin_rate')
@use_kwargs(
    {
        'code': fields.Str(load_default='USD'
        ),
        'amount': fields.Int(
            missing=100
        )
    },
    location='query'
)
def get_bitcoin_rate(code='USD', amount=100):
    result = requests.get('https://bitpay.com/api/rates')
    result = result.json()
    currency_list = list(filter(lambda item: item['code'] == code, result))
    currency_rate = currency_list[0]['rate']
    btc_to_buy = f' Here is the currency rate of {amount}  {code}:  {amount / currency_rate}'
    pprint.pprint(btc_to_buy)

    return btc_to_buy



if __name__ == "__main__":
    app.run(port=5001, debug=True)