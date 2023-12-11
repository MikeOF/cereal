import shutil

from cereal.protobufable import ProtobufAble


def test_roundtrip_1():

    # define the class
    class Roundtrip1(ProtobufAble):

        def __init__(self, a: str, b: float, c: int, d: list[str], e: set[int]):
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.e = e

    # clear any existing serialization files
    if Roundtrip1._get_protobuf_dir_path().exists():
        shutil.rmtree(Roundtrip1._get_protobuf_dir_path())

    # create an instance
    instance_a = Roundtrip1(
        a='hello',
        b=5.5,
        c=-6,
        d=['you', 'are', 'a', 'test'],
        e={5, 6, 7}
    )

    # round trip through the serialization process
    instance_b = Roundtrip1.from_protobuf(protobuf=instance_a.to_protobuf())

    try:
        # check for equality
        assert instance_a.__dict__ == instance_b.__dict__

    finally:

        # cleanup
        if Roundtrip1._get_protobuf_dir_path().exists():
            shutil.rmtree(Roundtrip1._get_protobuf_dir_path())
