import tempfile
from pathlib import Path

import pytest

from piquid.jsonable import JSONAble


# define the test class
class Basic(JSONAble):

    def __init__(self, a: int, b: list[str], c: dict[str, list[float]]):
        self.a = a
        self.b = b
        self.c = c
        self.e = None

    @classmethod
    def get_test_instance(cls):
        return cls(a=1, b=['hello', 'there'], c={'I': [5.5, 6.6, 7.7], 'am': [1.1, 2.2, 3.3], 'a': [4.4, 5.5]})


# define fixtures
@pytest.fixture()
def test_instance() -> Basic:
    instance = Basic.get_test_instance()
    instance.e = ['a', 'b', 'c']
    return instance


@pytest.fixture()
def expected_dict():
    return Basic.get_test_instance().__dict__


# define tests
def test_roundtrip_file(test_instance, expected_dict):

    temp_file_path = Path(tempfile.mkdtemp()).joinpath('file.bson')
    test_instance.to_json_file(file_path=temp_file_path)
    instance_roundtrip = Basic.from_json_file(file_path=temp_file_path)

    assert expected_dict == instance_roundtrip.__dict__


def test_roundtrip_str(test_instance, expected_dict):

    instance_roundtrip = Basic.from_json_str(json_str=test_instance.to_json_str())

    assert expected_dict == instance_roundtrip.__dict__


def test_roundtrip_obj(test_instance, expected_dict):

    instance_roundtrip = Basic.from_json(json_obj=test_instance.to_json())

    assert expected_dict == instance_roundtrip.__dict__
