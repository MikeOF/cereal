import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from piquid.protobufable import ProtobufAble


class Basic(ProtobufAble):

    def __init__(self, a: str, b: float, c: int, d: list[str], e: set[int]):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    @classmethod
    def get_test_instance(cls):
        return cls(
            a='hello',
            b=5.5,
            c=-6,
            d=['you', 'are', 'a', 'test'],
            e={5, 6, 7}
        )

    @classmethod
    def cleanup(cls):
        protobuf_dir_path = cls._get_protobuf_dir_path()
        if protobuf_dir_path.exists():
            shutil.rmtree(protobuf_dir_path)


@pytest.fixture()
def test_instance() -> Basic:
    return Basic.get_test_instance()


@pytest.fixture()
def expected_dict():
    return Basic.get_test_instance().__dict__


def test_roundtrip_file(test_instance, expected_dict):
    Basic.cleanup()

    try:

        # round trip through the serialization process
        temp_file_path = Path(tempfile.mkdtemp()).joinpath('file.binpb')
        test_instance.to_protobuf_file(file_path=temp_file_path)
        roundtrip_instance = Basic.from_protobuf_file(file_path=temp_file_path)

        # check for equality
        assert roundtrip_instance.__dict__ == expected_dict

    finally:
        Basic.cleanup()


def test_roundtrip(test_instance, expected_dict):
    Basic.cleanup()

    try:

        # round trip through the serialization process
        roundtrip_instance = test_instance.from_protobuf(protobuf=test_instance.to_protobuf())

        # check for equality
        assert roundtrip_instance.__dict__ == expected_dict

    finally:
        Basic.cleanup()


@dataclass(frozen=True)
class BasicDataclass(ProtobufAble):
    a: str
    b: float
    c: int
    d: list[str]
    e: set[int]

    @classmethod
    def get_test_instance(cls):
        return cls(
            a='hello',
            b=5.5,
            c=-6,
            d=['you', 'are', 'a', 'test'],
            e={5, 6, 7}
        )

    @classmethod
    def cleanup(cls):
        protobuf_dir_path = cls._get_protobuf_dir_path()
        if protobuf_dir_path.exists():
            shutil.rmtree(protobuf_dir_path)


@pytest.fixture
def test_dataclass_instance():
    return BasicDataclass.get_test_instance()


def test_roundtrip_dataclass(test_dataclass_instance):
    BasicDataclass.cleanup()

    try:

        # round trip through the serialization process
        roundtrip_instance = BasicDataclass.from_protobuf(protobuf=test_dataclass_instance.to_protobuf())

        # check for equality
        assert roundtrip_instance == test_dataclass_instance

    finally:
        BasicDataclass.cleanup()
