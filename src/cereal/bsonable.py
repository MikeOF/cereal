from abc import ABCMeta

from cereal import JSONAble


class BSONAble(JSONAble, metaclass=ABCMeta):

    _SERIALIZATION_MODULE = None
