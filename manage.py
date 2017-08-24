from flask_script import Manager, Command
from app import create_app

manager = Manager(create_app)


class CreateDB(Command):

    def run(self):
        from app import db
        db.create_all()

if __name__ == "__main__":
    manager.add_command('createdb', CreateDB())
    manager.run()
