import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from piquid.jsonable import JSONAble


class Basic(JSONAble):

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

    temp_file_path = Path(tempfile.mkdtemp()).joinpath('file.json')
    test_instance.to_json_file(file_path=temp_file_path)
    roundtrip_instance = Basic.from_json_file(file_path=temp_file_path)

    assert roundtrip_instance.__dict__ == expected_dict


def test_roundtrip_str(test_instance, expected_dict):

    roundtrip_instance = Basic.from_json(json_str=test_instance.to_json())

    assert roundtrip_instance.__dict__ == expected_dict


def test_roundtrip(test_instance, expected_dict):

    roundtrip_instance = Basic.from_json_obj(json_obj=test_instance.to_json_obj())

    assert roundtrip_instance.__dict__ == expected_dict


def test_roundtrip_dataclass():

    @dataclass(frozen=True)
    class BasicDataclass(JSONAble):
        a: str
        b: float
        c: list[int]
        d: bool

    test_instance = BasicDataclass(a='hello', b=5.5, c=[4,5,6], d=False)

    roundtrip_instance = BasicDataclass.from_json(json_str=test_instance.to_json())

    assert roundtrip_instance == test_instance
