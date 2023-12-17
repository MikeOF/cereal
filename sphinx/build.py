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

    # get the api docs path
    DOCS_DIR_PATH = ROOT_DIR_PATH.joinpath('docs')


def main():
    prepare()
    clean()
    build()


def prepare():
    subprocess.run(
        ['sphinx-apidoc', '-o', 'sphinx/reference', '-e', 'src/piquid', '-M', '-f'],
        cwd=Handle.ROOT_DIR_PATH,
        check=True
    )


def build():
    tempdir = tempfile.mkdtemp()
    subprocess.run(
        ['sphinx-build', '-b', 'html', '-d', tempdir, 'sphinx', 'docs'],
        cwd=Handle.ROOT_DIR_PATH,
        check=True
    )
    Handle.DOCS_DIR_PATH.joinpath('.nojekyll').touch()


def clean():

    # remove everything in the docs directory
    for path in Handle.DOCS_DIR_PATH.glob('*'):

        if path.is_file():
            path.unlink()

        else:
            shutil.rmtree(path)


if __name__ == '__main__':
    main()
