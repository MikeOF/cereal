import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent.joinpath('src')))

from cereal.protobufable import ProtoBufAble


class Simple(ProtoBufAble):

    def __init__(self, a: int, b: bool, c: list[float]):
        self.a = a
        self.b = b
        self.c = c
