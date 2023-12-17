import shutil
import subprocess
import tempfile
from pathlib import Path


class Handle:

    # get the project root
    ROOT_DIR_PATH = Path(__file__).absolute().parent.parent
    assert (
            ROOT_DIR_PATH.is_dir()
            and ROOT_DIR_PATH.name == 'piquid'
            and len({'src', 'sphinx', 'docs'}.difference(map(lambda x: x.name, ROOT_DIR_PATH.glob('*')))) == 0
    ), f'could not recognize the root dir path, {list(map(lambda x: x.name, ROOT_DIR_PATH.glob("*")))}'

    SRC_DIR_PATH = ROOT_DIR_PATH.joinpath('src')
    DOCS_DIR_PATH = ROOT_DIR_PATH.joinpath('docs')
    SPHINX_DIR_PATH = ROOT_DIR_PATH.joinpath('sphinx')


def main():
    prepare()
    clean()
    build()


def prepare():
    subprocess.run(
        tuple(
            map(
                str,
                (
                    'sphinx-apidoc', '-M', '-f',
                    '-o', Handle.SPHINX_DIR_PATH.joinpath('reference'),
                    '-e', Handle.SRC_DIR_PATH.joinpath('piquid')
                )
            )
        ),
        cwd=Handle.ROOT_DIR_PATH,
        check=True
    )


def clean():

    # remove everything in the docs directory
    for path in Handle.DOCS_DIR_PATH.glob('*'):

        if path.is_file():
            path.unlink()

        else:
            shutil.rmtree(path)


def build():
    tempdir = tempfile.mkdtemp()
    subprocess.run(
        tuple(map(str, ('sphinx-build', '-b', 'html', '-d', tempdir, Handle.SPHINX_DIR_PATH, Handle.DOCS_DIR_PATH))),
        cwd=Handle.ROOT_DIR_PATH,
        check=True
    )


if __name__ == '__main__':
    main()
