import shutil

from cereal.protobufable import ProtobufAble


def test_roundtrip():

    # define the class
    class Roundtrip(ProtobufAble):

        def __init__(self, a: str, b: float, c: int, d: list[str], e: set[int]):
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.e = e

    # clear any existing serialization files
    protobuf_dir_path = Roundtrip._get_protobuf_dir_path()
    if protobuf_dir_path.exists():
        shutil.rmtree(protobuf_dir_path)

    # create an instance
    instance_a = Roundtrip(
        a='hello',
        b=5.5,
        c=-6,
        d=['you', 'are', 'a', 'test'],
        e={5, 6, 7}
    )

    # round trip through the serialization process
    instance_b = Roundtrip.from_protobuf(protobuf=instance_a.to_protobuf())

    try:
        # check for equality
        assert instance_a.__dict__ == instance_b.__dict__

    finally:

        # cleanup
        if protobuf_dir_path.exists():
            shutil.rmtree(protobuf_dir_path)
