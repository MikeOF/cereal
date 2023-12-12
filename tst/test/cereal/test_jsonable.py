from cereal.jsonable import JSONAble


def test_roundtrip():

    # define the test class
    class Basic(JSONAble):

        def __init__(self, a: int, b: list[str], c: dict[str, list[float]]):
            self.a = a
            self.b = b
            self.c = c
            self.e = None

    # create the instance
    instance = Basic(a=1, b=['hello', 'there'], c={'I': [5.5, 6.6, 7.7], 'am': [1.1, 2.2, 3.3], 'a': [4.4, 5.5]})
    instance.e = ['a', 'b', 'c']

    # roundtrip the instance
    instance_roundtrip = Basic.from_json_str(json_str=instance.to_json_str())

    # check
    assert instance.__dict__ == instance_roundtrip.__dict__
