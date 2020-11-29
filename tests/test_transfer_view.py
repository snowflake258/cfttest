import json
from .cli import cli
from .test_limit_view import create_limit


async def test_transfer_view_post(cli):
    limit_id = await create_limit(cli)
    resp = await cli.post(
        '/transfer',
        data=json.dumps(dict({
            "sum": 111.45,
            "country": "RUS",
            "currency": "USD",
            "limit_id": limit_id
        }))
    )
    assert resp.status == 400

    resp = await cli.post(
        '/transfer',
        data=json.dumps(dict({
            "sum": 111.45,
            "country": "RUS",
            "currency": "RUB",
            "limit_id": 0
        }))
    )
    assert resp.status == 400

    resp = await cli.post(
        '/transfer',
        data=json.dumps(dict({
            "sum": 1000000000.45,
            "country": "RUS",
            "currency": "RUB",
            "limit_id": limit_id
        }))
    )
    assert resp.status == 400

    resp = await cli.post(
        '/transfer',
        data=json.dumps(dict({
            "sum": 111.45,
            "country": "RUS",
            "currency": "RUB",
            "limit_id": limit_id
        }))
    )
    assert resp.status == 200
