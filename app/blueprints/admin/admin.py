from urllib.parse import unquote
from flask import render_template, flash, url_for, redirect, request
from . import admin_bp
from app.forms import SignUpForm, LoginForm, ReviewForm
from app.models import Login, Subjects, Professors, Reviews
from app import db
from flask_login import login_user, login_required, logout_user, current_user



@admin_bp.route('/')
def home():
    return "test"


