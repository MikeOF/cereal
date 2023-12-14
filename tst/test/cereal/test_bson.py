import tempfile
from pathlib import Path

from cereal.bsonable import BSONAble


def test_roundtrip():

    # define the test class
    class Basic(BSONAble):

        def __init__(self, a: int, b: list[str], c: dict[str, list[float]]):
            self.a = a
            self.b = b
            self.c = c
            self.e = None

    # create the instance
    instance = Basic(a=1, b=['hello', 'there'], c={'I': [5.5, 6.6, 7.7], 'am': [1.1, 2.2, 3.3], 'a': [4.4, 5.5]})
    instance.e = ['a', 'b', 'c']

    # roundtrip the instance
    temp_file_path = Path(tempfile.mkdtemp()).joinpath('file.bson')
    instance.to_bson_file(file_path=temp_file_path)
    instance_roundtrip = Basic.from_bson_file(file_path=temp_file_path)

    # check
    expected_dict = instance.__dict__.copy()
    expected_dict['e'] = None
    assert expected_dict == instance_roundtrip.__dict__
