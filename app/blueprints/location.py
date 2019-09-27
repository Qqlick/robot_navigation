import os

from flasgger import validate
from flask import Blueprint, jsonify, request, json
from flask import current_app as app

from app.models import Location, DecimalEncoder
from app.validator import validation_error_inform_error

location = Blueprint('location', __name__, url_prefix='/location')


@location.route('', methods=["POST"])
def save_location_to_db():
    validate(request.json,
             'location',
             os.path.join(app.root_path, 'swagger.yml'),
             validation_error_handler=validation_error_inform_error)
    save_result = Location(**request.json).save()

    return jsonify(save_result)


@location.route('/<location_name>')
def get_location(location_name):
    loc = Location(name=location_name).get()
    return json.dumps(loc, cls=DecimalEncoder)
