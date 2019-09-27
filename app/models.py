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
            "aws_access_key_id": "dev",
            "aws_secret_access_key": "dev",
            "region_name": "local",
            "endpoint_url": "http://localhost:4569",
        }
        parameters = parameters if app.config["LOCAL"] else {}
        dynamo_resource = boto3.resource("dynamodb", **parameters)
        return dynamo_resource

    @classmethod
    def table(cls):
        db = Models.db()
        return db.Table(cls.db_table_name)

    @classmethod
    def batch_save(cls, data):
        table = cls.table()
        with table.batch_writer() as tbl:
            for r in data:
                tbl.put_item(r)

    def to_json(self):
        pass

    def get(self):
        r = self.table().get_item(Key={self.pk: getattr(self, self.pk)})
        return r

    def save(self):
        res = self.table().put_item(Item=self.to_json())
        return res


class Location(Models):
    db_table_name = "locations"
    pk = "name"

    def __init__(self, name=None, x=None, y=None):
        self.name = name
        self.x = x
        self.y = y

    def to_json(self):
        return {"name": self.name, "x": self.x, "y": self.y}


class Path(Models):
    db_table_name = "paths"
    pk = "path_dest"

    def __init__(
        self, path=None, start_x=None, start_y=None, finish_x=None, finish_y=None
    ):
        """
        :param path: List of instructions
        :param start_x:
        :param start_y:
        :param finish_x:
        :param finish_y:
        """
        self.start_x = start_x
        self.start_y = start_y
        self.finish_x = finish_x
        self.finish_y = finish_y
        self.path = path
        self.path_dest = f"{start_x}:{start_y}=>{finish_x}:{finish_y}"

    def to_json(self):
        return {
            "path_dest": self.path_dest,
            "path_info": {
                "start": [self.start_x, self.start_y],
                "finish": [self.finish_x, self.finish_y],
            },
            "path": self.path,
        }
