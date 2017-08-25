from random import choice, randint
from flask_script import Manager, Command
from app import create_app
from app.models import SubjectsNames, ProfessorsNames, Subjects, Professors

manager = Manager(create_app)


class CreateDB(Command):

    def run(self):
        from app import db
        db.create_all()
        subs = ["Computer Networks", "Unix Internals", "Digital Communications",
                "Digital Principles and Design", "Computer Architecture",
                "Fundamentals of Computing", "Engineering Graphics",
                "Operating Systems", "Discrete Mathematics"]

        profs = ["Prof " + chr(i) for i in range(65, 91)]

        for i in subs:
            db.session.add(SubjectsNames(name=i))

        for i in profs:
            db.session.add(ProfessorsNames(name=i))

        for i in range(1, 9):
            for j in range(randint(5, 7)):
                db.session.add(Subjects(sem=i, sub=choice(subs), prof=choice(profs)))

        db.session.commit()


if __name__ == "__main__":
    manager.add_command('createdb', CreateDB())
    manager.run()
