import shutil
from pathlib import Path


def clean():

    # get the docs path
    docs_dir_path = Path(__file__).absolute().parent.parent.joinpath('docs')
    assert docs_dir_path.is_dir() and docs_dir_path.parent.name == 'cereal', (
        f'could not determine docs path, {docs_dir_path}'
    )

    # remove everything in the docs directory
    for path in docs_dir_path.glob('*'):

        if path.is_file():
            path.unlink()

        else:
            shutil.rmtree(path)


if __name__ == '__main__':
    clean()
