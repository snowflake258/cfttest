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
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(limit.select().where(limit.c.id == id))
            record = await cursor.fetchone()
        return self.__item_to_dict(record)

    async def add(self, data: dict):
        errors = self.__check_data(data)
        if len(errors) > 0:
            return {'ok': False, 'errors': errors}

        async with self.__db.acquire() as conn:
            cursor = await conn.execute(limit.insert().values(**data))
            limit_id = await cursor.scalar()
        return {'ok': True, 'limit_id': limit_id}

    async def update(self, id: int, data: dict):
        errors = self.__check_data(data)
        if len(errors) > 0:
            return {'ok': False, 'errors': errors}

        async with self.__db.acquire() as conn:
            await conn.execute(limit.update().where(limit.c.id == id).values(**data))
        return {'ok': True}

    async def delete(self, id: int):
        async with self.__db.acquire() as conn:
            await conn.execute(limit.delete().where(limit.c.id == id))

    def __list_to_dict(self, records: list):
        result = []
        for item in records:
            result.append(self.__item_to_dict(item))
        return result

    @staticmethod
    def __item_to_dict(item: tuple):
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
