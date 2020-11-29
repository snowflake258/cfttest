from db.models import transfer
from services import LimitService
from datetime import datetime


class TransferSerivce:
    def __init__(self, db):
        self.__db = db
        self.__limit_service = LimitService(db)

    async def make_transfer(self, data: dict):
        errors = await self.__check_data(data)

        if len(errors) > 0:
            return {'ok': False, 'errors': errors}

        async with self.__db.acquire() as conn:
            cursor = await conn.execute(transfer.insert().values(**data))
            transfer_id = await cursor.scalar()
        return {'ok': True, 'transfer_id': transfer_id}

    async def __check_data(self, data: dict):
        errors = []

        if data.get('sum', None) is None:
            errors.append('You must enter sum.')
        if data.get('country', None) is None:
            errors.append('You must enter country.')
        if data.get('currency', None) is None:
            errors.append('You must enter currency.')
        if data.get('limit_id', None) is None:
            errors.append('You must enter limit_id.')

        if len(errors) > 0:
            return errors

        if data.get('limit_id', None) is None or not await self.__limit_service.exists(data['limit_id']):
            errors.append('Incorrect identifier of \'Limit\'.')
            return errors

        limit = await self.__limit_service.get_item(data['limit_id'])
        transfers = await self.__get_transfers(data['limit_id'])
        allowed_sum = await self.__get_allowed_sum_for_transfer(limit, transfers)

        if data['sum'] > allowed_sum:
            errors.append(f'Your can\' tranfer {data["sum"]} {data["currency"]}. You have reached the limit for this '
                          f'month. Limit - {limit["max_sum_per_month"]}. Allowed sum for transfer - {allowed_sum}.')

        if data['currency'] != limit['currency']:
            errors.append(f'Incorrect currency. You must use {limit["currency"]}.')

        return errors

    async def __get_transfers(self, limit_id: int):
        async with self.__db.acquire() as conn:
            cursor = await conn.execute(transfer.select().where(transfer.c.limit_id == limit_id))
            records = await cursor.fetchall()
        return records

    @staticmethod
    async def __get_allowed_sum_for_transfer(limit, transfers):
        month_sum = 0
        current_month = datetime.now().date().month

        for item in transfers:
            if item['time'].date().month == current_month:
                month_sum += item['sum']

        return limit['max_sum_per_month'] - month_sum
