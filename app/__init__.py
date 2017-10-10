import os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

SECRET_KEY = os.getenv("SECRET_KEY", "ffasdhfas;ofmjasdfhzizvmhdlahfm;oginlamfwldsafhks;foajflasjdfap9")
nav = Nav()


@nav.navigation(id="bar")
def bar():
    if current_user.is_authenticated:
        return Navbar(View("Home", "bp.home"), View("Log out", "bp.logout"))
    return Navbar(View("Home", "bp.home"), View("Sign Up", "bp.signup"), View("Login", "bp.login", next=request.path))


db = SQLAlchemy()
login = LoginManager()


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///db/main.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #TODO:Check for debug config
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    Bootstrap(app)
    nav.init_app(app)
    db.init_app(app)
    login.init_app(app)
    login.login_message = "You must login first"
    login.login_view = "bp.login"

    from .models import Login

    @login.user_loader
    def load_user(uid):
        return Login.query.get(int(uid))

    from app.blueprints.general import bp
    from app.blueprints.admin import admin_bp
    app.register_blueprint(bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.errorhandler(404)
    def pagenotfound(_):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def servererror(_):
        return render_template("500.html"), 500

    return app
