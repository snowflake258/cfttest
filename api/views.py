from aiohttp.web import View, json_response, Request
from containers import Container
from api.schemes import LimitSchema, TransferSchema
from api.responses import json_response_400


class LimitView(View):
    def __init__(self, request: Request):
        super().__init__(request)
        self.__limit_service = Container.limit_service(request.app['db'])

    async def get(self):
        if self.__get_id is None:
            return json_response({'limits': await self.__limit_service.get_list()})

        try:
            return json_response(status=200, data={'limit': await self.__limit_service.get_item(self.__get_id)})
        except Exception as exp:
            return json_response_400(exp)

    async def post(self):
        try:
            data = LimitSchema().load(await self.request.json())
            limit_id = await self.__limit_service.add(data)
            return json_response(status=200, data={'limit_id': limit_id})
        except Exception as exp:
            return json_response_400(exp)

    async def put(self):
        try:
            data = LimitSchema().load(await self.request.json())
            await self.__limit_service.update(self.__get_id, data)
            return json_response(status=200)
        except Exception as exp:
            return json_response_400(exp)

    async def delete(self):
        try:
            await self.__limit_service.delete(self.__get_id)
            return json_response(status=200)
        except Exception as exp:
            return json_response_400(exp)

    @property
    def __get_id(self):
        return self.request.match_info.get('id', None)


class TransferView(View):
    def __init__(self, request: Request):
        super().__init__(request)
        self.__limit_service = Container.limit_service(request.app['db'])

    async def post(self):
        try:
            data = await self.request.json()
            limit = await self.__limit_service.get_item(data['limit_id'])

            schema = TransferSchema(limit)
            validated_data = schema.load(data)

            transfer_id = await self.__transfer_service.make_transfer(validated_data)
            return json_response(status=200, data={'transfer_id': transfer_id})
        except Exception as exp:
            return json_response_400(exp)
