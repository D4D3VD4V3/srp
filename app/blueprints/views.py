from urllib.parse import unquote
from flask import render_template, flash, url_for, redirect
from . import bp
from app.forms import SignUpForm, LoginForm, ReviewForm
from app.models import Login, Subjects, Professors
from app import db
from flask_login import login_user, login_required, logout_user


@bp.route("/")
def home():
    return render_template("newhome.html")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if db.session.query(Login.uid).filter_by(email=form.Email_Address1.data).scalar() is not None:
            flash("The account already exists!", "danger")
        else:
            user = Login(
                rollno=form.Roll_Number.data,
                email=form.Email_Address1.data,
                password=form.Password1.data,
                isadmin=False)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("bp.home"))
    return render_template("signup.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.Email_Address.data).first()
        if user is not None and user.verify_password(form.Password.data):
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("bp.home"))
    return render_template("login.html", form=form)


@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Successfully logged out", "success")
    return redirect(url_for("bp.home"))


@bp.route("/semester/<int:sem>")
def semester(sem):
    subs = Subjects.query.filter_by(sem=sem).all()
    sublist = set([i.sub for i in subs])
    return render_template("semester.html", subs=sublist)


@bp.route("/subject/<subid>")
def subject(subid):
    profs = Subjects.query.filter_by(sub=unquote(subid)).all()
    proflist = set([i.prof for i in profs])
    return render_template("subject.html", profs=proflist)


@bp.route("/professor/<profid>", methods=["GET", "POST"])
def professor(profid):
    form = ReviewForm()
    if form.validate_on_submit():
        flash("rating:" + str(form.Rating.data), "success")
    prof = Professors.query.filter_by(name=unquote(profid)).first()
    return render_template("profile.html", prof=prof, form=form)


# @bp.route("/review/<name>")
# def review(name):
    # return unquote(name)
