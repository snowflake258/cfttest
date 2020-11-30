from aiohttp.web import Application
from routes import routes
from db.configuration import connect_db, close_db
import pytest


@pytest.fixture
def cli(loop, aiohttp_client):
    app = Application()
    app.add_routes(routes)
    app.on_startup.append(connect_db)
    app.on_cleanup.append(close_db)
    return loop.run_until_complete(aiohttp_client(app))
