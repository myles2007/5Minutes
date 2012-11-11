from flask import Flask, request, session, g, redirect, url_for,\
                  abort, render_template, flash

app = Flask(__name__)
app.config.from_object('config.Development')

@app.route('/')
def root():
    return render_template('root.html', login='abc', logout='def')

if __name__ == '__main__':
    app.run('0.0.0.0')
