#!/usr/bin/env python2.7

import argparse
from datetime import datetime
from hashlib import md5
from sqlite3 import dbapi2 as sqlite3, OperationalError
import os
import urllib2

from bs4 import BeautifulSoup
import dateutil.parser
from flask import Flask, request, session, g, redirect, url_for,\
                  abort, render_template, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash
from werkzeug.wsgi import SharedDataMiddleware

app = Flask(__name__)
app.config.from_object('config.Development')
app.config.from_object(__name__)

if app.config['DEBUG']:
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, app.config['PATH_MAP'])

@app.route('/')
def root():
    return redirect(url_for('timeline'))

@app.route('/<current>/login', methods=['GET', 'POST'])
def login(current='timeline'):
    """Logs the user in."""
    error = None
    register = None
    message = None
    if request.method == 'POST':
        user = query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Username not found. Do you need to register?'
            register = True
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = "Did you forget your password?"
        else:
            session['user_id'] = user['user_id']
            message = "You were logged in successfully!"

    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                         [session['user_id']], one=True)

    return app.view_functions[current](error=error, message=message, register=register, login=True)

@app.route('/register', methods=['GET', 'POST'])
def register(**kwargs):
    """Registers the user."""
    error = None
    g.this_page = '/register'

    if request.method == 'POST' and not kwargs.get('login'):
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db = get_db()
            db.execute('''insert into user (
              username, email, pw_hash) values (?, ?, ?)''',
              [request.form['username'], request.form['email'],
               generate_password_hash(request.form['password'])])
            db.commit()
            return redirect(url_for('root'))

    return render_template('register.html', error=error, Registration='active')

@app.route('/<current>/logout')
def logout(current='timeline'):
    """Logs the user out."""
    session.pop('user_id', None)
    g.user = None

    return app.view_functions[current](message='You have been successfully logged out.')

#Convienence Functions
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                         [session['user_id']], one=True)

def get_user_id(username):
    """Returns the username"""
    rv = query_db('select user_id from user where username = ?',
            [username], one=True)
    return rv[0] if rv else None

##END

def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/{mail_hash}?d=identicon&s={size}'.format(
            mail_hash=md5(email.strip().lower().encode('utf-8')).hexdigest(), size=size)

def get_song_of_the_day():
    today = datetime.now().date()
    song_of_the_day = query_db('''SELECT *
                                  FROM `daily_songs`
                                  WHERE `song_date` >= ?''', [today.strftime('%Y-%m-%d')],
                               one=True)

    return song_of_the_day

@app.route('/addMessage', methods=['POST'])
def addMessage():
    """ Adds a new message linked to the currently logged in user. """
    if 'user_id' not in session:
        abort(401)
    if request.form['message']:
        db = get_db()
        user = session['user_id']

        db.execute('''insert into message (author_id, text, pub_date)
          values (?, ?, ?)''', (user, request.form['message'],
                                datetime.now()))
        db.commit()
        flash('Your message was recorded')

    return redirect(url_for('timeline'))

@app.route('/setDailySongs', methods=['GET'])
@app.route('/setDailySongs/<message>', methods=['GET'])
def setDailySongs(**kwargs):
    g.this_page = '/setDailySongs'
    songs = query_db('''SELECT * FROM `daily_songs`
                        ORDER BY `song_date` DESC''')
    song_of_the_day = get_song_of_the_day()
    return render_template('set_daily_songs.html', DailySongs='active', songs=songs,
                           song_of_the_day=song_of_the_day, **kwargs)

def extract_id_from_uri(uri):
    '''
    '''
    return uri[uri.rfind(':') + 1:]

@app.route('/setSong', methods=['POST'])
def setSong():
    if 'user_id' not in session:
        abort(401)
    if request.form['spotify_uri'] and request.form['song_date']:
        song_details = get_song_details(request.form['spotify_uri'])
        db = get_db()
        db.execute('''INSERT INTO `daily_songs` (song_date, track_uri, artist_uri,
                                                 album_uri, track_name, artist_name, album_name)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (dateutil.parser.parse(request.form['song_date']).date(),
                       song_details['track_uri'], song_details['artist_uri'], song_details['album_uri'],
                       song_details['track_name'], song_details['artist_name'], song_details['album_name']))
        db.commit()

    return redirect(url_for('setDailySongs', message='Song set successfully!'))

def get_song_details(track_uri):
    '''
    '''
    spotify_lookup_base = 'http://ws.spotify.com/lookup/1/?uri='
    song_details = {}
    track_info = urllib2.urlopen(''.join([spotify_lookup_base, track_uri])).read()
    detail_soup = BeautifulSoup(track_info)

    song_details['track_uri'] = track_uri
    song_details['track_name'] = detail_soup.find('track').find('name').get_text()

    artist = detail_soup.find('artist')
    song_details['artist_uri'] = artist.get('href')
    song_details['artist_name'] = artist.find('name').get_text()

    album = detail_soup.find('album')
    song_details['album_uri'] = album.get('href')
    song_details['album_name'] = album.find('name').get_text()

    album_seen_before = query_db('''SELECT `song_id`
                                    FROM `daily_songs`
                                    WHERE `album_uri` = ?''', (song_details['album_uri'], ))
    if not album_seen_before:
        retrieve_album_art(song_details['album_uri'])

    return song_details


def retrieve_album_art(album_uri):
    '''
    '''
    img_dir = app.config['PATH_MAP']['/img']
    art_dir = os.path.join(img_dir, 'albumart')

    base_url = 'http://open.spotify.com/album/'
    album_uri = album_uri[album_uri.rfind(':') + 1:]

    full_url = ''.join([base_url, album_uri])
    track_html = urllib2.urlopen(full_url).read()
    track_soup = BeautifulSoup(track_html)
    cover = track_soup.find(id='big-cover')
    cover_url = cover.get('src')
    cover_art = urllib2.urlopen(cover_url)

    file_path = os.path.join(art_dir, album_uri)
    with open(file_path, 'w+') as art_file:
        art_file.write(cover_art.read())

    return file_path

@app.route('/timeline', methods=['GET'])
def timeline(**kwargs):
    """ Loads """
    all_messages = query_db('''SELECT `message`.`text`, `message`.`pub_date`,
                                      `message`.`sticky`, `message`.`message_id`,
                                      `user`.`username`, `user`.`email`
                                FROM `message`
                                JOIN `user`
                                    ON `user`.`user_id` = `message`.`author_id`
                            ''')
    song_of_the_day = get_song_of_the_day()
    g.this_page = '/timeline'
    return render_template('timeline.html', all_messages=all_messages,
                           song_of_the_day=song_of_the_day, Timeline='active',
                           **kwargs)

#Database functions
def get_db():
    """Opens a db connection if there isn't one for the app."""
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db

@app.teardown_appcontext
def close_database(exception):
    """Closes the db at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

def init_db():
    """Creates the db."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    """Queries the db and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

###End Database functions

# Add some filters to Jinja
app.jinja_env.filters['gravatar'] = gravatar_url
app.jinja_env.filters['extract_id_from_uri'] = extract_id_from_uri

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--always-init-db', dest='always_init_db', action='store_true', default=False)
    args = parser.parse_args()

    # If this is set, the db will initialize EVERY time the server is starte/restarted.
    if args.always_init_db:
        init_db()

    # Otherwise, it will initialize only if the user table doesn't exist.
    try:
        # If the user tried to start without initializing a DB when one
        # doesn't exist, go ahead and create it.
        with app.app_context():
            db = get_db()
            result = db.execute('''SELECT * FROM `user` LIMIT 1''').fetchall()
    except OperationalError:
        init_db()

    app.run('0.0.0.0')
