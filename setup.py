from setuptools import setup, find_packages

extra_requirement_list_by_name = {
    'protobuf': ['protobuf'],
    'bson': ['bson']
}

setup(
    name='cereal',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    extras_require=extra_requirement_list_by_name
)
