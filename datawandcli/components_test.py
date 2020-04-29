import os
from components.objects import *

pipe_dir = "../"
pipe_name = "First"

def test_create():
    mod = ModuleObject("module","trial","../module.py")
    nb = NotebookObject("notebook","trial","..notebook.ipynb")
    py1 = PyScriptObject("script1","trial","../script1.py")
    py2 = PyScriptObject("script2","trial","../script2.py")
    pipe = Pipeline(pipe_name, pipe_dir)
    pipe.description = "bla bla bla"
    for obj in [mod, nb, py1, py2]:
        pipe.add(obj)
    pipe.save()
    assert len(pipe.modules) == 1
    assert len(pipe.notebooks) == 1
    assert len(pipe.pyscripts) == 2

def test_deps():
    pipe = Pipeline()
    pipe.load("%s/%s.json" % (pipe_dir, pipe_name))
    pipe.set_dependencies("script1",["notebook"])
    pipe.set_dependencies("script2",["notebook","script1"])
    pipe.save()
    assert len(pipe.dependencies) == 2
    assert len(pipe.dependencies["script2"]) == 2
    
def test_remove():
    pipe = Pipeline()
    pipe.load("%s/%s.json" % (pipe_dir, pipe_name))
    pipe.remove("notebook", with_source=True)
    pipe.save()
    assert len(pipe.notebooks) == 0
    assert not os.path.exists("../notebook.py")
    assert len(pipe.dependencies) == 1
    assert len(pipe.dependencies["script2"]) == 1
    
def test_clear():
    pipe = Pipeline()
    pipe.load("%s/%s.json" % (pipe_dir, pipe_name))
    pipe.clear(True)
    os.remove("%s/%s.json" % (pipe_dir, pipe_name))
    assert len(pipe.modules) == 0
    assert len(pipe.notebooks) == 0
    assert len(pipe.pyscripts) == 0
    assert len(pipe.dependencies) == 0