from flask import Blueprint, jsonify, request, json

from app.models import Location, DecimalEncoder
from app.utils import allowed_file
from app.validator import validate_data

location = Blueprint('location', __name__, url_prefix='/location')


@location.route('', methods=["POST"])
def save_location_to_db():
    validate_data(request.json, 'location')
    save_result = Location(**request.json).save()
    return jsonify(save_result)


@location.route('/<location_name>')
def get_location(location_name):
    loc = Location(name=location_name).get()
    status = loc['ResponseMetadata']['HTTPStatusCode']
    item = loc.get('Item')
    return json.dumps(item, cls=DecimalEncoder), status if item else 404


@location.route('/batch_save', methods=["POST"])
def batch_save_locations():
    validate_data(request.json, 'locations')
    Location.batch_save(request.json)

    return jsonify("Success")


@location.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        locs_json = json.load(file)
        validate_data(locs_json, "locations")
        Location.batch_save(locs_json)

        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp

    else:
        resp = jsonify({'message': 'Allowed file types are json, yml'})
        resp.status_code = 400
    return resp
