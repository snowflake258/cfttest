from sqlalchemy import create_engine, MetaData
from db.models import limit, transfer


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[limit, transfer])


if __name__ == '__main__':
    engine = create_engine("postgresql://postgres:qdg058znm230@127.0.0.1:5432/cfttest")
    create_tables(engine)
