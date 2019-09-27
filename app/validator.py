import json
import os
from http import HTTPStatus

from flasgger import validate
from flask import Response
from flask import current_app as app
from werkzeug.exceptions import abort


def validation_error_inform_error(err, data, schema):
    """
    Custom validation error handler which produces 404 Bad Request
    response in case validation fails and returns the error
    """
    abort(Response(
        json.dumps({'error': str(err), 'data': data, 'schema': schema}),
        status=HTTPStatus.BAD_REQUEST))


def validate_data(data, validation_type):
    validate(data,
             validation_type,
             os.path.join(app.root_path, 'swagger.yml'),
             validation_error_handler=validation_error_inform_error)
