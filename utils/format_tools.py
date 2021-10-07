import json
import random
import string


def transform_representation(ret):
    for key in ret:
        if ret[key] and (ret[key].__contains__('{')
                         or ret[key].__contains__('[')):
            ret[key] = json.loads(ret[key])
    return ret


def random_string(string_length=5):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, string_length))


def set_request_parameter_to_string(request, parameter: str):
    if parameter in request.data:
        request.data[parameter] = json.dumps(request.data[parameter])