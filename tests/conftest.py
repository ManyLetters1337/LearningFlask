import sqlalchemy
import pytest
from create_app import create_app


class DatabaseLoader:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            db_name = 'test_db'

            engine = sqlalchemy.create_engine('mysql+pymysql://manyletters:12345678*Aa@localhost/test_db')
            engine.execute(f"DROP DATABASE IF EXISTS {db_name};")
            engine.execute(f"CREATE DATABASE {db_name};")
            engine.execute(f"USE {db_name};")

            cls._instance = super(DatabaseLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance


@pytest.fixture(scope="session")
def init_notes_app():
    db_url = 'mysql+pymysql://manyletters:12345678*Aa@localhost/test_db'
    app = create_app(db_url, False)

    context = app.app_context()
    context.push()

    DatabaseLoader()

    with app.test_client() as app:
        yield app
