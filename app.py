from aiohttp.web import Application, run_app
from db.connection import connect_db, close_db
from routes import routes


app = Application()
app.add_routes(routes)
app.on_startup.append(connect_db)
app.on_cleanup.append(close_db)


if __name__ == '__main__':
    run_app(app)
