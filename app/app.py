import os

import boto3
import flasgger
from flasgger import Swagger
from flask import Flask, jsonify, redirect, request, url_for

from app.blueprints import path, location

app = Flask(__name__)
app.config['LOCAL'] = os.environ.get("FLASK_LOCAL")
app.register_blueprint(path)
app.register_blueprint(location)

swagger = Swagger(app, template_file="swagger.yml")

TABLE_NAME = 'robot_nav'


@app.after_request
def after_request(response):
    origin = request.environ.pop('HTTP_ORIGIN', '*')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('X-Requested-With', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        response.headers.add('Content-Type', 'application/json')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
        return response
    return response


@app.route('/ping')
def test_route():
    return 'pong', 200


@app.route('/')
def main_route():
    return redirect(url_for('flasgger.apidocs'), 302)


@app.route('/dynamo')
def dynamo_test_route():
    parameters = {
        'aws_access_key_id': "dev",
        'aws_secret_access_key': "dev",
        'region_name': "local",
        'endpoint_url': "http://localhost:4569",
    }
    parameters = parameters if app.config['LOCAL'] else {}
    dynamo = boto3.client('dynamodb', **parameters)
    payload = {"TableName": TABLE_NAME}
    return jsonify(dynamo.scan(**payload))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
