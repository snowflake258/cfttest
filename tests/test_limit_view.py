import json
from .cli import cli


async def create_limit(cli):
    resp = await cli.post(
        '/limit',
        data=json.dumps(dict(country="RUS", currency="RUB", max_sum_per_month="1000.15"))
    )
    return (await resp.json())['limit_id']


async def test_limit_view_get(cli):
    resp = await cli.get('/limit')
    assert resp.status == 200

    resp = await cli.get('/limit/1')
    assert resp.status == 200

    resp = await cli.get('/limit/0')
    assert resp.status == 400


async def test_limit_view_post(cli):
    resp = await cli.post(
        '/limit',
        data=json.dumps(dict(country="RUS", currency="RUB", max_sum_per_month="999999999.99"))
    )
    assert resp.status == 200


async def test_limit_view_put(cli):
    resp = await cli.put(
        '/limit/0',
        data=json.dumps(dict(country="RUS", currency="RUB", max_sum_per_month="999999999.99"))
    )
    assert resp.status == 400

    limit_id = await create_limit(cli)
    resp = await cli.put(
        f'/limit/{limit_id}',
        data=json.dumps(dict(country="RUS", currency="RUB", max_sum_per_month="11.111"))
    )
    assert resp.status == 200


async def test_limit_view_delete(cli):
    resp = await cli.delete('/limit/0')
    assert resp.status == 400
    print(await resp.json())

    limit_id = await create_limit(cli)
    resp = await cli.delete(f'/limit/{limit_id}')
    assert resp.status == 200
