import datetime
import random, string


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

def get_average_parameters():


app.run(port=5001, debug=True)