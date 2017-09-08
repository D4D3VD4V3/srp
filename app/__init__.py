from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_restless import APIManager

SECRET_KEY = 'ffasdhfas;ofmjasdfhzizvmhdlahfm;oginlamfwldsafhks;foajflasjdfap9'
nav = Nav()


@nav.navigation(id='bar')
def bar():
    if current_user.is_authenticated:
        return Navbar(View("Home", "bp.home"), View("".join(["Log out (", current_user.email, ")"]), "bp.logout"))
    return Navbar(View("Home", "bp.home"), View("Sign Up", "bp.signup"), View("Login", "bp.login", next=request.path))


db = SQLAlchemy()
login = LoginManager()
restless = APIManager(flask_sqlalchemy_db = db)


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/main.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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

    restless.init_app(app)

    from .models import ProfessorsNames, Professors
    with app.app_context():
        restless.create_api(ProfessorsNames, app=app, methods=["GET", "POST"])
        restless.create_api(Professors, app=app, methods=["GET", "POST"])

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
