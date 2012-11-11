from flask import Flask, request, session, g, redirect, url_for,\
                  abort, render_template, flash, _app_ctx_stack
from sqlite3 import dbapi2 as sqlite3
from werkzeug import check_password_hash, generate_password_hash

#config
DATABASE = '/tmp/5minutes.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object('config.Development')
app.config.from_object(__name__)


@app.route('/')
def root():
    return render_template('root.html', login='abc', logout='def')

@app.route('/', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    # if g.user:
        # return redirect(url_for('timeline'))
    error = None 
    register = None
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
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(url_for('timeline'))
    return render_template('root.html', error=error, register=register)

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

if __name__ == '__main__':
    init_db()
    app.run('0.0.0.0')
