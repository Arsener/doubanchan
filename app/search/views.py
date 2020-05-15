from . import search
from flask import request, jsonify
from doubanchan import db
import requests
import json


@search.route('/')
def index():
    start = int(request.args.get('start'))
    if start < 0:
        return jsonify({'status': -1})

    count = int(request.args.get('count'))
    query = request.args.get('query')
    tag = int(request.args.get('tag'))
    HEADERS = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    if tag == 1:  # 电影
        url = 'http://166.111.83.75:9200/movie/_search?size={}&from={}'.format(count, start)
        data = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"movie_name_cn": query}}
                    ]
                }
            }
        }

        return jsonify(json.loads(requests.post(url, json.dumps(data), headers=HEADERS).text))
    elif tag == 2:  # 影人
        pass
    elif tag == 3:  # 简介
        url = 'http://166.111.83.75:9200/movie/_search?size={}&from={}'.format(count, start)
        data = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"summary": query}}
                    ]
                }
            },
            "highlight": {
                "fields": {
                    "summary": {}
                }
            }
        }
        return jsonify(json.loads(requests.post(url, json.dumps(data), headers=HEADERS).text))

    return jsonify({'status': -1})
