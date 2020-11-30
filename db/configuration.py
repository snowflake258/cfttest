from sqlalchemy import create_engine, MetaData
from aiopg.sa import create_engine as aiopg_create_engine
from db.models import limit, transfer


db_config = {
    'database': 'cfttest',
    'user': 'postgres',
    'password': 'qdg058znm230',
    'host': '127.0.0.1',
    'port': '5432'
}


def init_db():
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    meta = MetaData()
    meta.create_all(bind=engine, tables=[limit, transfer])

    conn = engine.connect()
    conn.execute(limit.insert(), [
        dict(country="RUS", currency="RUB", max_sum_per_month="1000.15"),
        dict(country="AUS", currency="USD", max_sum_per_month="2000.46")
    ])
    conn.close()

async def connect_db(app):
    engine = await aiopg_create_engine(**db_config)
    app['db'] = engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()
