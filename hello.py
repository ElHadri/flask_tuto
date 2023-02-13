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

import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

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

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite') # The URL of the application database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to use less memory unless signals for object changes are needed. 
db = SQLAlchemy(app)  # represents the database and provides access to all the functionality of Flask-SQLAlchemy.

@app.route('/', methods=['GET', 'POST'])
def index():
   name = None
   form = NameForm()

   # this portion is for handling the form -------------------------------
   if form.validate_on_submit():
      user = User.query.filter_by(username=form.name.data).first()
      if user is None:
         user = User(username=form.name.data)
         db.session.add(user)
         db.session.commit()
         session['known'] = False
      else:
         session['known'] = True
      session['name'] = form.name.data
      form.name.data = ''
      flash('Change submitted!') # we have to choose where we can render it in index.html
      return redirect(url_for('index'))
   # ---------------------------------------------------------------------

   return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
   return render_template('user.html', name=name, y=app.url_map)

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
   return render_template('500.html'), 500


# Models ------------------------------------------------------------------
class Role(db.Model):
   __tablename__ = 'roles'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(64), unique=True)
   
   def __repr__(self):  # give model a readable string representation that can be used for debugging and testing purposes.
      return '<Role %r>' % self.name
   
   # lazy='dynamic': to request that the query is not automatically executed. To return a query object not a list
   users = db.relationship('User', backref='role', uselist=True, lazy='dynamic')  # represents the object-oriented view of the relationship.

class User(db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(64), unique=True, index=True)
   
   def __repr__(self):  # give model a readable string representation that can be used for debugging and testing purposes.
      return '<User %r>' % self.username

   role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

   # role (hidden attribute - object-oriented view ) !!

class Modele(db.Model):
   __tablename__ = 'Modeles'
   id = db.Column(db.Integer, primary_key=True)
   label = db.Column(db.String(64), unique=True)
   
   def __repr__(self):  # give model a readable string representation that can be used for debugging and testing purposes.
      return '<Modele %r>' % self.label

# -------------------------------------------------------------------------

@app.shell_context_processor
def make_shell_context():
   return dict(db=db, User=User, Role=Role)

from flask_migrate import Migrate
migrate = Migrate(app, db)