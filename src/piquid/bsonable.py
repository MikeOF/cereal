import inspect
from abc import ABCMeta
from pathlib import Path
from typing import Optional, Union

import bson


class BSONAble(metaclass=ABCMeta):
    """A base class providing BSON serialization functionality.

    This class includes an interface for BSON serialization that relies on the signature of the inheriting classes
    __init__ method. Any member included in that init method can be serialized by using the "to_json" methods of this
    class. During deserialization, parameters of the __init__ method are extracted from a BSON object and used to
    construct an instance.

    Notes & Caveats:

    * Currently only standard JSON/BSON types are supported.
    * Any instance state that is not part of the __init__ signature will not be serialized.

    """

    _CONSTRUCTOR_PARAMETER_SET: Optional[set[str]] = None

    @classmethod
    def _ensure_constructor_parameter_set(cls) -> None:

        if cls._CONSTRUCTOR_PARAMETER_SET is None:

            cls._CONSTRUCTOR_PARAMETER_SET = {
                name for name in inspect.signature(cls.__init__).parameters if name != 'self'
            }

    @classmethod
    def from_bson_file(cls, file_path: Union[Path, str]):
        with Path(file_path).open(mode='rb') as inf:
            return cls.from_bson(bson_bytes=inf.read())

    @classmethod
    def from_bson(cls, bson_bytes: bytes):

        instance_dict = bson.loads(data=bson_bytes)

        cls._ensure_constructor_parameter_set()
        construction_kwarg_by_name = {k: v for k, v in instance_dict.items() if k in cls._CONSTRUCTOR_PARAMETER_SET}

        return cls(**construction_kwarg_by_name)

    def to_bson_file(self, file_path: Union[Path, str]) -> None:
        with Path(file_path).open(mode='wb') as outf:
            outf.write(self.to_bson())

    def to_bson(self) -> bytes:
        self._ensure_constructor_parameter_set()
        return bson.dumps(obj={k: getattr(self, k) for k in self._CONSTRUCTOR_PARAMETER_SET})
