from aiohttp.web import View, json_response, Request
from services import LimitService


class LimitView(View):
    def __init__(self, request: Request):
        self.__limit_service = LimitService(request.app['db'])
        super().__init__(request)

    async def get(self):
        id = self.__get_id
        if id is not None:
            if not await self.__limit_service.exists(id):
                return json_response(status=400, data={'data': 'Incorrect identifier of \'Limit\'.'})
            return json_response({'limit': await self.__limit_service.get_item(id)})

        return json_response({'limits': await self.__limit_service.get_list()})

    async def post(self):
        result = await self.__limit_service.add(await self.request.json())

        if result['ok']:
            return json_response({'limit_id': result['limit_id']})
        return json_response(status=400, data={'errors': result['errors']})

    async def put(self):
        id = self.__get_id
        if not await self.__limit_service.exists(id):
            return json_response(status=400, data={'data': 'Incorrect identifier of \'Limit\'.'})

        result = await self.__limit_service.update(id, await self.request.json())
        if result['ok']:
            return json_response({})
        return json_response(status=400, data={'errors': result['errors']})

    async def delete(self):
        id = self.__get_id
        if not await self.__limit_service.exists(id):
            return json_response(status=400, data={'data': 'Incorrect identifier of \'Limit\'.'})

        await self.__limit_service.delete(id)
        return json_response({})

    @property
    def __get_id(self):
        return self.request.match_info.get('id', None)
