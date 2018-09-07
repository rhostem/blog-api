from flask import Flask, jsonify
from analytics import initialize_analyticsreporting, get_pageview, get_report_example, get_pageview, print_response

app = Flask(__name__)
analytics = initialize_analyticsreporting()


@app.route('/')
def index():
    return 'blog-api'


@app.route('/report/visitors')
def report_visitors():
    response = get_pageview(analytics)
    # print(response['reports'][0]['data'])

    return jsonify(response), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/report/example')
def defaultReport():
    response = get_report_example(analytics)

    return jsonify(response)
