.. piquid documentation master file, created by
   sphinx-quickstart on Tue Dec 12 23:58:48 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to piquid's documentation
=================================

Piquid is a simple library that provides serialization functionality via a collection of base classes. It
supports JSON, BSON, Protobuf, and Pickle serialization. Each base class supports translations between objects in
memory or file paths, and each is meant to be compatible with dataclasses.

The implementations of these base classes are quite simple and somewhat limited. The library does not present a
suite of tools that can satisfy any use case. It instead presents a pattern that can be used and improved upon
for simple low-effort serialziation in Python. It would be reasonable to copy code from the source or overwrite
the inherited methods on a subclass. However, it might be unreasonable to expect perfection or even excellence.

The usage pattern for each base class is similar. For example, here is how the JSONAble base class is used:

.. code-block::

   class Example(JSONAble):

      def __init__(a: int, b: str):
         self.a = a
         self.b = b

   example = Example(a=5, b='b')

   json_str = example.to_json()

   example_roundtrip = Example.from_json(json_str)

`github repo`_

.. _github repo: https://github.com/MikeOF/piquid

Read through the reference below for more details.

.. toctree::
   :maxdepth: 2
   :caption: Reference:

   reference/modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
