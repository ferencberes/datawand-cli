from datawandcli.components.objects import *
from datawandcli.parametrization import ConfigGenerator

pipe_path = "Trial.json"

pipe = Pipeline("Trial")
#pipe = Pipeline()
#pipe.load(pipe_path)
pys = PyScriptObject("sample","","examples/sample.py")
pipe.add(pys)
pipe.save()
print(pipe.config)

cg = ConfigGenerator(pipe_path, experiment_name="TrialDemo")
DEFAULTS = {}
DEFAULTS["p1"] = 0.5
DEFAULTS["p3"] = "default"

PARAMETERS = {}
for item in cg.pythonitem_names:
    PARAMETERS[item] = []

PARAMETERS["sample"].append({"p1":1.0,"p2":0.5})
PARAMETERS["sample"].append({"p1":0.0,"p2":1.0})

cg.save_params(DEFAULTS, PARAMETERS)
print(cg.pipeline_cfg)