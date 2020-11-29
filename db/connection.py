from aiopg.sa import create_engine


async def connect_db(app):
    engine = await create_engine(
        database='cfttest',
        user='postgres',
        password='qdg058znm230',
        host='127.0.0.1',
        port='5432'
    )
    app['db'] = engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()
