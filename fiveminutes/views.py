import os
from functools import wraps
from datetime import datetime
from hashlib import md5
import urllib2

from bs4 import BeautifulSoup
import dateutil.parser

from flask import render_template, request, flash, redirect,\
                  url_for, g, abort, session
from fiveminutes import app, oid
from fiveminutes.models import Announcement, User, DailySong
from fiveminutes.mixin import func, safe_commit

# Utility functions for our Flask App

def login_required(fnctn):
    @wraps(fnctn)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return redirect(url_for('login', next=request.url))
        return fnctn(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    g.user = None
    if 'openid' in session:
        g.user = User.query.filter_by(openid=session['openid']).first()

# End Utility Functions

@app.route('/')
def index():
    if not g.user:
        return redirect(url_for('login'))
    return redirect(url_for('announcements'))

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """Does the login via OpenID.  Has to call into `oid.try_login`
    to start the OpenID machinery.
    """
    # if we are already logged in, go back to were we came from
    if g.user is not None:
        oid_url = oid.get_next_url()
        if oid_url.endswith('login'):
            # Don't redirect to the login page ever.
            oid_url = url_for('index')

        return redirect(oid_url)

    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email', 'fullname',
                                                  'nickname'])
    err = oid.fetch_error()
    if err:
        flash(err, 'error')

    return render_template('login.html', next=oid.get_next_url(),
                           openid_domain=app.config['OPENID_DOMAIN'],
                           id_url='https://www.google.com/accounts/o8/id')

@oid.after_login
def create_or_login(resp):
    """This is called when login with OpenID succeeded and it's not
    necessary to figure out if this is the users's first login or not.
    This function has to redirect otherwise the user will be presented
    with a terrible URL which we certainly don't want.
    """
    session['openid'] = resp.identity_url
    user = User.query.filter_by(openid=resp.identity_url).first()
    if not resp.email.endswith('@{}'.format(app.config['OPENID_DOMAIN'])):
        flash('You must be logged in to your {} Google account to continue.'.format(app.config['OPENID_DOMAIN']), 'error')
        return redirect(url_for('index'))
    if user is not None:
        flash(u'Successfully signed in', 'success')
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_profile', next=oid.get_next_url(),
                            name=resp.fullname or resp.nickname,
                            email=resp.email))

@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    """If this is the user's first login, the create_or_login function
    will redirect here so that the user can set up his profile.
    """
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        group = request.form['group']
        if not name:
            flash(u'Error: you have to provide a name', 'error')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address', 'error')
        else:
            flash(u'Profile successfully created', 'success')
            user = User(name=name, email=email, openid=session['openid'], group=group)
            user.insert()
            safe_commit()
            return redirect(oid.get_next_url())
    return render_template('create_profile.html', next_url=oid.get_next_url(), work_groups=app.config['WORK_GROUPS'])

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Updates a profile"""
    form = dict(name=g.user.name, email=g.user.email, group=g.user.group)
    if request.method == 'POST':
        if 'delete' in request.form:
            g.user.delete()
            safe_commit()
            session['openid'] = None
            flash(u'Profile deleted', 'success')
            return redirect(url_for('index'))
        form['name'] = request.form['name']
        form['email'] = request.form['email']
        form['group'] = request.form['group']
        if not form['name']:
            flash(u'Error: you have to provide a name', 'error')
        elif '@' not in form['email']:
            flash(u'Error: you have to enter a valid email address', 'error')
        else:
            flash(u'Profile successfully updated', 'success')
            g.user.name = form['name']
            g.user.email = form['email']
            g.user.group = form['group']
            safe_commit()
            return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', form=form, work_groups=app.config['WORK_GROUPS'])

@app.route('/logout')
@login_required
def logout():
    session.pop('openid', None)
    flash(u'You have been signed out', 'success')
    return redirect(url_for('index'))

def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/{mail_hash}?d=identicon&s={size}'.format(
            mail_hash=md5(email.strip().lower().encode('utf-8')).hexdigest(), size=size)

def get_song_of_the_day(today=None):
    if not today:
        today = datetime.now().date()

    song_of_the_day = DailySong.filter(func.date(DailySong.created_on) == today).all()
    return song_of_the_day

@app.route('/announcements/add', methods=['POST'])
@login_required
def add_announcement():
    """ Adds a new announcment linked to the currently logged in user. """
    if request.form['announcement']:
        new_a = Announcement(user_id=g.user.id, text=request.form['announcement'])
        new_a.insert()
        safe_commit()
        flash('Your announcement was stored', 'success')

    return redirect(url_for('announcements'))

@app.route('/daily-songs', methods=['GET'])
@login_required
def get_daily_songs():
    songs = DailySong.order_by(DailySong.created_on.desc()).all()
    song_of_the_day = get_song_of_the_day()
    return render_template('daily_songs.html', songs=songs,
                           song_of_the_day=song_of_the_day)

def extract_id_from_uri(uri):
    '''
    '''
    return uri[uri.rfind(':') + 1:]

@app.route('/daily-songs/add', methods=['POST'])
@login_required
def set_song():
    if request.form['spotify_uri'] and request.form['song_date']:
        song_details = get_song_details(request.form['spotify_uri'])
        new_song = DailySong(created_on=dateutil.parser.parse(request.form['song_date']).date(),
                             **song_details)
        new_song.insert()
        safe_commit()

    flash('Song set successfully!', 'success')
    return redirect(url_for('get_daily_songs'))

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

    album_seen_before = DailySong.filter_by(album_uri=song_details['album_uri']).first()

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

@app.route('/announcements', methods=['GET'])
def announcements():
    """ Loads all Announcements for today including the song of the day."""
    today = datetime.now().date()
    all_announcements = Announcement.filter(func.date(Announcement.created_on) == today).all()
    song_of_the_day = get_song_of_the_day(today)
    return render_template('timeline.html', all_announcements=all_announcements,
                           song_of_the_day=song_of_the_day)

@app.route('/queues', methods=['GET'])
@app.route('/queues/<string:user_id>', methods=['GET'])
def get_queues(user_id=None):
    pass

def datetimeformat(value, format='%m/%d/%Y %I:%M %p'):
    return value.strftime(format)

# Add some filters to Jinja
app.jinja_env.filters['gravatar'] = gravatar_url
app.jinja_env.filters['extract_id_from_uri'] = extract_id_from_uri
app.jinja_env.filters['datetimeformat'] = datetimeformat
