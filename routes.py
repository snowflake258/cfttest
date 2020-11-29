from aiohttp.web import route
from views import LimitView, TransferView

routes = [
    route('GET', '/limit', LimitView),
    route('GET', '/limit/{id}', LimitView),
    route('POST', '/limit', LimitView),
    route('PUT', '/limit/{id}', LimitView),
    route('DELETE', '/limit/{id}', LimitView),

    route('POST', '/transfer', TransferView)
]
