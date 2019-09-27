import json
from http import HTTPStatus

from flask import Response
from werkzeug.exceptions import abort


def validation_error_inform_error(err, data, schema):
    """
    Custom validation error handler which produces 404 Bad Request
    response in case validation fails and returns the error
    """
    abort(Response(
        json.dumps({'error': str(err), 'data': data, 'schema': schema}),
        status=HTTPStatus.BAD_REQUEST))
