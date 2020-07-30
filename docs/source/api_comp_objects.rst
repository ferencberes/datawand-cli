Objects module
==============

datawand-cli handles experiment execution through pipelines which is the collection of multiple Python scripts or Jupyter notebooks. The Pipeline class has a simple interface to provide parameters and dependencies between pipeline components.


Pipeline components
-------------------

.. autoclass:: datawandcli.components.objects.Base

.. autoclass:: datawandcli.components.objects.Configurable
    :show-inheritance:

.. autoclass:: datawandcli.components.objects.Module
    :show-inheritance:

.. autoclass:: datawandcli.components.objects.Notebook
    :show-inheritance:    

.. autoclass:: datawandcli.components.objects.PyScript
    :show-inheritance:

.. autofunction:: datawandcli.components.objects.create_object

Pipeline class
--------------

.. autoclass:: datawandcli.components.objects.Pipeline
    :members: save, load, add, remove, add_dependencies, remove_dependencies, add_clone, clear
    :undoc-members:

