from aiohttp.web import View, json_response, Request
from marshmallow import ValidationError
from services import LimitService, TransferSerivce
from api.schemes import LimitSchema, TransferSchema


class LimitView(View):
    def __init__(self, request: Request):
        self.__limit_service = LimitService(request.app['db'])
        super().__init__(request)

    async def get(self):
        if self.__get_id is None:
            return json_response({'limits': await self.__limit_service.get_list()})

        try:
            return json_response(status=200, data={'limit': await self.__limit_service.get_item(self.__get_id)})
        except ValueError as error:
            return json_response(status=400, data={'errors': [str(error)]})

    async def post(self):
        try:
            data = await LimitSchema().load(await self.request.json())
            limit_id = await self.__limit_service.add(data)
            return json_response(status=200, data={'limit_id': limit_id})
        except ValidationError as error:
            return json_response(status=400, data={'errors': error.messages})

    async def put(self):
        try:
            data = await LimitSchema().load(await self.request.json())
            await self.__limit_service.update(self.__get_id, data)
            return json_response(status=200)
        except ValidationError as error:
            return json_response(status=400, data={'errors': error.messages})
        except ValueError as error:
            return json_response(status=400, data={'errors': [str(error)]})

    async def delete(self):
        try:
            await self.__limit_service.delete(self.__get_id)
            return json_response(status=200)
        except ValueError as error:
            return json_response(status=400, data={'errors': [str(error)]})

    @property
    def __get_id(self):
        return self.request.match_info.get('id', None)


class TransferView(View):
    def __init__(self, request: Request):
        super().__init__(request)

        self.__limit_service = LimitService(request.app['db'])
        self.__transfer_service = TransferSerivce(request.app['db'])

    async def post(self):
        try:
            schema = TransferSchema(self.__limit_service, self.__transfer_service)
            data = await schema.load(await self.request.json())

            transfer_id = await self.__transfer_service.make_transfer(data)
            return json_response(status=200, data={'transfer_id': transfer_id})
        except ValidationError as error:
            return json_response(status=400, data={'errors': error.messages})
