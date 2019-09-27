import os

from bravado_core.spec import Spec
from bravado_core.validate import validate_object
from flask import current_app as app
from yaml import load, Loader

bravado_config = {
    "validate_swagger_spec": False,
    "validate_requests": False,
    "validate_responses": False,
    "use_models": True,
}


def validate_data(data, validation_type):
    validate_object(*get_spec(validation_type), data)


def get_spec(def_name):
    spec_path = os.path.join(app.root_path, "swagger.yml")

    def _get_swagger_spec():
        with open(spec_path, "r") as spec:
            return load(spec.read(), Loader)

    spec_dict = _get_swagger_spec()
    spec = Spec.from_dict(spec_dict, config=bravado_config)
    return spec, spec_dict["definitions"].get(def_name)
