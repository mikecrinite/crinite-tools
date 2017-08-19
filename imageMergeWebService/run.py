#!usr/bin/python
from flask import Flask
from urllib.request import urlopen

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

def getfile(url):
    return Image.open

if __name__ == '__main__':
    app.run(debug=True)