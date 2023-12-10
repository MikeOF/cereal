import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath('tester')))

from tester.simple import Simple


def main():

    # write the protofile
    Simple._write_protofile()
    Simple._compile()

    # create an instance of the class
    simple = Simple(a=5, b=True, c=[5.5, 6.6, 7.7])
    protobuf_str = simple.to_protobuf()
    print(simple.__dict__)
    print(type(protobuf_str))
    print(protobuf_str)
    simple_from = Simple.from_protobuf(protobuf=protobuf_str)
    print(simple_from.__dict__)


if __name__ == '__main__':
    main()
