from myjson.convertor import parse

import json


def test_dict():
    val = {"name": "Ramasubramanian", "age": 28, "salaried": True,
           "score": 4.6, "others": None }
    text = json.dumps(val)
    # print(text)
    ret = parse(text)
    assert type(ret) is dict
    assert len(ret) == 5
