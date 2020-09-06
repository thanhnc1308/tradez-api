import pytest

from application import create_app
from application.extensions import db


@pytest.fixture
def app():
    app = create_app("testing")
    # return app
    with app.app_context():
        yield app


@pytest.fixture
def app_context(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture(scope="function")
def database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield db


@pytest.fixture
def test_client(app, app_context):
    return app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db


@pytest.yield_fixture(scope="class", autouse=True)
def session(app, _db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = db.create_scoped_session(options=options)

        db.session = sess
        yield sess

        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()