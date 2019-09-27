from flask import Blueprint, jsonify

path = Blueprint('path', __name__, url_prefix='/path')


@path.route('/', methods=["POST"])
def save_path_to_db():
    return jsonify("Success", 200)
