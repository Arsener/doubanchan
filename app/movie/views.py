from . import movie
from flask import request, Response, jsonify
from doubanchan import db
import requests


@movie.route('/')
def index():
    return ''


@movie.route('/top250')
def top250():
    rank = ['if_top', 'year desc']
    start = int(request.args.get('start'))
    count = int(request.args.get('count'))
    try:
        rankby = int(request.args.get('rankby'))
    except:
        rankby = 0
    if not 0 <= start < 250:
        return jsonify({'status': -1})

    sql = '''
        select movie_id, movie_name_cn, movie_country, year, if_top, poster_url, db_rating, movie_name_ori
        from movie
        where if_top > 0
        order by {}
    '''

    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute(sql.format(rank[rankby]))
    top = cur.fetchall()[start: start + count]

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
    data['rankby'] = rankby
    cur.close()

    return jsonify(data)


@movie.route('/subject')
def subject():
    movie_id = request.args.get('id')
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

    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute(sql_movie, (movie_id,))
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

    cur.execute(sql_type, (movie_id,))
    types = cur.fetchall()
    data['type'] = ' / '.join([t[0] for t in types])

    cur.execute(sql_actor, (movie_id,))
    actors = cur.fetchall()
    data['actors'] = [
        {'actor_id': a[0],
         'actor_name': a[1]}
        for a in actors
    ]

    cur.execute(sql_comments, (movie_id,))
    comments = cur.fetchall()
    data['comments'] = [
        {'content': c[0], 'date': c[1], 'rate': c[2], 'support': c[3]}
        for c in comments
    ]

    data['imdb_rating'] = float(data['imdb_rating'].split('/')[0])
    data['lfq_rating'] = int(data['lfq_rating'].split('%')[0])
    data['meta_rating'] = int(data['meta_rating'].split('/')[0])
    cur.close()

    return jsonify(data)


@movie.route('/area')
def area():
    rank = ['year', 'db_rating']
    start = int(request.args.get('start'))
    if start < 0:
        return jsonify({'status': -1})

    count = int(request.args.get('count'))
    areaid = int(request.args.get('areaid'))
    try:
        rankby = int(request.args.get('rankby'))
    except:
        rankby = 0

    cur = db.cursor()
    sql = '''
        select movie_id, movie_name_cn, movie_country, year, if_top, poster_url, db_rating, movie_name_ori
        from movie
    '''
    if areaid == 1:
        sql += '''
            where language like '%汉语普通话%'
                and movie_country like '%中国%'
        '''
    elif areaid == 2:
        sql += '''
            where movie_country like '%日本%'
        '''
    elif areaid == 3:
        sql += '''
            where movie_country like '%韩国%'
        '''
    elif areaid == 4:
        sql += '''
            where movie_country like '%美国%'
                or movie_country like '%英国%'
                or movie_country like '%德国%'
                or movie_country like '%法国%'
                or movie_country like '%意大利%'
                or movie_country like '%西班牙%'
                or movie_country like '%俄罗斯%'
                or movie_country like '%荷兰%'
                or movie_country like '%瑞典%'
                or movie_country like '%丹麦%'
        '''
    else:
        return jsonify({'status': -1})

    sql += 'order by {} desc'

    cur.execute(sql.format(rank[rankby], ))
    movies = cur.fetchall()[start:start + count]

    data = dict()
    data['status'] = 1
    data['start'] = start
    data['count'] = len(movies)
    data['movies'] = [
        {'movie_id': m[0],
         'movie_name_cn': m[1],
         'movie_country': m[2],
         'year': m[3],
         'if_top': m[4],
         'poster_url': m[5],
         'db_rating': m[6],
         'movie_name_ori': m[7]}
        for m in movies
    ]
    data['areaid'] = areaid
    data['rankby'] = rank[rankby]
    cur.close()

    return jsonify(data)


@movie.route('/type')
def type_():
    rank = ['year', 'db_rating']
    start = int(request.args.get('start'))
    if start < 0:
        return jsonify({'status': -1})

    count = int(request.args.get('count'))
    typeid = request.args.get('typeid')
    try:
        rankby = int(request.args.get('rankby'))
    except:
        rankby = 0

    sql = '''
        select movie.movie_id, movie_name_cn, movie_country, year, if_top, poster_url, db_rating, movie_name_ori
        from movie, belongs_to, type
        where movie.movie_id = belongs_to.movie_id 
            and belongs_to.type_id = type.type_id 
            and type_name = '{}'
        order by {} desc
    '''
    cur = db.cursor()
    cur.execute(sql.format(typeid, rank[rankby]))
    movies = cur.fetchall()[start:start + count]

    data = dict()
    data['status'] = 1
    data['start'] = start
    data['count'] = len(movies)
    data['movies'] = [
        {'movie_id': m[0],
         'movie_name_cn': m[1],
         'movie_country': m[2],
         'year': m[3],
         'if_top': m[4],
         'poster_url': m[5],
         'db_rating': m[6],
         'movie_name_ori': m[7]}
        for m in movies
    ]
    data['type'] = typeid
    data['rankby'] = rank[rankby]
    cur.close()

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
