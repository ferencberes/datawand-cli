NOTEBOOK_SAMPLE = """
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Load parameters"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "import sys"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "from datawand.parametrization import ParamHelper"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "ph = ParamHelper('{{ rel_path }}', '{{ pipeline_name }}', sys.argv)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:py3]",
   "language": "python",
   "name": "conda-env-py3-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
"""

PY_SAMPLE = """
import sys
from datawand.parametrization import ParamHelper

ph = ParamHelper('{{ rel_path }}', '{{ pipeline_name }}', sys.argv)
"""

PARAMETER_SAMPLE = """
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "from datawand.parametrization import ConfigGenerator"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Initialize configuration generator"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "cg = ConfigGenerator(pipeline_name='{{ pipeline_name }}')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Setting default parameters for pipeline"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "DEFAULTS = {}"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Set your default parameters below:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Setting parameters for notebooks"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "PARAMETERS = {}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "for nb_name in cg.pythonitem_names:\n",
    "    PARAMETERS[nb_name] = []\n",
    "print(PARAMETERS)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Set your parameters for each notebooks below: \n",
    "\n",
    "##### You can specify the ending of the names of the generated notebook clones, if you add an \"\\_\\_ ending \\_\\_\" parameter. (Otherwise they will end with \\_CLONE\\_1, \\_CLONE\\_2, etc.)\n",
    "##### WARNING: if the name of the generated notebook clone is not an identifier, then luigi will NOT be able to run it."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Export parameters into pipeline configuration file"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "cg.save_params(PARAMETERS, DEFAULTS)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "cg.pipeline_cfg"
   ]
  }
 ],
 "metadata": {
  "anaconda-cloud": {},
  "kernelspec": {
   "display_name": "Python [conda env:dm-env]",
   "language": "python",
   "name": "conda-env-dm-env-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
"""