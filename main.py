from flask import Flask, jsonify
from analytics import initialize_analyticsreporting, get_report, print_response

app = Flask(__name__)
analytics = initialize_analyticsreporting()


@app.route('/')
def index():
    return 'blog-api'


@app.route('/report')
def defaultReport():
    response = get_report(analytics)

    # print_response(response)
    print(response)

    return jsonify(response)
