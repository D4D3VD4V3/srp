from flask import render_template, flash, url_for, redirect
from . import bp
from app.forms import SignUpForm


@bp.route("/")
def home():
    return render_template("home.html")

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
#TODO Check this out
        return redirect(url_for("bp.home"))
    return render_template("signup.html", form=form)

@bp.route("/test")
def test():
    return render_template("newhome.html")

@bp.route("/semester/<int:sem>")
def semester():
    return "It worked" + str(sem)
