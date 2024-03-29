# application routes in main blueprint
from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from flask import flash


@main.route('/', methods=['GET', 'POST'])
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
        return redirect(url_for('.index'))
   # ---------------------------------------------------------------------


    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), known=session.get('known', False))


@main.route('/user/<name>')
def user(name):
   return render_template('user.html', name=name, y=app.url_map)
