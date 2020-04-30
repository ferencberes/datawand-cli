import os, json
from jinja2 import Template
from .templates import NOTEBOOK_SAMPLE, PY_SAMPLE

def create_notebook(path):
    template = Template(NOTEBOOK_SAMPLE)
    rendered = template.render(rel_path="ALMA", pipeline_name="KORTE")
    with open(path, 'w') as f:
        f.write(rendered)
        
def create_pyscript(path):
    template = Template(PY_SAMPLE)
    rendered = template.render(rel_path="ALMA", pipeline_name="KORTE")
    with open(path, 'w') as f:
        f.write(rendered)
        
def remove_from_pipeline(objects, obj_name):
    tmp = objects.copy()
    for i, item in enumerate(objects):
        if item.name == obj_name:
            break
    del tmp[i]
    return tmp, objects[i].path

class Base():
    def __init__(self, name, type, path, extensions=[]):
        self.name = name
        self.type = type
        self._extensions = extensions
        self.path = path
        
    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type
    
    @property
    def path(self):
        return self._path
    
    @name.setter
    def name(self, value):
        if " " in str(value):
            raise ValueError("Object name cannot contain spaces!")
        self._name = value

    @type.setter
    def type(self, value):
        self._type = str(value)
        
    @path.setter
    def path(self, value):
        if value != "" and len(self._extensions) > 0:
            ext = value.split(".")[-1]
            if ext not in self._extensions:
                raise ValueError("Invalid file extension '%w'! It must be '.%s'." % (ext, str(self._extensions)))
            if not os.path.exists(value):
                self._create(value)
            self._path = value

    def _create(self, path):
        pass
    
    def get(self, deps=[]):
        conf = {"name":self.name, "type":self.type, "path":self.path}
        if len(deps) > 0:
            conf["dependencies"] = deps
        return conf
        
    def load(self, config):
        self.extensions = [config["path"].split(".")[-1]]
        self.name = config["name"]
        self.type = config["type"]
        self.path = config["path"]
    
class Configurable(Base):
    def __init__(self, name="", type="", path="", extensions=[]):
        super(Configurable, self).__init__(name, type, path, extensions)
        self.config = {}
        
    @property
    def config(self):
        return self._config
    
    @config.setter
    def config(self, value):
        if not isinstance(value, dict):
            raise ValueError("Parameters must be stored in a dictionary!")
        self._config = value
        
class ModuleObject(Configurable):
    def __init__(self, name="", type="", path="", extensions=["py"]):
        super(ModuleObject, self).__init__(name, type, path, extensions)
        
    def _create(self, path):
        print("Creating new python module: %s" % path)
        f = open(path, 'w')
        f.close()
        
class NotebookObject(Configurable):
    def __init__(self, name="", type="", path="", extensions=["ipynb"]):
        super(NotebookObject, self).__init__(name, type, path, extensions)
        
    def _create(self, path):
        print("Creating new ipython notebook: %s" % path)
        create_notebook(path)
        
class PyScriptObject(Configurable):
    def __init__(self, name="", type="", path="", extensions=["py"]):
        super(PyScriptObject, self).__init__(name, type, path, extensions)
        
    def _create(self, path):
        print("Creating new python script: %s" % path)
        create_pyscript(path)
        
class Pipeline():
    def __init__(self, name="", directory=None, description=""):
        self.name = name
        self.description = description
        self.path = "%s/%s.json" % (directory, self.name)
        self.modules = []
        self.notebooks = []
        self.pyscripts = []
        self.dependencies = {}
        self.parts = {}
        self.file_paths = []

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if " " in str(value):
            raise ValueError("Pipeline name cannot contain spaces!")
        self._name = value
    
    @property
    def config(self):
        conf = {}
        conf["name"] = self.name
        conf["description"] = self.description
        conf["config_path"] = self.path
        conf["imports"] = [item.get() for item in self.modules]
        conf["notebooks"] = [item.get(self.dependencies.get(item.name, [])) for item in self.notebooks]
        conf["py_scripts"] = [item.get(self.dependencies.get(item.name, [])) for item in self.pyscripts]
        return conf
    
    def clear(self, with_source=False):
        names = list(self.parts.keys())
        for obj_name in names:
            self.remove(obj_name, with_source)
    
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.config, f, sort_keys=True, indent="    ")
        print("Pipeline was SAVED")
    
    def load(self, config_path):
        ext = config_path.split(".")[-1]
        if ext == "json":
            with open(config_path) as f:
                config = json.load(f)
            self.name = config["name"]
            self.description = config["description"]
            self.path = config_path
            # parse modules
            self.modules = []
            for item in config["imports"]:
                mod = ModuleObject(item["name"], item["type"], item["path"])
                self.add(mod)
            # parse notebooks
            self.notebooks = []
            for item in config["notebooks"]:
                nb = NotebookObject(item["name"], item["type"], item["path"])
                self.add(nb)
            # parse scripts
            self.pyscripts = []
            for item in config["py_scripts"]:
                ps = PyScriptObject(item["name"], item["type"], item["path"])
                self.add(ps)
            # parse dependencies
            for item in config["notebooks"] + config["py_scripts"]:
                deps = item.get("dependencies",[])
                if len(deps) > 0:
                    self.add_dependencies(item["name"], deps)
            print("Pipeline was LOADED")
        else:
            raise ValueError("Invalid path! You must specify a JSON file.")
    
    def add(self, obj, silent=False):
        obj_name = obj.name
        obj_path = obj.path
        if obj_name in self.parts:
            if not silent:
                print("An object with 'name=%s' is already present in the pipeline. The names of the components must be unique!" % obj_name)
        elif obj_path in self.file_paths:
            if not silent:
                print("An object with 'path=%s' is already present in the pipeline. Cannot add the same file twice!" % obj_path)
        else:
            if isinstance(obj, ModuleObject):
                self.modules.append(obj)
                self.parts[obj_name] = "module"
            elif isinstance(obj, NotebookObject):
                self.notebooks.append(obj)
                self.parts[obj_name] = "notebook"
            elif isinstance(obj, PyScriptObject):
                self.pyscripts.append(obj)
                self.parts[obj_name] = "pyscript"
            else:
                raise ValueError("Object with invalid type!")
            self.file_paths.append(obj_path)
    
    def remove(self, obj_name, with_source=False, silent=False):
        if obj_name in self.parts:
            obj_type = self.parts[obj_name]
            if obj_type == "module":
                self.modules, fp = remove_from_pipeline(self.modules, obj_name)
            elif obj_type == "notebook":
                self.notebooks, fp = remove_from_pipeline(self.notebooks, obj_name)
            else:
                self.pyscripts, fp = remove_from_pipeline(self.pyscripts, obj_name)
            del self.parts[obj_name]
            self.file_paths.remove(fp)
            # remove all dependencies of this item
            if obj_name in self.dependencies:
                del self.dependencies[obj_name]
            # remove if it was a dependency
            keys = list(self.dependencies.keys())
            for key in keys:
                if obj_name in self.dependencies[key]:
                    self.remove_dependencies(key, [obj_name])
            if with_source:
                os.remove(fp)
                print("%s file was deleted!" % fp)
        else:
            if not silent:
                print("There was no object with 'name=%s' found in the pipeline" % obj_name)
            
    def add_dependencies(self, obj_name, dep_names=[], reset=False):
        for name in [obj_name]+dep_names:
            if name not in self.parts:
                raise ValueError("'%s' name was not found in the pipeline!" % name)
            elif self.parts[name] == "module":
                raise ValueError("Cannot set dependencies for ModuleObjects (name=%s)!" % name)
        if obj_name in self.dependencies and not reset:
            self.dependencies[obj_name] = list(set(self.dependencies[obj_name]).union(set(dep_names)))
        else:
            self.dependencies[obj_name] = dep_names
            
    def remove_dependencies(self, obj_name, dep_names=[]):
         if obj_name in self.dependencies:
                for dep_name in dep_names:
                    if dep_name in self.dependencies[obj_name]:
                        self.dependencies[obj_name].remove(dep_name)
                        if len(self.dependencies[obj_name]) == 0:
                            del self.dependencies[obj_name]
                            break