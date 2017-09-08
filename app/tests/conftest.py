from app import create_app
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Session = sessionmaker()
engine = create_engine("sqlite:///C:/Users/david/Desktop/srp/srp/app/db/main.db")


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    return app


@pytest.fixture(scope="session")
def db():
    connection = engine.connect()
    trans = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    trans.rollback()
    connection.close()
