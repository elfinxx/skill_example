from flask import Flask
import csv


app = Flask(__name__)

with open("./1.csv", 'r', encoding='utf8') as d:
    reader = csv.DictReader(d)

    for r in reader:
        print(r)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sample')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
