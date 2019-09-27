import os

import boto3
from flasgger import Swagger
from flask import Flask, jsonify, redirect

from app.blueprints import path, location

app = Flask(__name__)
app.config['LOCAL'] = os.environ.get("FLASK_LOCAL")
app.register_blueprint(path)
app.register_blueprint(location)

swagger = Swagger(app, template_file="swagger.yml")

TABLE_NAME = 'robot_nav'



@app.route('/ping')
def test_route():
    return 'pong', 200


@app.route('/')
def main_route():
    return redirect('/apidocs', 302)


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
