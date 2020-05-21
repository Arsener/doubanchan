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

    url = 'http://166.111.83.75:9200/movie/_search?size={}&from={}'.format(count, start)
    data = {}
    if tag == 1:  # 电影
        data = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"movie_name_cn": query}}
                    ]
                }
            }
        }
    elif tag == 2:  # 影人
        url = 'http://166.111.83.75:9200/actor/_search?size={}&from={}'.format(count, start)
        data = {
            "query": {
                "multi_match": {
                    "query": query,
                    "type": "cross_fields",
                    "operator": "and",
                    "fields": [
                        "actor_first_name_cn",
                        "actor_first_name_en",
                        "actor_last_name_cn",
                        "actor_last_name_en",
                        "actor_first_name_cn.pinyin",
                        "actor_last_name_cn.pinyin",
                        "actor_name",
                        "actor_name.pinyin"
                    ]
                }
            }
        }
    elif tag == 3:  # 简介
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

    result = json.loads(requests.post(url, json.dumps(data), headers=HEADERS).text)
    data = dict()
    data['total'] = result['hits']['total']['value']
    data['status'] = result['_shards']['successful']
    data['movies'] = [s['_source'] for s in result['hits']['hits']]
    data['count'] = len(data['movies'])
    if tag == 3:
        for i in range(data['count']):
            data['movies'][i]['summary_highlight'] = '…'.join(result['hits']['hits'][i]['highlight']['summary'])
    data['tag'] = tag
    data['query'] = query

    return jsonify(data)
