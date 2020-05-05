from . import movie
from flask import request, redirect, render_template, session, url_for
from ..db import get_db

@movie.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_name = request.values.get('movie_name')
        session['movie_name'] = movie_name

        db = get_db()
        cur = db.cursor()
        sql = '''
            select movie_name_cn from movie limit %s
        '''
        cur.execute(sql, (int(movie_name), ))
        movie_list = cur.fetchall()
        # print(movie_list)
        session['hh'] = movie_list

        cur.close()
        db.close()
        return redirect(url_for('movie.index'))

    return render_template('movie_list.html', movie_name=session.get('movie_name'), l=session.get('hh'))