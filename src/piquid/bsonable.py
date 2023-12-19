"""BSON serialization"""
import inspect
from abc import ABCMeta
from pathlib import Path
from typing import Optional, Union

import bson


class BSONAble(metaclass=ABCMeta):
    """A base class providing BSON serialization functionality.

    This class includes an interface for BSON serialization that relies on the signature of the inheriting classes
    __init__ method. During serialization the parameters of the __init__ method are collected from the class to be
    serialized, and during deserialization the parameters of the __init__ method are used to create keyword arguments
    to the __init__ method. The means that any class members which need to be included in serialzied instances of the
    class must be included as paramters to the __init__ signature.

    Notes & Caveats:

    * Currently only standard JSON/BSON types are supported.
    * Any instance state that is not part of the __init__ signature will not be serialized.

    """

    _CONSTRUCTOR_PARAMETER_SET: Optional[set[str]] = None

    @classmethod
    def _ensure_constructor_parameter_set(cls) -> None:
        """Ensure that the constructor parameter set is set for this JSONAble class."""

        if cls._CONSTRUCTOR_PARAMETER_SET is None:

            cls._CONSTRUCTOR_PARAMETER_SET = {
                name for name in inspect.signature(cls.__init__).parameters if name != 'self'
            }

    @classmethod
    def from_bson_file(cls, file_path: Union[Path, str]):
        """Deserialize an instance from a file path.

        Parameters
        ----------
        file_path : Path | str
            the file path to deserialize the instance from

        Returns
        -------
        __class__
            the instance of the class
        """

        with Path(file_path).open(mode='rb') as inf:
            return cls.from_bson(bson_bytes=inf.read())

    @classmethod
    def from_bson(cls, bson_bytes: bytes):
        """Deserialize an instance from BSON bytes.

        Parameters
        ----------
        bson_bytes : bytes
            bytes to deserialize the instance from

        Returns
        -------
        __class__
            the instance of the class
        """

        instance_dict = bson.loads(data=bson_bytes)

        cls._ensure_constructor_parameter_set()
        construction_kwarg_by_name = {k: v for k, v in instance_dict.items() if k in cls._CONSTRUCTOR_PARAMETER_SET}

        return cls(**construction_kwarg_by_name)

    def to_bson_file(self, file_path: Union[Path, str]) -> None:
        """Serialize the instance and write to a file path.

        Parameters
        ----------
        file_path : Union[Path, str]
            the file path to write to

        Returns
        -------
        None
            nothing
        """

        with Path(file_path).open(mode='wb') as outf:
            outf.write(self.to_bson())

    def to_bson(self) -> bytes:
        """Serialize the instance to BSON bytes.

        Returns
        -------
        bytes
            the instance as BSON bytes
        """

        self._ensure_constructor_parameter_set()
        return bson.dumps(obj={k: getattr(self, k) for k in self._CONSTRUCTOR_PARAMETER_SET})
