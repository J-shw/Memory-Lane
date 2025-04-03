from flask import Flask, render_template, jsonify, request
from waitress import serve
import logging

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    logging.info('Starting server')
    serve(app, host='0.0.0.0', port=8080)
