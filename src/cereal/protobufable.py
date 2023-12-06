import inspect
import subprocess
from abc import ABC
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import GenericAlias
from typing import Optional


class ProtoBufAble(ABC):
    """Base blass that provides protobuf serialization."""

    PROTOBUF_DIRNAME = '__protobuf__'
    PROTOFILE_SUFFIX = '.proto'
    OPTIONAL_TYPE_SET = frozenset((str, bool, int, float))
    REPEATED_TYPE_SET = frozenset((list, tuple, set))
    OPTIONAL_TYPE_BY_TYPE = {str: 'string', bool: 'bool', int: 'int32', float: 'double'}
    OPTIONAL_TYPE_BY_MEMBER: Optional[dict] = None
    REPEATED_TYPE_BY_MEMBER: Optional[dict] = None
    SOURCE_CLASS: Optional[type] = None

    @classmethod
    def get_protobuf_dir_path(cls) -> Path:
        """Get the directory where protobuf files will be stored."""
        return Path(inspect.getmodule(cls).__file__).parent.joinpath(cls.PROTOBUF_DIRNAME)

    @classmethod
    def get_proto_file_path(cls) -> Path:
        """Get the proto file path for this class."""
        return cls.get_protobuf_dir_path().joinpath(cls.__name__).with_suffix('.proto')

    @classmethod
    def get_source_file_path(cls) -> Path:
        """Get the proto file path for this class."""
        return cls.get_protobuf_dir_path().joinpath(f'{cls.__name__}_pb2.py')

    @classmethod
    def set_type_by_member_dicts(cls) -> None:

        type_by_member = {
            name: parameter.annotation
            for name, parameter in inspect.signature(cls.__init__).parameters.items()
            if name != 'self'
        }

        cls.OPTIONAL_TYPE_BY_MEMBER = {
            name: member_type for name, member_type in type_by_member.items()
            if member_type in cls.OPTIONAL_TYPE_BY_TYPE
        }

        cls.REPEATED_TYPE_BY_MEMBER = {
            name: member_type for name, member_type in type_by_member.items()
            if name not in cls.OPTIONAL_TYPE_BY_MEMBER
        }

    @classmethod
    def write_protofile(cls) -> None:
        """Write a proto file for this class."""

        cls.get_protobuf_dir_path().mkdir(exist_ok=True)

        with cls.get_proto_file_path().open(mode='w') as outf:

            # write the header
            print('syntax = "proto3";', file=outf)
            print('', file=outf)
            print(f'package {cls.__name__};', file=outf)
            print('', file=outf)

            # write the message
            print(f'message {cls.__name__} {{', file=outf)

            if cls.OPTIONAL_TYPE_BY_MEMBER is None or cls.REPEATED_TYPE_BY_MEMBER is None:
                cls.set_type_by_member_dicts()

            element_count = 0
            for member, repeated_type in cls.REPEATED_TYPE_BY_MEMBER.items():
                element_count += 1
                assert isinstance(repeated_type, GenericAlias)
                container_type = getattr(repeated_type, '__origin__')
                element_type = next(iter(getattr(repeated_type, '__args__')))
                assert container_type in cls.REPEATED_TYPE_SET
                assert element_type in cls.OPTIONAL_TYPE_SET
                print(f'\trepeated {cls.OPTIONAL_TYPE_BY_TYPE[element_type]} {member} = {element_count};', file=outf)
                print(f'', file=outf)

            for member, optional_type in cls.OPTIONAL_TYPE_BY_MEMBER.items():
                element_count += 1
                print(f'\toptional {cls.OPTIONAL_TYPE_BY_TYPE[optional_type]} {member} = {element_count};', file=outf)
                print(f'', file=outf)

            print('}', file=outf)

    @classmethod
    def compile(cls) -> None:

        cmd_tuple = [
            'protoc',
            f'-I={cls.get_protobuf_dir_path()}',
            f'--python_out={cls.get_protobuf_dir_path()}',
            f'{cls.get_proto_file_path()}'
        ]

        subprocess.run(cmd_tuple)

        assert cls.get_source_file_path().exists(), (
            f'could not find source path, {list(cls.get_protobuf_dir_path().glob("*"))}'
        )

    @classmethod
    def prepare_proto(cls) -> None:
        cls.write_protofile()
        cls.compile()

    @classmethod
    def import_source_class(cls) -> None:

        if cls.SOURCE_CLASS is None:

            # load the source module
            source_file_path = cls.get_source_file_path()
            loader = SourceFileLoader(fullname=source_file_path.stem, path=str(source_file_path))
            source_module = loader.load_module()

            # get the source class
            cls.SOURCE_CLASS = getattr(source_module, cls.__name__)

    def to_protobuf(self) -> str:

        if self.SOURCE_CLASS is None:
            self.import_source_class()

        instance = self.SOURCE_CLASS()
        for member in self.OPTIONAL_TYPE_BY_MEMBER:
            setattr(instance, member, getattr(self, member))

        for member in self.REPEATED_TYPE_BY_MEMBER:
            getattr(instance, member).extend(getattr(self, member))

        return instance.SerializeToString()
