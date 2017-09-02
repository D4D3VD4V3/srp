from app import create_app
import pytest


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    return app


@pytest.fixture(scope="session")
def db():
    from app import db
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
