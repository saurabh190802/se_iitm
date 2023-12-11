"""
    Flask app is created and configured
    DB, blueprints are registered
"""
import os

# Library imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# File imports
from .database import db
from .models import *
from . import auth, posts, quiz, achievement, search, profile, home


def create_app(test_config=None):
    """
        create and configure the app
    """
    app = Flask(__name__, instance_relative_config=True,template_folder="templates")
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'project.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #initializing app with db
    db.init_app(app)

    #Creates db and tables if not present. If tables are already present in db, doesn't update them
    with app.app_context():
        db.create_all()

    #Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)
    app.register_blueprint(quiz.bp)
    app.register_blueprint(achievement.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(home.bp)

    #Serve the html file to kickoff frontend
    @app.route("/")
    def index():
        return render_template("application.html")

    return app
