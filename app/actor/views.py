from . import actor
from flask import request, Response, jsonify
from doubanchan import db

@actor.route('/')
def index():
    actor_id = request.args.get('id')
    sql_actor = 'select actor_name from actor where actor_id = %s'
    sql_movies = '''
        select movie.movie_id, movie_name_cn, movie_country, year, if_top, poster_url, db_rating, movie_name_ori
        from movie, act
        where act.actor_id = %s and act.movie_id = movie.movie_id
    '''

    db.ping(reconnect=True)
    cur = db.cursor()
    cur.execute(sql_actor, (actor_id,))
    actor = cur.fetchall()
    if len(actor) == 0:
        return jsonify({'status': -1})

    data = dict()
    data['status'] = 1
    data['actor_id'] = actor_id
    data['actor_name'] = actor[0][0]

    cur.execute(sql_movies, (actor_id,))
    movies = cur.fetchall()
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
    cur.close()

    return jsonify(data)