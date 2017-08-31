from urllib.parse import unquote
from flask import render_template, flash, url_for, redirect, request
from . import bp
from app.forms import SignUpForm, LoginForm, ReviewForm
from app.models import Login, Subjects, Professors, Reviews
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
        user = Login.query.filter_by(email=form.Email_Address.data).first()
        if user is not None and user.verify_password(form.Password.data):
            login_user(user, remember=form.RememberMe.data)
            flash("Login successful", "success")
            if nexturl:
                return redirect(nexturl)
            else:
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
    prof = Professors.query.filter_by(name=unquote(profid)).first()
    form = ReviewForm()
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
            flash("Review submitted successfully", "success")
        else:
            flash("You've already reviewed this professor. Only one review per student", "danger")
    if current_user.is_authenticated is False:
        flash("You cannot leave a review unless you're logged in", "danger")
    fields = ["punctual", "deathbypowerpoint", "fairpaperevaluation", "rating"]
    statistics = {k: 0 for k in fields}
    stats = Reviews.query.filter_by(professoruid=prof.uid).all()
    count = len(stats)
    print(count)
    if stats is not None:
        for stat in stats:
            # for i in fields:
            # statistics[i] += stat[i]
            statistics["punctual"] += stat.punctual
            statistics["deathbypowerpoint"] += stat.deathbypowerpoint
            statistics["fairpaperevaluation"] += stat.fairpaperevaluation
            statistics["rating"] += stat.rating

    return render_template("profile.html", prof=prof, form=form, statistics=statistics)


@bp.after_request
def cache(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response