from abc import ABCMeta

import bson

from cereal.jsonable import JSONAble


class BSONAble(JSONAble, metaclass=ABCMeta):

    _SERIALIZATION_MODULE = bson
