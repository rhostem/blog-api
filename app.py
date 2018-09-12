from flask import Flask, jsonify
from api.ga import ga_api
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(ga_api)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def index():
    return 'blog-api'
