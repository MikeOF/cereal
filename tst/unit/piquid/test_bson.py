import tempfile
from pathlib import Path

import pytest

from piquid.bsonable import BSONAble


class Basic(BSONAble):

    def __init__(self, a: int, b: list[str], c: dict[str, list[float]]):
        self.a = a
        self.b = b
        self.c = c
        self.e = None

    @classmethod
    def get_test_instance(cls):
        return cls(a=1, b=['hello', 'there'], c={'I': [5.5, 6.6, 7.7], 'am': [1.1, 2.2, 3.3], 'a': [4.4, 5.5]})


@pytest.fixture()
def test_instance() -> Basic:
    instance = Basic.get_test_instance()
    instance.e = ['a', 'b', 'c']
    return instance


@pytest.fixture()
def expected_dict():
    return Basic.get_test_instance().__dict__


def test_roundtrip_file(test_instance, expected_dict):

    # roundtrip the instance
    temp_file_path = Path(tempfile.mkdtemp()).joinpath('file.bson')
    test_instance.to_bson_file(file_path=temp_file_path)
    roundtrip_instance = Basic.from_bson_file(file_path=temp_file_path)

    # check
    assert expected_dict == roundtrip_instance.__dict__


def test_roundtrip(test_instance, expected_dict):

    # roundtrip the instance
    roundtrip_instance = Basic.from_bson(bson_bytes=test_instance.to_bson())

    # check
    assert expected_dict == roundtrip_instance.__dict__
