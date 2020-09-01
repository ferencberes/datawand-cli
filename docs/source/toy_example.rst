Toy example
===========

In this toy example we create a pipeline **(GraphDemo)** that will calculate the correlation matrix for four centrality measures (degree, pagerank, closeness, betweenness) on the `Karate Club graph <https://networkx.github.io/documentation/stable/auto_examples/graph/plot_karate_club.html>`_.

Demo code
---------

**TODO: load demo code**

The pipeline have three (pre-prepaired) files:

   - **scripts/centrality.py** : calculates node centrality then export it to a csv file
   - **scripts/correlation.py** : calculates correlation matrix for the given centrality scores
   - **init_experiment.py** : initialize the experiment with parameters (e.g. centrality measure, correlation type)

Follow the steps below:

Initialize repository
---------------------

To enable **datawand-cli** features for a given repository you must initialize it with the following command:

.. code-block:: bash

   $ cd $DEMO_DIR
   $ datawand init --name Demo

After this step you can assess API endpoints in the subfolders as well.

You can also easily keep track of the repositories that you use with **datawand-cli**:

.. code-block:: bash

   $ datawand list

Output:

.. code-block:: bash

      name       path           created_at
   0  Demo  $DEMO_DIR  2020-08-05 10:47:13

Create pipeline with components
-------------------------------

.. code-block:: bash

   $ datawand create GraphDemo
   $ datawand add GraphDemo.json scripts/centrality.py
   $ datawand add GraphDemo.json scripts/correlation.py
   $ datawand view GraphDemo.json

Output:

.. code-block:: bash

   Name: GraphDemo
   Namespace: GraphDemo
   Python scripts: ['centrality', 'correlation']

Do not forget to add a dependency relation between the two script components as node centrality scores are needed to calculate their correlation.

.. code-block:: bash

   $ datawand dependency add GraphDemo.json correlation centrality
   $ datawand view GraphDemo.json --name correlation

Output:

.. code-block:: bash

   Name: correlation
   Type: pyscript
   Path: scripts/correlation.py
   Dependencies: ['centrality']
   No parameters were set.

Initialize experiment
---------------------

Set parameters for pipeline components.

.. code-block:: bash

   $ python init_experiment.py

Now it is worth to have a look at the repository status. It shows that you have a single pipeline (GraphDemo) and one experiment that hasn't been executed yet (last line).

.. code-block:: bash

   $ datawand status

Output:

.. code-block:: bash

   ### General information ###
   Name: Demo
   Base folder: /home/fberes/projects/demo_dir
   Number of pipelines: 1
   Number of experiments: 1
   ### Pipelines ###
   /home/fberes/projects/demo_dir/GraphDemo.json
   ### Experiments with status ###
   /home/fberes/projects/demo_dir/experiments/demo/GraphDemo.json N/A 0%

If you have a look at the experiment configuration file then you will see several clones that each have different parameters.

.. code-block:: bash

   $ datawand view experiments/demo/GraphDemo.json

Output:

.. code-block:: bash

   Name: GraphDemo
   Namespace: demo
   Base directory: experiments/demo/
   Parameters:
   {'metrics': ['degree', 'pagerank', 'closeness', 'betweenness']}
   Python scripts: ['centrality_CLONE_1', 'centrality_CLONE_2', 'centrality_CLONE_3', 'centrality_CLONE_4', 'correlation_CLONE_1', 'correlation_CLONE_2']

The custom parameters of the clones can also be observed easily:

.. code-block:: bash

   $ datawand view experiments/demo/GraphDemo.json --name correlation_CLONE_2

Output:

.. code-block:: bash

   Name: correlation_CLONE_2
   Type: pyscript
   Path: scripts/correlation_CLONE_2.py
   Dependencies: ['centrality_CLONE_1', 'centrality_CLONE_2', 'centrality_CLONE_3', 'centrality_CLONE_4']
   Parameters:
   {'metrics': ['degree', 'pagerank', 'closeness', 'betweenness'], 'corr_type': 'pearson'}

Running the experiment
----------------------

First you must start the luigi scheduler in order to execute your experiment

.. code-block:: bash

   $ datawand scheduler start

With the following command you can query the luigi scheduler status along with its port

.. code-block:: bash

   $ datawand scheduler status


Then provide the path for the experiment configuration file. You can also specify the maximum number of threads to use for parallel execution.


.. code-block:: bash

   $ datawand run experiments/demo/GraphDemo.json --workers 2

During runtime you can monitor the status of your experiments.

.. code-block:: bash

   $ datawand status

Output:

.. code-block:: bash

   ### General information ###
   Name: Demo
   Base folder: /home/fberes/projects/demo_dir
   Number of pipelines: 1
   Number of experiments: 1
   ### Pipelines ###
   /home/fberes/projects/demo_dir/GraphDemo.json
   ### Experiments with status ###
   /home/fberes/projects/demo_dir/experiments/demo/GraphDemo.json SUCCESS 100%

Observe results
---------------

You can access pipeline component log files with the command below. These files contain the correlation matrices in our case.

.. code-block:: bash

   $ datawand log experiments/demo/GraphDemo.json --name correlation_CLONE_2 --tail 5

Output: (Spearman's Rho correlation of different centrality metrics for the Karate Club graph)

.. code-block:: bash

                  degree  pagerank  closeness  betweenness
   degree       1.000000  0.978925   0.894507     0.905013
   pagerank     0.978925  1.000000   0.824780     0.879444
   closeness    0.894507  0.824780   1.000000     0.898087
   betweenness  0.905013  0.879444   0.898087     1.000000


Postprocessing
--------------

Finally, if you have finished running your experiments then you should stop the scheduler

.. code-block:: bash

   $ datawand scheduler stop
s
