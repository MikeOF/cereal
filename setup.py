from setuptools import setup, find_packages


setup(
    name='piquid',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=(
        'bson',
        'protobuf'
    )
)
