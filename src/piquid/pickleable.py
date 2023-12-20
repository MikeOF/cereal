import io
import pickle
from abc import ABCMeta
from pathlib import Path
from typing import Union


class PickleAble(metaclass=ABCMeta):
    """Base class providing pickle serialization convenience methods.

    This class provides convenience methods for pickle serialization. Serialization can either be to/from bytes or
    to/from a file path. It might seem odd to have a class like this since two lines of code is often enough to pickle a
    Python object. The motivation is to provide consitency rather that to encapsulate complexity. The consitency is
    gained through having a few methods calls which can only be written one way rather than allowing for creativity to
    occur during some pickling process. Creativity is bad. Another perhaps more convincing justification for this class
    is that is can prevent a lot of instances of "import pickle".
    """

    @classmethod
    def from_pickle_file(cls, file_path: Union[Path, str]):
        """Deserialize and instance from a file path.

        Parameters
        ----------
        file_path : Union[Path, str]
            a path to a file containing a pickled instance of the class.

        Returns
        -------
        __class__
            an instance of the class
        """
        with Path(file_path).open('rb') as inf:
            return cls.from_pickle(pickle_bytes=inf.read())

    @classmethod
    def from_pickle(cls, pickle_bytes: bytes):
        """Deserialize and instance from bytes.

        Parameters
        ----------
        pickle_bytes : bytes
            bytes containing a pickle serialized instance

        Returns
        -------
        __class__
            an instance of the class
        """
        instance = pickle.loads(pickle_bytes)
        assert isinstance(instance, cls), (
            f'loaded object is not of the expected type, {type(cls)}, {type(instance)}'
        )
        return instance

    def to_pickle_file(self, file_path: Union[Path, str]) -> None:
        """Serialized this instance and write it to a file.

        Parameters
        ----------
        file_path : Union[Path, str]
            the path to write the instance to

        Returns
        -------
        None
            nothing
        """
        with Path(file_path).open(mode='wb') as outf:
            outf.write(self.to_pickle())

    def to_pickle(self) -> bytes:
        """Serialized this instance and get the serialized for in bytes.

        Returns
        -------
        bytes
            bytes containing the pickle serialized form of this instance
        """
        bytes_io = io.BytesIO()
        pickle.dump(self, file=bytes_io)
        return bytes_io.getvalue()
