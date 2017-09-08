from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from . import db


class Login(db.Model, UserMixin):
    __tablename__ = 'login'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _rollno = db.Column(db.String, unique=True)
    _email = db.Column(db.String, unique=True)
    _passwordhash = db.Column(db.String(256))
    isadmin = db.Column(db.Boolean)

    def check_rollno(self, rollno):
        return check_password_hash(self._rollno, rollno)

    def check_email(self, email):
        return check_password_hash(self._email, email)

    def check_password(self, passwd):
        return check_password_hash(self._passwordhash, passwd)

    @property
    def rollno(self):
        raise AttributeError("Nice try!")

    @property
    def email(self):
        raise AttributeError("Nice try!")

    @property
    def password(self):
        raise AttributeError("Nice try!")

    @rollno.setter
    def rollno(self, rollno):
        self._rollno = generate_password_hash(rollno)

    @email.setter
    def email(self, email):
        self._email = generate_password_hash(email)

    @password.setter
    def password(self, password):
        self._passwordhash = generate_password_hash(password)

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
    name = db.Column(db.String(50), db.ForeignKey('professorsnames.name'))
    spec = db.Column(db.String(50))
    qual = db.Column(db.String(50))
# TODO pic?
    pic = db.Column(db.LargeBinary)
    exp = db.Column(db.Integer)
    sub = db.Column(db.String(50), db.ForeignKey('subjectsnames.name'))


class ProfessorsNames(db.Model):
    __tablename__ = "professorsnames"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)


class Subjects(db.Model):
    __tablename__ = 'subjects'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sem = db.Column(db.Integer)
    sub = db.Column(db.String(50))
    prof = db.Column(db.String(50), db.ForeignKey('professorsnames.name'))


class SubjectsNames(db.Model):
    __tablename__ = "subjectsnames"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)


class Reviews(db.Model):
    __tablename__ = 'reviews'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    studentuid = db.Column(db.Integer, db.ForeignKey('login.uid'))
    professoruid = db.Column(db.Integer, db.ForeignKey('professors.uid'))
    punctual = db.Column(db.Boolean)
    deathbypowerpoint = db.Column(db.Boolean)
    fairpaperevaluation = db.Column(db.Boolean)
    rating = db.Column(db.Integer)

    __table_args__ = (db.UniqueConstraint('studentuid', 'professoruid', name='compositeuid'),)
