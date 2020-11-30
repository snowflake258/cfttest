from db.models import transfer


class TransferSerivce:
    def __init__(self, db):
        self.__db = db

    async def make_transfer(self, data: dict):
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(transfer.insert().values(**data))
            transfer_id = await cursor.scalar()
        return transfer_id

    async def get_transfers(self, limit_id: int):
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(transfer.select().where(transfer.c.limit_id == limit_id))
            records = await cursor.fetchall()
        return records
