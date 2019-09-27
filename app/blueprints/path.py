from flask import Blueprint, jsonify, request, json

from app.models import Path, DecimalEncoder
from app.utils import allowed_file
from app.validator import validate_data

path = Blueprint("path", __name__, url_prefix="/path")


@path.route("", methods=["POST"])
def save_location_to_db():
    validate_data(request.json, "path")
    save_result = Path(**request.json).save()
    return jsonify(save_result)


@path.route("/<path_dest>")
def get_path(path_dest):
    path = Path(path_dest=path_dest).get()
    status = path["ResponseMetadata"]["HTTPStatusCode"]
    item = path.get("Item")
    return json.dumps(item, cls=DecimalEncoder), status if item else 404


@path.route("/batch_save", methods=["POST"])
def batch_save_paths():
    validate_data(request.json, "paths")
    Path.batch_save(request.json)
    return jsonify("Success")


@path.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        resp = jsonify({"message": "No file part in the request"})
        resp.status_code = 400
        return resp
    file = request.files["file"]
    if file.filename == "":
        resp = jsonify({"message": "No file selected for uploading"})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        locs_json = json.load(file)
        validate_data(locs_json, "paths")
        Path.batch_save(locs_json)

        resp = jsonify({"message": "File successfully uploaded"})
        resp.status_code = 201
        return resp

    else:
        resp = jsonify({"message": "Allowed file types are json, yml"})
        resp.status_code = 400
    return resp
