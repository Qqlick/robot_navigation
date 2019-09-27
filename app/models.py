import decimal
import json

import boto3
from flask import current_app as app


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class Models:
    db_table_name = None
    pk = None

    @staticmethod
    def db():
        parameters = {
            'aws_access_key_id': "dev",
            'aws_secret_access_key': "dev",
            'region_name': "local",
            'endpoint_url': "http://localhost:4569",
        }
        parameters = parameters if app.config['LOCAL'] else {}
        dynamo_resource = boto3.resource('dynamodb', **parameters)
        return dynamo_resource

    @property
    def table(self):
        db = Models.db()
        return db.Table(self.db_table_name)

    def to_json(self):
        pass

    def get(self):
        r = self.table.get_item(Key={self.pk: getattr(self, self.pk)})
        return r

    def save(self):
        res = self.table.put_item(Item=self.to_json())
        return res


class Location(Models):
    db_table_name = 'locations'
    pk = 'name'

    def __init__(self, name=None, x=None, y=None):
        """
        :param name:
        :param x:
        :param y:
        """
        self.name = name
        self.x = x
        self.y = y

    def to_json(self):
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y
        }

    @classmethod
    def get_pk(cls):
        return cls.db_table_name
