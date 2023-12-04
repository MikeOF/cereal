import inspect
from abc import ABC
from pathlib import Path
from types import GenericAlias


class ProtoBufAble(ABC):
    """Base blass that provides protobuf serialization."""

    PROTOBUF_DIRNAME = '__proto__'
    PROTOFILE_SUFFIX = '.proto'
    OPTIONAL_TYPE_SET = frozenset((str, bool, int, float))
    REPEATED_TYPE_SET = frozenset((list, tuple, set))
    OPTIONAL_TYPE_BY_TYPE = {str: 'string', bool: 'bool', int: 'int32', float: 'double'}

    @classmethod
    def get_protobuf_dir_path(cls) -> Path:
        """Get the directory where protobuf files will be stored."""
        return Path(inspect.getmodule(cls).__file__).parent.joinpath(cls.PROTOBUF_DIRNAME)

    @classmethod
    def get_proto_file_path(cls) -> Path:
        """Get the proto file path for this class."""
        return cls.get_protobuf_dir_path().joinpath(cls.__name__).with_suffix('.proto')

    @classmethod
    def write_protofile(cls) -> None:
        """Write a proto file for this class."""

        with cls.get_proto_file_path().open(mode='w') as outf:

            # write the header
            print('syntax = "proto3";', file=outf)
            print('', file=outf)
            print(f'package {cls.__name__};', file=outf)
            print('', file=outf)

            # write the message
            print(f'message {cls.__name__} {{', file=outf)

            signature = inspect.signature(cls.__init__)

            member_to_type = {
                name: parameter.annotation for name, parameter in signature.parameters.items()
                if name != 'self'
            }

            optional_type_by_member = {
                name: member_type for name, member_type in member_to_type.items()
                if member_type in cls.OPTIONAL_TYPE_BY_TYPE
            }

            repeated_type_by_member = {
                name: member_type for name, member_type in member_to_type.items()
                if name not in optional_type_by_member
            }

            element_count = 0
            for member, repeated_type in repeated_type_by_member:
                element_count += 1
                assert isinstance(repeated_type, GenericAlias)
                container_type = getattr(repeated_type, '__origin__')
                element_type = next(iter(getattr(repeated_type, '__args__')))
                assert container_type in cls.REPEATED_TYPE_SET
                assert element_type in cls.OPTIONAL_TYPE_SET
                print(f'repeated {cls.OPTIONAL_TYPE_BY_TYPE[element_type]} {member} = {element_count};', file=outf)
                print(f'', file=outf)

            for member, optional_type in optional_type_by_member:
                element_count += 1
                print(f'optional {cls.OPTIONAL_TYPE_BY_TYPE[optional_type]} {member} = {element_count};', file=outf)
                print(f'', file=outf)

            print('}', file=outf)
