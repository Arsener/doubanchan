from . import movie
from flask import request, redirect, render_template, session, url_for, Response
from ..db import get_db
import requests

@movie.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_name = request.values.get('movie_name')
        session['movie_name'] = movie_name

        db = get_db()
        cur = db.cursor()
        sql = '''
            select movie_id, movie_name_cn, poster_url from movie where movie_name_cn like %s
        '''
        cur.execute(sql, ('%{}%'.format(movie_name), ))
        movie_list = cur.fetchall()
        # print(movie_list)
        session['hh'] = movie_list

        cur.close()
        db.close()
        return redirect(url_for('movie.index'))

    return render_template('movie_list.html', movie_name=session.get('movie_name'), l=session.get('hh'))


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