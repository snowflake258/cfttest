from aiohttp.web import json_response
from marshmallow import ValidationError


def json_response_400(exp: Exception):
    errors = None
    print(exp)

    if isinstance(exp, ValidationError):
        errors = exp.messages
    elif isinstance(exp, ValueError):
        errors = {'id': str(exp)}

    return json_response(status=400, data={'errors': errors})
