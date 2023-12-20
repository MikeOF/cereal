# piquid

A simple project that enables serialization of Python classes via a collection of base classes.

[Details in the docs](https://mikeof.github.io/piquid/)

## Installation

```
pip install "piquid @ git+https://github.com/MikeOF/piquid"
```

or perhaps

```
git clone git@github.com:MikeOF/piquid.git
cd piquid
pip install .
```

## Usage

To use piquid, create a subclass of one of its base classes.

```
from piquid.bsonable import BSONAble

class Example(BSONAble):

  def __init__(self, a: int, b: str):
     self.a = a
     self.b = b

example = Example(a=5, b='b')

bson_bytes = example.to_bson()

example_roundtrip = Example.from_bson(bson_bytes)
```
[Read more in the docs.](https://mikeof.github.io/piquid/)
