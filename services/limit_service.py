from sqlalchemy import select
from itertools import groupby
from db.models import limit, transfer


class LimitService:
    def __init__(self, db):
        self.__db = db

    @property
    def __select_data(self):
        return select([
                limit.c.id,
                limit.c.country,
                limit.c.currency,
                limit.c.max_sum_per_month,
                transfer.c.id.label('transfer_id'),
                transfer.c.time.label('transfer_time'),
                transfer.c.country.label('transfer_country'),
                transfer.c.currency.label('transfer_currency'),
                transfer.c.sum.label('transfer_sum')
            ]).select_from(limit.outerjoin(transfer))

    async def exists(self, id: int):
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(limit.select().where(limit.c.id == id))
            record = await cursor.fetchone()
            if record is None:
                return False
        return True

    async def get_list(self):
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(self.__select_data)
            records = await cursor.fetchall()

        return self.__parse_data(records)

    async def get_item(self, id: int):
        await self.__check_id(id)

        async with self.__db.acquire() as conn:
            cursor = await conn.execute(self.__select_data.where(limit.c.id == id))
            records = await cursor.fetchall()

        return self.__parse_data(records)[0]

    async def add(self, data: dict):
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(limit.insert().values(**data))
            limit_id = await cursor.scalar()
        return limit_id

    async def update(self, id: int, data: dict):
        await self.__check_id(id)

        async with self.__db.acquire() as conn:
            await conn.execute(limit.update().where(limit.c.id == id).values(**data))

    async def delete(self, id: int):
        await self.__check_id(id)

        async with self.__db.acquire() as conn:
            await conn.execute(limit.delete().where(limit.c.id == id))

    async def __check_id(self, id: int):
        if id is None or not await self.exists(id):
            raise ValueError('Incorrect identifier of limit.')

    def __parse_data(self, records: list):
        result = []
        for limit, transfers in groupby(records, lambda x: (x[0], x[1], x[2], x[3])):
            result.append(self.__parse_item(limit, transfers))
        return result

    @staticmethod
    def __parse_item(item: tuple, transfers: list):
        if item is None:
            return None

        result = {
            'id': item[0],
            'country': item[1].value,
            'currency': item[2].value,
            'max_sum_per_month': item[3]
        }

        transfers_of_item = []
        for tr in transfers:
            if tr[4] is not None:
                transfers_of_item.append({
                    'id': tr[4],
                    'time': tr[5].strftime("%m/%d/%Y, %H:%M:%S"),
                    'country': tr[6].value,
                    'currency': tr[7].value,
                    'sum': tr[8],
                })
        result['transfers'] = transfers_of_item

        return result
