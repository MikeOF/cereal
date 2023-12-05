from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.joinpath('tester')))

from tester.simple import Simple


def main():

    # write the protofile
    Simple.write_protofile()
    Simple.compile()

    # create an instance of the class
    simple = Simple(a=5, b=True, c=[5.5, 6.6, 7.7])


if __name__ == '__main__':
    main()
