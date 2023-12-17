import io
import pickle
from abc import ABCMeta
from pathlib import Path
from typing import Union


class PickleAble(metaclass=ABCMeta):
    """Base class providing pickle serialization convenience methods.

    This class provides convenience methods for pickle serialization. Serialization can either be to/from bytes or
    to/from a file path.
    """

    @classmethod
    def from_pickle_bytes(cls, obj_bytes: bytes):
        """Deserialize and instance from bytes.

        Parameters
        ----------
        obj_bytes : bytes
            bytes containing a pickle serialized instance

        Returns
        -------
            an instance of the class

        """
        instance = pickle.loads(obj_bytes)
        assert isinstance(instance, cls), (
            f'loaded object is not of the expected type, {type(cls)}, {type(instance)}'
        )
        return instance

    @classmethod
    def from_pickle_file(cls, file_path: Union[Path, str]):
        """Deserialize and instance from a file path.

        Parameters
        ----------
        file_path : Path | str
            a path to a file containing a pickled instance of the class.

        Returns
        -------
            an instance of the class

        """
        with Path(file_path).open('rb') as inf:
            return cls.from_pickle_bytes(obj_bytes=inf.read())

    def to_pickle_bytes(self) -> bytes:
        """Serialized this instance and get the serialized for in bytes.

        Returns
        -------
            bytes containing the pickle serialized form of this instance

        """
        bytes_io = io.BytesIO()
        pickle.dump(self, file=bytes_io)
        return bytes_io.getvalue()

    def to_pickle_file(self, file_path: Union[Path, str]) -> None:
        """Serialized this instance and write it to a file.

        Parameters
        ----------
        file_path : Path | str
            the path to write the instance to

        Returns
        -------
            Nothing

        """
        with Path(file_path).open(mode='wb') as outf:
            outf.write(self.to_pickle_bytes())
