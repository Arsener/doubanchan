from . import movie
from flask import request, Response, jsonify
from ..db import get_db
from doubanchan import db
import requests


@movie.route('/')
def index():
    return ''


@movie.route('/top250')
def top250():
    start = int(request.args.get('start'))
    count = int(request.args.get('count'))
    if not 1 <= start <= 250:
        return jsonify({'status': -1})
    end = start + count - 1

    sql = '''
        select movie_id, movie_name_cn, movie_country, year, if_top, poster_url, db_rating
        from movie
        where if_top >= %s and if_top <= %s
        order by if_top
    '''

    # db = get_db()
    cur = db.cursor()
    cur.execute(sql, (start, end))
    top = cur.fetchall()

    data = dict()
    data['status'] = 1
    data['start'] = start
    data['count'] = len(top)
    data['movies'] = [
        {'movie_id': t[0],
         'movie_name_cn': t[1],
         'movie_country': t[2],
         'year': t[3],
         'if_top': t[4],
         'poster_url': t[5],
         'db_rating': t[6]}
        for t in top
    ]
    cur.close()

    return jsonify(data)


@movie.route('/subject')
def subject():
    id = request.args.get('id')
    db = get_db()
    return ''



@movie.route('/image/', methods=['GET'])
def image():
    image_url = request.args.get('image_url')
    conn = requests.get(
        url=image_url,
        headers={
            "Origin": "https://www.douban.com",
            "Referer": "https://www.douban.com/",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
    )

    return Response(conn.content, mimetype="image/jpeg")
