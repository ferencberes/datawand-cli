import os
from datawandcli.components.objects import *

pipe_dir = ".." + os.path.sep
pipe_name = "First"
module_path = os.path.join("..", "module.py")
nb_path = os.path.join("..", "notebook.ipynb")
script_path_1 = os.path.join("..", "script1.py")
script_path_2 = os.path.join("..", "script2.py")
pipe_config_path = os.path.join(pipe_dir, pipe_name + ".json")

def test_create_obj():
    assert create_object(module_path, pipe_name, "module")
    assert create_object(nb_path, pipe_name, "notebook")
    assert create_object(script_path_1, pipe_name, "pyscript")
    assert create_object(script_path_2, pipe_name, "pyscript")

def test_add_obj():
    mod = Module(module_path)
    nb = Notebook(nb_path)
    py1 = PyScript(script_path_1)
    py2 = PyScript(script_path_2)
    pipe = Pipeline(pipe_name)
    pipe.description = "bla bla bla"
    for obj in [mod, nb, py1, py2]:
        pipe.add(obj)
    pipe.save(pipe_dir)
    assert len(pipe.modules) == 1
    assert len(pipe.notebooks) == 1
    assert len(pipe.pyscripts) == 2

def test_add_deps():
    pipe = Pipeline()
    pipe.load(pipe_config_path)
    pipe.add_dependencies("script1",["notebook"])
    pipe.add_dependencies("script2",["notebook","script1"])
    pipe.save(pipe_dir)
    assert len(pipe.dependencies) == 2
    assert len(pipe.dependencies["script2"]) == 2
    
def test_add_clones():
    pipe = Pipeline()
    pipe.load(pipe_config_path)
    pipe.add_clone("script1", {"val":1})
    pipe.add_clone("script1", {"val":2})
    pipe.add_clone("script2", {"val":5})
    print(pipe.config)
    pipe.save(pipe_dir)
    assert pipe.num_clones["script1"] == 2
    assert pipe.num_clones["script2"] == 1
    assert len(pipe.pyscripts) == 5

def test_clear():
    pipe = Pipeline()
    pipe.load(pipe_config_path)
    pipe.clear()
    pipe.save(pipe_dir)
    assert len(pipe.num_clones) == 0
    assert len(pipe.pyscripts) == 2

def test_remove_obj():
    pipe = Pipeline()
    pipe.load(pipe_config_path)
    pipe.remove("notebook", with_source=True)
    pipe.save(pipe_dir)
    assert len(pipe.notebooks) == 0
    assert not os.path.exists(os.path.join("..", "notebook.py"))
    assert len(pipe.dependencies) == 1
    assert len(pipe.dependencies["script2"]) == 1

def test_remove_deps():
    pipe = Pipeline()
    pipe.load(pipe_config_path)
    pipe.remove_dependencies("script2",["script1"])
    pipe.save(pipe_dir)
    assert len(pipe.dependencies) == 0

def test_cleanup():
    pipe = Pipeline()
    pipe.load(pipe_config_path)
    print(pipe.config)
    print(pipe.num_clones)
    names = list(pipe.parts.keys())
    for name in names:
        pipe.remove(name, with_source=True)
    os.remove(pipe_config_path)
    assert len(pipe.modules) == 0
    assert len(pipe.notebooks) == 0
    assert len(pipe.pyscripts) == 0
    assert len(pipe.dependencies) == 0