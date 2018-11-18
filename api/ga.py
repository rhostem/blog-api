"""Google Analytics Reporting API V4.

Creating a Report
https://developers.google.com/analytics/devguides/reporting/core/v4/basic

Dimensions & Metrics Explorer
https://developers.google.com/analytics/devguides/reporting/core/dimsmets
"""

from flask import Flask, jsonify, Blueprint, request

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import re
import operator

from functools import lru_cache

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = './ga_key.json'
VIEW_ID = '136669174'


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


@lru_cache(maxsize=10)
def get_post_pageview(analytics, startDate='7daysAgo', endDate='2018-09-19'):
    """페이지뷰"""

    batchData = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
                    "metrics": [
                        {
                            "expression": "ga:pageviews",
                        },
                    ],
                    "dimensions": [
                        {
                            "name": "ga:pagePath",
                        },
                    ],
                    "orderBys": [
                        {"fieldName": "ga:pageviews", "sortOrder": "DESCENDING"},
                    ]
                }]
        }
    ).execute()

    rows = batchData.get('reports', [])[0].get('data', {}).get('rows', [])
    postPage = {}
    MIN_COUNT = 1

    for row in rows:
        pagePath = row.get('dimensions', [])[0].lower()
        count = int(row.get('metrics')[0].get('values')[0])

        # /post 로 시작하고, 역슬래쉬(\)를 포함하지 않는 문자열을 매칭
        postPathRegex = re.compile('^\/posts\/(?!\/)[가-힣\w-]+')
        matchingPostPath = postPathRegex.match(pagePath)

        # 포스트 라우팅이 매칭되었을 때
        if postPathRegex.match(pagePath) and count >= MIN_COUNT:
            pagePath = matchingPostPath.group()

            # if pagePath not in pagePathList:
            if pagePath not in postPage:
                postPage[pagePath] = {
                    'count': count
                }
            else:
                postPage[pagePath]['count'] = postPage[pagePath]['count'] + count

    # 결과 리스트 생성
    result = []
    for page in postPage.keys():
        result.append({
            'page': page,
            'count': postPage[page]['count']
        })

    result = sorted(result, key=lambda k: k['count'], reverse=True)

    return result


def get_report_example(analytics):
    batchData = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:sessions'}],
                    'dimensions': [{'name': 'ga:country'}]
                }]
        }
    ).execute()

    data = batchData.get('reports', [])[0].get('data', {})

    return data


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get(
            'metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ' + dimension)

            for i, values in enumerate(dateRangeValues):
                print('Date range: ' + str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    print(metricHeader.get('name') + ': ' + value)


def jsonRes(res):
    """response 데이터를 jsonify 모듈로 변환해서 전달"""
    return jsonify(res), 200


ga_api = Blueprint('ga_api', __name__)
analytics = initialize_analyticsreporting()


@ga_api.route('/api/ga/post_pageviews')
def post_pageview():
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    response = get_post_pageview(analytics, startDate, endDate)

    return jsonRes(response)


@ga_api.route('/api/ga/example')
def defaultReport():
    response = get_report_example(analytics)

    return jsonRes(response)
