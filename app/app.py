import boto3
from flask import Flask, json

app = Flask(__name__)

TABLE_NAME = 'robot_nav'


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


@app.route('/ping')
def test_route():
    return 'pong'


@app.route('/dynamo')
def dynamo_test_route():
    dynamo = boto3.client('dynamodb')
    payload = {"TableName": TABLE_NAME}
    return respond(dynamo.scan(payload))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
