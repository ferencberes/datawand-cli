from datawandcli.parametrization import ConfigGenerator
import random

cg = ConfigGenerator("Trial.json", experiment_name="demo_1", experiment_dir="experiments/demo_1/")
DEFAULTS = {}
DEFAULTS["p1"] = 0.5
DEFAULTS["p3"] = "default"
DEFAULTS["sleep"] = 0

PARAMETERS = {}
for item in cg.pythonitem_names:
    PARAMETERS[item] = []

PARAMETERS["PySample"].append({"p1":1.0,"p2":0.5,"sleep":random.random()*60})
PARAMETERS["PySample"].append({"p1":5.0,"p2":0.1,"sleep":random.random()*60})
#PARAMETERS["PySample"].append({"p1":10.0,"p2":0.1,"sleep":random.random()*120})
PARAMETERS["PySample"].append({"p1":0.0,"p2":1.0,"sleep":random.random()*60})
cg.save_params(DEFAULTS, PARAMETERS)
cg.pipeline.save()
