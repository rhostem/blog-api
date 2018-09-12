from flask import Flask, jsonify
from api.ga import ga_api

app = Flask(__name__)
app.register_blueprint(ga_api)


@app.route('/')
def index():
    return 'blog-api'
