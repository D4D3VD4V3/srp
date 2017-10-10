from os import makedirs, path
from random import choice, randint
from flask_script import Manager
from app import create_app
from app.models import SubjectsNames, ProfessorsNames, Subjects, Professors, Login
import mimesis

manager = Manager(create_app)


@manager.command
def createdb():
    if not path.exists(path.join(path.dirname(__file__), 'app', 'db')):
        makedirs(path.join(path.dirname(__file__), 'app', 'db'))

        from app import db
        db.drop_all()
        db.create_all()
        subs = ["Computer Networks", "Unix Internals", "Digital Communications",
                "Digital Principles and Design", "Computer Architecture",
                "Digital Signal Processing", "Engineering Graphics",
                "Operating Systems", "Discrete Mathematics"]

        p = mimesis.Personal(locale='en')
        profs = [p.full_name() for i in range(20)]

        for i in subs:
            db.session.add(SubjectsNames(name=i))

        for i in profs:
            db.session.add(ProfessorsNames(name=i))

        for i in range(1, 9):
            for j in range(randint(5, 7)):
                db.session.add(Subjects(sem=i, sub=choice(subs), prof=choice(profs)))

        for name in profs:
            db.session.add(
                Professors(
                    name=name, spec=choice(subs),
                    qual=choice(["Master's", "PhD"]) + " in " + choice(subs),
                    exp=randint(2, 20)))

        db.session.add(Login(rollno="00000000", email="admin@admin.com", password="password", isadmin=True))
        db.session.commit()


if __name__ == "__main__":
    manager.run()
