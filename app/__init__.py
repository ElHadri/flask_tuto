# app package constructor
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy() # represents the database and provides access to all the functionality of Flask-SQLAlchemy.

# the application factory, which takes as an argument the name of a configuration to use for the application. 
def create_app(config_name):
    # app creation
    app = Flask(__name__)
    # app configuration
    app.config.from_object(config[config_name]) # The configuration settings stored in one of the classes defined in config.py can be imported directly into the application using the from_object()
    # app initiation
    config[config_name].init_app(app) # To allow more complex initialization procedures to take place.
    # extensions initiation
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # attach routes and custom error pages here

    from .main import main as main_blueprint # main blueprint registration
    app.register_blueprint(main_blueprint)

    return app