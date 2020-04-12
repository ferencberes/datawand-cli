from jinja2 import Template
from .utils import *
import os

nb_str = """
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
    "import sys\n",
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
"""
def extract_base_dir(cursor, instance_name, instance_table):
    base_dir = get_instance_dir(cursor, instance_name, instance_table)
    num_pipelines, num_experiments = 0, 0
    if base_dir == None:
        print("Invalid instance name. Choose from the instances below:")
        show_table(cursor, instance_table)
    else:
        pipeline_dir = base_dir + "/datawand/pipelines"
        experiment_dir = base_dir + "/datawand/experiments"
        for new_dir in [pipeline_dir, experiment_dir]:
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
        num_pipelines = len(os.listdir(pipeline_dir))
        num_experiments = len(os.listdir(experiment_dir))
    return base_dir, num_pipelines, num_experiments

def create_pipeline(cursor, instance_table, instance_name, pipeline_name):
    base_dir, _, _ = extract_base_dir(cursor, instance_name, instance_table)
    print(base_dir)
    if base_dir != None:
        template = Template(nb_str)
        rendered = template.render(rel_path="./", pipeline_name=pipeline_name)
        with open("%s/datawand/pipelines/%s.ipynb" % (base_dir, pipeline_name), 'w') as f:
            f.write(rendered)
            
def remove_pipeline(cursor, instance_table, instance_name, pipeline_name):
    base_dir = extract_base_dir(cursor, instance_name, instance_table)
    if base_dir != None:
        pipeline_wout_extension = pipeline_name.replace(".ipynb","")
        f_name = "%s/%s.ipynb" % (base_dir, pipeline_wout_extension)
        if os.path.exists(f_name):
            os.remove(f_name)
        else:
            print("Invalid pipeline name! Choose from:")

def list_pipelines(cursor, instance_table, instance_name):
    base_dir, _, _ = extract_base_dir(cursor, instance_name, instance_table)
    if base_dir != None:
        print(os.listdir(base_dir+"/datawand/pipelines"))

def handle_pipeline_request(args, cursor, inst_name, instance_table):
    if inst_name == None:
        print("Provide an instance name!")
    else:
        if args.action in ["create","remove"]:
            pipeline_name = args.name
            if args.action == "create":
                create_pipeline(cursor, instance_table, inst_name, pipeline_name)
            else:
                remove_pipeline(cursor, instance_table, inst_name, pipeline_name)
        list_pipelines(cursor, instance_table, inst_name)
"""