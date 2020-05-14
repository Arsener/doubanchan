from . import movie
from flask import request, Response, jsonify
from ..db import get_db
import requests


@movie.route('/')
def index():
    return ''


@movie.route('/top250')
def top250():
    start = int(request.args.get('start'))
    count = int(request.args.get('count'))

    if start == 1:
        end = count * 2
    elif start + count <= 250:
        start += count
        end = start + count
    else:
        return jsonify({'status': -1})

    sql = '''
        select movie_id, movie_name_cn, movie_country, year, if_top, poster_url, db_rating
        from movie
        where if_top >= %s and if_top <= %s
        order by if_top
    '''

    db = get_db()
    cur = db.cursor()
    cur.execute(sql, (start, end))
    top = cur.fetchall()

    data = dict()
    data['status'] = 1
    data['start'] = start
    data['count'] = len(top)
    movies = [
        {'movie_id': t[0],
         'movie_name_cn': t[1],
         'movie_country': t[2],
         'year': t[3],
         'if_top': t[4],
         'poster_url': t[5],
         'db_rating': t[6]}
        for t in top
    ]
    data['movies'] = movies

    return jsonify(data)



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
