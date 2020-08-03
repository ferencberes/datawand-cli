Getting Started
===============

**datawand-cli** can help you managing your Python data science pipelines. Before plunging into coding let's get familiar with our pipeline concept.

Terminology
-----------

In our terminology, **Pipeline** is a collection a Python scripts, Jupyter notebooks and other resources that are related to the same experiment or data processing workflow. During pipeline execution (which is governed by `Luigi <https://github.com/spotify/luigi>`_) the dependency relations as well as the assigned parameters of the components are taken into account.

A given component (e.g. script, notebook) can be executed with different parameters in the same experiment. We refer to these duplicated components instances as **Clones** throughout the documentation.

Installation
------------

For now **datawand-cli** is only available from a GitHub repository.

.. code-block:: bash

   $ git clone https://github.com/ferencberes/datawand-cli.git
   $ cd datawand-cli
   $ pip install -U .

After installation you can access available API endpoints with the *datawand* bash command.

.. code-block:: bash

   $ datawand

Output:

.. code-block:: bash
   
   Welcome to datawand CLI. Happy coding! :)

   positional arguments:
     {status,list,init,drop,create,copy,view,delete,run,log,clear,kill,scheduler}
       status              Get information about your current folder
       list                List available datawand repositories
       init                Initialize new repository in your current folder
       drop                Disable repository by providing its name
       create              Create a new pipeline
       copy                Copy pipeline
       view                View pipeline (items)
       delete              Remove pipeline
       run                 Run experiment
       log                 View experiment logs
       clear               Clear experiment
       kill                Kill experiment processes
       scheduler           Interact with luigi scheduler

   optional arguments:
     -h, --help            show this help message and exit

Quick Start
-----------

To enable features for a given repository you must initialize **datawand-cli** with the following command:

.. code-block:: bash

   $ cd REPO_ROOT_DIR
   $ datawand init

After this step you can assess API endpoints in the subfolders as well. 


