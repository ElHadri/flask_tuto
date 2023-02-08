from flask import Flask
from flask import request
from flask import current_app
from flask import g
from flask import session
from flask import make_response
from flask import redirect
from flask import abort
from flask import render_template
from flask import url_for

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime



app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
   return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
   return render_template('user.html', name=name, y=app.url_map)

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
   return render_template('500.html'), 500