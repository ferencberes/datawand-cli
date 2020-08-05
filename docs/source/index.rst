.. datawand-cli documentation master file, created by
   sphinx-quickstart on Mon Jul 27 15:03:09 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to datawand-cli's documentation!
========================================

**datawand-cli** is a lightweight Python data science pipeline manager that is built on top of the `Luigi <https://github.com/spotify/luigi>`_ task scheduler package. Our solution provides in addition:

- Python API + bash CLI to interact with pipelines in a comfortable way
- common parameter loading interface for Jupyter Notebooks and Python scripts **(WIP)**
- parallel scheduling of Jupyter notebooks and Python scripts in the same environment (governed by `Luigi <https://github.com/spotify/luigi>`_) 
- experiment reproducibility

.. toctree::
   :maxdepth: 2
   :caption: CLI Documentation:

   getting_started
   toy_example
   cli_docs
 
.. toctree::
   :maxdepth: 1
   :caption: API Reference:
   
   api_comp_objects
   api_comp_params

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
