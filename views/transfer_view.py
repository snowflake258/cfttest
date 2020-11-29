from aiohttp.web import View, json_response, Request
from services import TransferSerivce, LimitService


class TransferView(View):
    def __init__(self, request: Request):
        self.__transfer_service = TransferSerivce(request.app['db'])
        super().__init__(request)

    async def post(self):
        result = await self.__transfer_service.make_transfer(await self.request.json())
        if result['ok']:
            return json_response(status=200, data={'transfer_id': result['transfer_id']})
        return json_response(status=400, data={'errors': result['errors']})
