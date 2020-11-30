from db.models import transfer


class TransferSerivce:
    def __init__(self, db):
        self.__db = db

    async def make_transfer(self, data: dict):
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(transfer.insert().values(**data))
            transfer_id = await cursor.scalar()
        return transfer_id
