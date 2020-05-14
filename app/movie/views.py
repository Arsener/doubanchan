from . import movie
from flask import request, Response, jsonify
from doubanchan import db
import requests


@movie.route('/')
def index():
    return ''


@movie.route('/top250')
def top250():
    print(request.args.get('start'), request.args.get('count'))
    start = int(request.args.get('start'))
    count = int(request.args.get('count'))
    if not 1 <= start <= 250:
        return jsonify({'status': -1})
    end = start + count - 1

    sql = '''
        select movie_id, movie_name_cn, movie_country, year, if_top, poster_url, db_rating, movie_name_ori
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
         'db_rating': t[6],
         'movie_name_ori': t[7]}
        for t in top
    ]
    cur.close()

    return jsonify(data)


@movie.route('/subject')
def subject():
    id = request.args.get('id')
    sql_movie = 'select * from movie where movie_id = %s'
    sql_actor = '''
        select actor.actor_id, actor_name 
        from actor, act 
        where actor.actor_id = act.actor_id and act.movie_id = %s
    '''
    sql_type = '''
        select type_name 
        from type, belongs_to 
        where type.type_id = belongs_to.type_id and belongs_to.movie_id = %s
    '''
    sql_comments = '''
        select content, date, rate, support
        from comments
        where movie_id = %s
    '''

    cur = db.cursor()
    cur.execute(sql_movie, (id,))
    movie = cur.fetchall()
    if len(movie) == 0:
        return jsonify({'status': -1})
    data = dict()
    data['status'] = 1
    cols = ['movie_id', 'movie_name_cn', 'movie_name_ori', 'other_name', 'movie_country', 'date',
            'year', 'length', 'language', 'summary', 'if_top', 'poster_url', 'db_rating', 'imdb_link',
            'imdb_rating', 'my_rating', 'lfq_rating', 'meta_rating']
    for c, d in zip(cols, movie[0]):
        data[c] = d

    cur.execute(sql_type, (id,))
    types = cur.fetchall()
    data['type'] = ' / '.join([t[0] for t in types])

    cur.execute(sql_actor, (id,))
    actors = cur.fetchall()
    data['actors'] = [
        {'actor_id': a[0],
         'actor_name': a[1]}
        for a in actors
    ]

    cur.execute(sql_comments, (id,))
    comments = cur.fetchall()
    data['comments'] = [
        {'content': c[0], 'date': c[1], 'rate': c[2], 'support': c[3]}
        for c in comments
    ]

    return jsonify(data)


@movie.route('/area')
def area():
    return 'area'


@movie.route('/type')
def type_():
    return 'type'


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
