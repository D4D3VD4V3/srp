from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from . import db


class Login(db.Model, UserMixin):
    __tablename__ = 'login'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rollno = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(50), unique=True)
    _passwordhash = db.Column(db.String(256))
    isadmin = db.Column(db.Boolean)

    def check_password(self, passwd):
        return check_password_hash(self._passwordhash, passwd)

    @property
    def password(self):
        raise AttributeError("Nice try!")

    @password.setter
    def password(self, password):
        self._passwordhash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._passwordhash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uid


class Professors(db.Model):
    __tablename__ = 'professors'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    spec = db.Column(db.String(50))
    qual = db.Column(db.String(50))
    pic = db.Column(db.LargeBinary)
    exp = db.Column(db.Integer)
    sub = db.Column(db.String(50), db.ForeignKey('subjects.sub'))


class Subjects(db.Model):
    __tablename__ = 'subjects'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sem = db.Column(db.Integer)
    sub = db.Column(db.String(50))
    prof = db.Column(db.String(50), db.ForeignKey('professors.name'))


class Reviews(db.Model):
    __tablename__ = 'reviews'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    studentuid = db.Column(db.Integer, db.ForeignKey('login.uid'))
    professoruid = db.Column(db.Integer, db.ForeignKey('professors.uid'))
    __table_args__ = (db.UniqueConstraint('studentuid', 'professoruid', name='compositeuid'),)
