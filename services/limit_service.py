from db.models import limit


class LimitService:
    def __init__(self, db):
        self.__db = db

    async def exists(self, id: int):
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(limit.select().where(limit.c.id == id))
            record = await cursor.fetchone()
            if record is None:
                return False
        return True

    async def get_list(self):
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(limit.select())
            records = await cursor.fetchall()
        return self.__list_to_dict(records)

    async def get_item(self, id: int):
        await self.__check_id(id)

        async with self.__db.acquire() as conn:
            cursor = await conn.execute(limit.select().where(limit.c.id == id))
            record = await cursor.fetchone()
        return self.__item_to_dict(record)

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

    def __list_to_dict(self, records: list):
        result = []
        for item in records:
            result.append(self.__item_to_dict(item))
        return result

    @staticmethod
    def __item_to_dict(item: tuple):
        if item is None:
            return None

        return {
            'id': item[0],
            'country': item[1].value,
            'currency': item[2].value,
            'max_sum_per_month': item[3],
        }

    @staticmethod
    def __check_data(data: dict):
        errors = []

        if data.get('country', None) is None:
            errors.append('You must enter country.')
        if data.get('max_sum_per_month', None) is None:
            errors.append('You must enter max_sum_per_month.')
        elif float(data.get('max_sum_per_month')) < 0:
            errors.append('Value max_sum_per_month must be positive number.')

        return errors
