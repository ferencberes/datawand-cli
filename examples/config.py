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

for exp_id in ["demo1","demo2"]:
    cg = ConfigGenerator(pipe_path, experiment_name=exp_id, experiment_dir="experiments/%s/" % exp_id)
    DEFAULTS = {}
    DEFAULTS["p1"] = 0.5
    DEFAULTS["p3"] = "default"
    PARAMETERS = {}
    for item in cg.pythonitem_names:
        PARAMETERS[item] = []
    PARAMETERS["sample"].append({"p1":1.0,"p2":0.5})
    PARAMETERS["sample"].append({"p1":0.0,"p2":1.0})
    if exp_id == "demo2":
        PARAMETERS["sample"].append({"p1":10.0,"p2":10.0})
        PARAMETERS["sample"].append({"p1":-10.0,"p2":-10.0})
    cg.save_params(DEFAULTS, PARAMETERS)
    #cg.pipeline.add_dependencies("sample_CLONE_2",["sample_CLONE_1"])
    #cg.generate_luigi_plan()
    cg.pipeline.save()