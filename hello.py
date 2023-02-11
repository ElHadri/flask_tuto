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


# Form ------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class NameForm(FlaskForm):
   name = StringField('What is your name?', validators=[DataRequired()])
   submit = SubmitField('Submit')
# ------------------------------------------------------------------

from flask import flash


app = Flask(__name__)

bootstrap = Bootstrap(app)

moment = Moment(app)

app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/', methods=['GET', 'POST'])
def index():
   name = None
   form = NameForm()

   # this portion is for handling the form -------------------------------
   if form.validate_on_submit():
      session['name'] = form.name.data
      form.name.data = ''
      print(name)
      flash('Change submitted!') # we have to choose where we can display it in index.html

      return redirect(url_for('index'))
   # ---------------------------------------------------------------------

   return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
   return render_template('user.html', name=name, y=app.url_map)

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
   return render_template('500.html'), 500
