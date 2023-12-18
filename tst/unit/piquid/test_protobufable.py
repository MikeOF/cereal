import shutil
import tempfile
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


@pytest.fixture()
def test_instance() -> Basic:
    return Basic.get_test_instance()


@pytest.fixture()
def expected_dict():
    return Basic.get_test_instance().__dict__


def cleanup():
    protobuf_dir_path = Basic._get_protobuf_dir_path()
    if protobuf_dir_path.exists():
        shutil.rmtree(protobuf_dir_path)


def test_roundtrip_file(test_instance, expected_dict):
    cleanup()

    try:

        # round trip through the serialization process
        temp_file_path = Path(tempfile.mkdtemp()).joinpath('file.binpb')
        test_instance.to_protobuf_file(file_path=temp_file_path)
        roundtrip_instance = Basic.from_protobuf_file(file_path=temp_file_path)

        # check for equality
        assert roundtrip_instance.__dict__ == expected_dict

    finally:
        cleanup()


def test_roundtrip(test_instance, expected_dict):
    cleanup()

    try:

        # round trip through the serialization process
        roundtrip_instance = test_instance.from_protobuf(protobuf=test_instance.to_protobuf())

        # check for equality
        assert roundtrip_instance.__dict__ == expected_dict

    finally:
        cleanup()
