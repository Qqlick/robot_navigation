import os

import boto3
from flask import Flask, jsonify

app = Flask(__name__)
app.config['LOCAL'] = os.environ.get("FLASK_LOCAL")

TABLE_NAME = 'robot_nav'


@app.route('/ping')
def test_route():
    return 'pong'


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
