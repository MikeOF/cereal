from setuptools import setup, find_packages

setup(
    name='cereal',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    requires=['protobuf']
)
