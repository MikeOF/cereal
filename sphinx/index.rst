.. piquid documentation master file, created by
   sphinx-quickstart on Tue Dec 12 23:58:48 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to piquid's documentation
=================================

Piquid is a simple library that provides serialization functionality via a collection of base classes. It
supports JSON, BSON, Protobuf, and Pickle serialization. Each base class supports translations between objects in
memory or file paths, and each is meant to be compatible with dataclasses.

The implementations of these base classes are quite simple and somewhat limited. The intention is not to
present a library that can satisfy any use case. It is instead to present a pattern that can be used and improved upon
for simple "afterthought" style serialziation in Python. I would be reasonable to copy code from the source or overwrite
the inherited methods on a subclass.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference/modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
