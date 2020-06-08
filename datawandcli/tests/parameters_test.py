from datawandcli.components.objects import *
from datawandcli.parametrization import ConfigGenerator
from shutil import rmtree
import subprocess, os

def load_last_line(fp):
    last_line = ""
    with open(fp) as f:
        for line in f:
            last_line = line.rstrip()
    return last_line

def test_create_pipeline():
    pipe = Pipeline("Trial")
    mod = ModuleObject("my_module","","examples/my_module.py")
    pys = PyScriptObject("PySample","","examples/sample.py")
    pipe.add(mod)
    pipe.add(pys)
    pipe.save()
    print(pipe.config)
    assert len(pipe.parts)==2
    
def test_demo_1_init():
    cg = ConfigGenerator("Trial.json", experiment_name="demo_1", experiment_dir="experiments/demo_1/")
    DEFAULTS = {}
    DEFAULTS["p1"] = 0.5
    DEFAULTS["p3"] = "default"
    DEFAULTS["sleep"] = 0
    PARAMETERS = {}
    for item in cg.pythonitem_names:
        PARAMETERS[item] = []
    PARAMETERS["PySample"].append({"p1":1.0,"p2":0.5})
    PARAMETERS["PySample"].append({"p1":0.0,"p2":1.0})
    cg.save_params(DEFAULTS, PARAMETERS, local_scheduler=True)
    cg.pipeline.save()
    assert len(cg.pipeline.parts) == 3
    assert cg.pipeline.num_clones["PySample"] == 2

def test_demo_1_params():
    pipe = Pipeline()
    pipe.load("experiments/demo_1/Trial.json")
    assert pipe.default_config["p1"] == 0.5
    assert pipe.default_config["p3"] == "default"
    assert pipe.parts["PySample_CLONE_1"].config["p1"] == 1.0
    assert pipe.parts["PySample_CLONE_2"].config["p1"] == 0.0
    assert pipe.parts["PySample_CLONE_1"].config["p2"] == 0.5
    assert pipe.parts["PySample_CLONE_2"].config["p2"] == 1.0

def test_demo_1_run():
    fp = "experiments/demo_1/demo_1.log"
    p = subprocess.Popen("bash demo_1.sh 1", cwd="experiments/demo_1/", stdout=open(fp, "w"), shell=True)
    p_status = p.wait()
    with open(fp) as f:
        output = f.read()
    print(output)
    assert "PySample_CLONE_1 task was executed!" in output
    assert "PySample_CLONE_2 task was executed!" in output

def test_demo_1_output():
    out_1 = load_last_line("experiments/demo_1/examples/PySample_CLONE_1.log")
    out_2 = load_last_line("experiments/demo_1/examples/PySample_CLONE_2.log")
    rmtree("experiments/demo_1/")
    assert out_1 == "1.0 0.5 default"
    assert out_2 == "0.0 1.0 default"
    
def test_demo_2_init():
    cg = ConfigGenerator("Trial.json", experiment_name="demo_2", experiment_dir="experiments/demo_2/")
    DEFAULTS = {}
    DEFAULTS["p1"] = 0.1
    DEFAULTS["p3"] = "default"
    DEFAULTS["sleep"] = 0
    PARAMETERS = {}
    for item in cg.pythonitem_names:
        PARAMETERS[item] = []
    PARAMETERS["PySample"].append({"p2":0.5})
    PARAMETERS["PySample"].append({"p2":1.0})
    PARAMETERS["PySample"].append({"p1":10.0,"p2":-10.0})
    PARAMETERS["PySample"].append({"p1":-10.0,"p2":10.0})
    cg.save_params(DEFAULTS, PARAMETERS, local_scheduler=True)
    cg.pipeline.save()
    assert len(cg.pipeline.parts) == 5
    assert cg.pipeline.num_clones["PySample"] == 4
    
def test_demo_2_params():
    pipe = Pipeline()
    pipe.load("experiments/demo_2/Trial.json")
    assert pipe.default_config["p1"] == 0.1
    assert pipe.default_config["p3"] == "default"
    assert "p1" not in pipe.parts["PySample_CLONE_1"].config
    assert "p1" not in pipe.parts["PySample_CLONE_2"].config
    assert pipe.parts["PySample_CLONE_1"].config["p2"] == 0.5
    assert pipe.parts["PySample_CLONE_2"].config["p2"] == 1.0
    assert pipe.parts["PySample_CLONE_3"].config["p1"] == 10.0
    assert pipe.parts["PySample_CLONE_4"].config["p1"] == -10.0
    assert pipe.parts["PySample_CLONE_3"].config["p2"] == -10.0
    assert pipe.parts["PySample_CLONE_4"].config["p2"] == 10.0

def test_demo_2_run():
    fp = "experiments/demo_2/demo_2.log"
    p = subprocess.Popen("bash demo_2.sh 1", cwd="experiments/demo_2/", stdout=open(fp, "w"), shell=True)
    p_status = p.wait()
    with open(fp) as f:
        output = f.read()
    assert "PySample_CLONE_1 task was executed!" in output
    assert "PySample_CLONE_2 task was executed!" in output
    assert "PySample_CLONE_3 task was executed!" in output
    assert "PySample_CLONE_4 task was executed!" in output

def test_demo_2_output():
    out_1 = load_last_line("experiments/demo_2/examples/PySample_CLONE_1.log")
    out_2 = load_last_line("experiments/demo_2/examples/PySample_CLONE_2.log")
    out_3 = load_last_line("experiments/demo_2/examples/PySample_CLONE_3.log")
    out_4 = load_last_line("experiments/demo_2/examples/PySample_CLONE_4.log")
    rmtree("experiments/demo_2/")
    assert out_1 == "0.1 0.5 default"
    assert out_2 == "0.1 1.0 default"
    assert out_3 == "10.0 -10.0 default"
    assert out_4 == "-10.0 10.0 default"
    rmtree("experiments/")