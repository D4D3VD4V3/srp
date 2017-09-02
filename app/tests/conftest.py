from app import create_app, db
# from app.models import Login
import pytest


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    return app


@pytest.fixture(scope="session")
def db():
    db.drop_all()
    db.create_all()
    # user = Login(email="testingaccount@tests.com", password="securepasslol", rollno=9999999999)
    # db.session.add(user)
    # db.session.commit()
    yield db
