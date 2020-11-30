from aiohttp.web import Application, run_app
from db.configuration import connect_db, close_db
from routes import routes


def create_app():
    app = Application()
    app.add_routes(routes)
    app.on_startup.append(connect_db)
    app.on_cleanup.append(close_db)
    return app


if __name__ == '__main__':
    app = create_app()
    run_app(app)
