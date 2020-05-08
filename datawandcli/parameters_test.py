from datawandcli.components.objects import *
from datawandcli.parametrization import ConfigGenerator
from shutil import rmtree

def test_create_pipeline():
    pipe = Pipeline("Trial")
    pys = PyScriptObject("sample","","examples/sample.py")
    pipe.add(pys)
    pipe.save()
    print(pipe.config)
    assert len(pipe.parts)==1
    
def test_demo_1_init():
    cg = ConfigGenerator("Trial.json", experiment_name="demo_1", experiment_dir="experiments/demo_1/")
    DEFAULTS = {}
    DEFAULTS["p1"] = 0.5
    DEFAULTS["p3"] = "default"
    PARAMETERS = {}
    for item in cg.pythonitem_names:
        PARAMETERS[item] = []
    PARAMETERS["sample"].append({"p1":1.0,"p2":0.5})
    PARAMETERS["sample"].append({"p1":0.0,"p2":1.0})
    cg.save_params(DEFAULTS, PARAMETERS)
    cg.pipeline.save()
    assert len(cg.pipeline.parts) == 3
    assert cg.pipeline.num_clones["sample"] == 2
    
def test_demo_1_params():
    pipe = Pipeline()
    pipe.load("experiments/demo_1/Trial.json")
    assert pipe.default_config["p1"] == 0.5
    assert pipe.default_config["p3"] == "default"
    assert pipe.parts["sample_CLONE_1"].config["p1"] == 1.0
    assert pipe.parts["sample_CLONE_2"].config["p1"] == 0.0
    assert pipe.parts["sample_CLONE_1"].config["p2"] == 0.5
    assert pipe.parts["sample_CLONE_2"].config["p2"] == 1.0
    
def test_demo_2_init():
    cg = ConfigGenerator("Trial.json", experiment_name="demo_2", experiment_dir="experiments/demo_2/")
    DEFAULTS = {}
    DEFAULTS["p1"] = 0.5
    DEFAULTS["p3"] = "default"
    PARAMETERS = {}
    for item in cg.pythonitem_names:
        PARAMETERS[item] = []
    PARAMETERS["sample"].append({"p1":1.0,"p2":0.5})
    PARAMETERS["sample"].append({"p1":0.0,"p2":1.0})
    PARAMETERS["sample"].append({"p1":10.0,"p2":-10.0})
    PARAMETERS["sample"].append({"p1":-10.0,"p2":10.0})
    cg.save_params(DEFAULTS, PARAMETERS)
    cg.pipeline.save()
    assert len(cg.pipeline.parts) == 5
    assert cg.pipeline.num_clones["sample"] == 4
    
def test_demo_2_params():
    pipe = Pipeline()
    pipe.load("experiments/demo_2/Trial.json")
    assert pipe.default_config["p1"] == 0.5
    assert pipe.default_config["p3"] == "default"
    assert pipe.parts["sample_CLONE_1"].config["p1"] == 1.0
    assert pipe.parts["sample_CLONE_2"].config["p1"] == 0.0
    assert pipe.parts["sample_CLONE_1"].config["p2"] == 0.5
    assert pipe.parts["sample_CLONE_2"].config["p2"] == 1.0
    assert pipe.parts["sample_CLONE_3"].config["p1"] == 10.0
    assert pipe.parts["sample_CLONE_4"].config["p1"] == -10.0
    assert pipe.parts["sample_CLONE_3"].config["p2"] == -10.0
    assert pipe.parts["sample_CLONE_4"].config["p2"] == 10.0
    rmtree("experiments/")