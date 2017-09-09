from itertools import chain
from werkzeug.security import generate_password_hash
from urllib.parse import unquote
from flask import render_template, flash, url_for, redirect, request, jsonify
from . import bp
from app.forms import SignUpForm, LoginForm, ReviewForm
from app.models import Login, Subjects, Professors, Reviews, ProfessorsNames
from app import db
from flask_login import login_user, login_required, logout_user, current_user


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
            flash("Account created successfully. Please login now", "success")
            return redirect(url_for("bp.login"))
    return render_template("signup.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    nexturl = request.args.get('next')
    if form.validate_on_submit():
        # user = Login.query.filter_by(email=generate_password_hash(form.Email_Address.data)).first()
        users = Login.query.all()
        user = None
        for i in users:
            if i.check_email(form.Email_Address.data):
                user = i
                break

        if user is not None and user.check_password(form.Password.data):
            login_user(user, remember=form.RememberMe.data)
            flash("Login successful", "success")
            if nexturl:
                return redirect(nexturl)
            else:
                return redirect(url_for("bp.home"))
        flash("Invalid credentials", "danger")
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
    if profs:
        proflist = set([i.prof for i in profs])
    else:
        flash("Invalid subject", "danger")
        return redirect(url_for("bp.home"))
    return render_template("subject.html", profs=proflist)


@bp.route("/professor/<profid>", methods=["GET", "POST"])
def professor(profid):
    prof = Professors.query.filter_by(name=unquote(profid)).first()
    if prof is None:
        flash("No professor by that name", "danger")
        return redirect(url_for("bp.home"))
    form = ReviewForm()
    disabled = "False"
    if db.session.query(Reviews).filter(
                Reviews.studentuid == current_user.get_id()).filter(
                Reviews.professoruid == prof.uid).one_or_none() is not None:
        disabled = "True"
        flash("You've already reviewed this professor. Only one review per student", "danger")
    if form.validate_on_submit():
        if db.session.query(Reviews).filter(
                    Reviews.studentuid == current_user.get_id()).filter(
                    Reviews.professoruid == prof.uid).one_or_none() is None:
            review = Reviews(
                studentuid=int(current_user.get_id()),
                professoruid=int(prof.uid),
                punctual=form.Punctual.data,
                deathbypowerpoint=form.DeathByPPT.data,
                fairpaperevaluation=form.FairPaperEvaluation.data,
                rating=form.Rating.data)
            db.session.add(review)
            db.session.commit()
            disabled = "True"
            flash("Review submitted successfully", "success")
        else:
            disabled = "True"
            flash("You've already reviewed this professor. Only one review per student", "danger")

    if current_user.is_authenticated is False:
        flash("You cannot leave a review unless you're logged in", "danger")
    fields = ["punctual", "reliesonppt", "fairpaperevaluation", "rating"]
    statistics = {k: 0 for k in fields}
    stats = Reviews.query.filter_by(professoruid=prof.uid).all()
    if stats is not None:
        for stat in stats:
            # for i in fields:
            # statistics[i] += stat[i]
            statistics["punctual"] += stat.punctual
            statistics["reliesonppt"] += stat.deathbypowerpoint
            statistics["fairpaperevaluation"] += stat.fairpaperevaluation
            statistics["rating"] += stat.rating
            statistics["rating"] /= len(stats)

    return render_template("profile.html", prof=prof, form=form, statistics=statistics, disabled=disabled)


@bp.route("/data")
def data():
    names = ProfessorsNames.query.with_entities(ProfessorsNames.name).all()
    flattened_names = list(chain.from_iterable(names))
    flat_dict = {"data": flattened_names}
    return jsonify(flat_dict)


@bp.after_request
def cache(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response
