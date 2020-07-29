Objects module
==============

datawand-cli handles experiment execution through pipelines which is the collection of multiple Python scripts or Jupyter notebooks. The Pipeline class has a simple interface to provide parameters and dependencies between pipeline components.


Pipeline components
-------------------

.. autoclass:: datawandcli.components.objects.ModuleObject
    :members:
    :undoc-members:

.. autoclass:: datawandcli.components.objects.NotebookObject
    :members:
    :undoc-members:

.. autoclass:: datawandcli.components.objects.PyScriptObject
    :members:
    :undoc-members:

.. autofunction:: datawandcli.components.objects.create_object

Pipeline class
--------------

.. autoclass:: datawandcli.components.objects.Pipeline
    :members:
    :undoc-members:

