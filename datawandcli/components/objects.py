import os, json
from shutil import copyfile
from jinja2 import Template
from .templates import NOTEBOOK_SAMPLE, PY_SAMPLE

def create_object(path, pipeline_name, obj_type, delim=os.path.sep):
    r"""
    Create new object for the given pipeline if the given path does not exists.
    
    Args:
        path: Provide path for new pipeline object
        pipeline_name: Provide pipeline name
        obj_time: Choose from values ['pyscript','notebook','module']
    """
    success = False
    if not os.path.exists(path):
        obj_type_lower = obj_type.lower()
        if obj_type_lower == "module":
            content = ""
        else:
            if obj_type_lower=="pyscript":
                template = Template(PY_SAMPLE)
            elif obj_type_lower == "notebook":
                template = Template(NOTEBOOK_SAMPLE)
            else:
                raise ValueError("Choose object_type from values ['pyscript','notebook','module']!")
            depth = len(path.split(delim))-1
            parent_dir = ".." + os.path.sep
            content = template.render(rel_path=parent_dir*depth, pipeline_name=pipeline_name)
        with open(path, 'w') as f:
            f.write(content)
        success = True
    else:
        # if file exists then it would not be overwritten
        success = True
    return success
        
def remove_from_pipeline(objects, obj_name):
    tmp = objects.copy()
    for i, item in enumerate(objects):
        if item.name == obj_name:
            break
    del tmp[i]
    return tmp, objects[i].path

class Base():
    r"""
    Base is the abstract representation of all pipeline components. It is non configurable and only contains basic information on each object.
    
    Args:
        path: Provide path relative to the project root folder 
        name (optional): Provide a reference name for this object. It must be unique among pipeline components!
        type (optional): Provide a note on the type or purpose of this object (e.g. visualization, preprocessor, data etc.)
    """
    def __init__(self, path, name="", type="", is_clone=False, extensions=[]):
        self._extensions = extensions
        self.is_clone = is_clone
        self.path = path
        self.name = self._extract_name(path) if (name == "" or name == None) else name
        self.type = type
        
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
        if len(self._extensions) > 0:
            ext = value.split(".")[-1]
            if ext not in self._extensions:
                raise ValueError("Invalid file extension '%s'! It must be '.%s'." % (str(ext), str(self._extensions)))
        #if not os.path.exists(value) and not self.is_clone:
        #    print("FileNotFound:", value)
        #    raise FileNotFoundError(value)
        self._path = value
        
    def _extract_name(self, file_name, delim=os.path.sep):
        return ".".join(file_name.split(delim)[-1].split(".")[:-1])
    
    def get(self, deps=[]):
        conf = {"name":self.name, "type":self.type, "path":self.path}
        conf["is_clone"] = "yes" if self.is_clone else "no"
        if len(deps) > 0:
            conf["dependencies"] = deps
        return conf
        
    def load(self, config):
        self.extensions = [config["path"].split(".")[-1]]
        self.is_clone = config["is_clone"] == "yes"
        self.name = config["name"]
        self.type = config["type"]
        self.path = config["path"]
    
class ModuleObject(Base):
    r"""
    ModuleObject represents any unconfigurable pipeline components (e.g. Python module, data or API key files).
    """
    def __init__(self, path, name="", type="module"):
        super(ModuleObject, self).__init__(path, name, type)
    
class Configurable(Base):
    r"""
    Configurable is a pipeline component with custom parameters. Its main purpose is to enable pipeline object execution with different parameters in parallel.
    
    Args:
        config (optinal): Provide parameters to the given pipeline object through a dictionary.
    """
    def __init__(self, path, name="", type="", is_clone=False, config={}, extensions=[]):
        super(Configurable, self).__init__(path, name, type, is_clone, extensions)
        self.config = config
        
    @property
    def config(self):
        return self._config
    
    @config.setter
    def config(self, value):
        if not isinstance(value, dict):
            raise ValueError("Parameters must be stored in a dictionary!")
        self._config = value
        
    def get(self, deps=[]):
        conf = super(Configurable, self).get(deps)
        conf["config"] = self.config
        return conf
        
    def load(self, config):
        super(Configurable, self).load(config)
        self.config = config.get("config",{})
        

        
class NotebookObject(Configurable):
    r"""
    NotebookObject represents Jupyter notebooks in a pipeline.
    """
    def __init__(self, path, name="", type="notebook", is_clone=False, config={}, extensions=["ipynb"]):
        super(NotebookObject, self).__init__(path, name, type, is_clone, config, extensions)
        
    def copy(self):
        return NotebookObject(self.path, self.name, self.type, self.is_clone, self.config)
        
class PyScriptObject(Configurable):
    r"""
    PyScriptObject represents executable Python scripts in a pipeline.
    """
    def __init__(self, path, name="", type="pyscript", is_clone=False, config={}, extensions=["py"]):
        super(PyScriptObject, self).__init__(path, name, type, is_clone, config, extensions)
        
    def copy(self):
        return PyScriptObject(self.path, self.name, self.type, self.is_clone, self.config)
        
class Pipeline():
    r"""
    This object is the representation of a pure Python data science pipeline. It stores components along with their parameters and dependency relations. Clones of the same object can be created with different parametrization in order to execute them in parallel during experiments.
    
    Args:
        name: Provide a name for your pipeline
        description: Provide a short description for your pipeline
        base_dir: Provide path relative to the project root folder. Needed only for scheduling!
        experiment_name: Provide an experiment name. Needed only for scheduling!
    """
    def __init__(self, name="", description="", base_dir="", experiment_name="", verbose=False):
        self.verbose = verbose
        self.name = name
        self.experiment_name = experiment_name
        self.description = description
        self.base_dir = base_dir
        self.parts = {}
        self.file_paths = []
        self.dependencies = {}
        self.num_clones = {}
        self._default_config = {}
        
    @property
    def name(self):
        return self._name
    
    @property
    def experiment_name(self):
        return self.name if self._experiment_name == "" else self._experiment_name
    
    @property
    def base_dir(self):
        return self._base_dir
    
    @base_dir.setter
    def base_dir(self, value):
        #if value != "" and not os.path.exists(value):
        #    os.makedirs(value)
        self._base_dir = value
        
    @experiment_name.setter
    def experiment_name(self, value):
        if " " in str(value):
            raise ValueError("Experiment name cannot contain spaces!")
        self._experiment_name = value
    
    @name.setter
    def name(self, value):
        if " " in str(value):
            raise ValueError("Pipeline name cannot contain spaces!")
        self._name = value
        
    @property
    def default_config(self):
        return self._default_config
    
    @default_config.setter
    def default_config(self, value):
        if isinstance(value, dict):
            self._default_config = value
        else:
            raise ValueError("Configuration must be specified in a dictionary!")
        
    @property
    def modules(self):
        return [obj for obj in self.parts.values() if isinstance(obj, ModuleObject)]
    
    @property
    def notebooks(self):
        return [obj for obj in self.parts.values() if isinstance(obj, NotebookObject)]
    
    @property
    def pyscripts(self):
        return [obj for obj in self.parts.values() if isinstance(obj, PyScriptObject)]
    
    @property
    def config(self):
        conf = {}
        conf["name"] = self.name
        conf["experiment_name"] = self.experiment_name
        conf["base_dir"] = self.base_dir
        conf["description"] = self.description
        conf["default_config"] = self.default_config
        conf["imports"] = [item.get() for item in self.modules]
        conf["notebooks"] = [item.get(self.dependencies.get(item.name, [])) for item in self.notebooks]
        conf["py_scripts"] = [item.get(self.dependencies.get(item.name, [])) for item in self.pyscripts]
        return conf
    
    def _duplicate_file(self, old_path, new_path):
        fp = str(new_path)
        if self.base_dir != "":
            fp = os.path.join(self.base_dir, fp)
        fp_dir, _ = os.path.split(fp)
        if not os.path.exists(fp_dir):
            os.makedirs(fp_dir)
        if old_path != fp:
            copyfile(old_path, fp)
        # check for __init__.py files
        old_dir, old_file = os.path.split(old_path)
        if old_dir != '' and "__init__.py" != old_file:
            if "__init__.py" in os.listdir(old_dir):
                init_path = os.path.join(old_dir, "__init__.py")
                self._duplicate_file(init_path, init_path)
    
    def save(self, output_folder=None):
        r"""
        Save pipeline object to JSON file.
        """
        if output_folder == None:
            output_folder = self.base_dir
        if output_folder == "":
            output_path = "%s.json" % self.name
        else:
            output_path = os.path.join(output_folder, "%s.json" % self.name)
        with open(output_path, 'w') as f:
            json.dump(self.config, f, sort_keys=True, indent="    ")
        for obj in self.modules:
            self._duplicate_file(obj.path, obj.path)
        if self.verbose:
            print("Pipeline was SAVED")
        return output_path
    
    def load(self, path, experiment_name=None, experiment_dir=None):
        r"""
        Load pipeline object from JSON file.
        
        Args:
            path: JSON file path
            experiment_name: Provide experiment name. Needed only for scheduling!
            experiment_dir: Provide path relative to the project root folder. Needed only for scheduling!
        """
        ext = path.split(".")[-1]
        if ext.lower() == "json":
            with open(path) as f:
                config = json.load(f)
            self.name = config["name"]
            self.experiment_name = config.get("experiment_name","") if experiment_name == None else experiment_name
            self.base_dir = config.get("base_dir","") if experiment_dir == None else experiment_dir
            self.description = config["description"]
            self.default_config = config.get("default_config",{})
            self.num_clones = {}
            # parse modules
            for item in config["imports"]:
                mod = ModuleObject(item["path"], item["name"], item["type"])
                self.add(mod)
            # parse notebooks
            for item in config["notebooks"]:
                nb = NotebookObject(item["path"], item["name"], item["type"], item["is_clone"]=="yes", item.get("config",dict()))
                self.add(nb)
            # parse scripts
            for item in config["py_scripts"]:
                ps = PyScriptObject(item["path"], item["name"], item["type"], item["is_clone"]=="yes", item.get("config",dict()))
                self.add(ps)
            # parse dependencies
            for item in config["notebooks"] + config["py_scripts"]:
                deps = item.get("dependencies",[])
                if len(deps) > 0:
                    self.add_dependencies(item["name"], deps)
                if "CLONE" in item["name"]:
                    name = item["name"].split("_CLONE")[0]
                    if not name in self.num_clones:
                        self.num_clones[name] = 0
                    self.num_clones[name] += 1
            if self.verbose:
                print("Pipeline was LOADED")
        else:
            raise ValueError("Invalid path! You must specify a JSON file.")
    
    def add(self, obj, silent=False):
        r"""
        Add new object to the pipeline (e.g. ModuleObject, NotebookObject, PyScriptObject). The new objects'a name parameter must be unique!
        """
        obj_name = obj.name
        obj_path = obj.path
        if obj_name in self.parts:
            if not silent:
                print("An object with 'name=%s' is already present in the pipeline. Object names must be unique!" % obj_name)
        else:
            self.parts[obj_name] = obj
            self.file_paths.append(obj_path)
    
    def remove(self, obj_name, with_source=False, silent=False):
        r"""
        Remove object from the pipeline.
        
        Args:
           obj_name: Provide the name of the object to be deleted
           with_source: Decide whether the source file of the object should be deleted as well
        """
        if obj_name in self.parts:
            obj = self.parts[obj_name]
            fp = obj.path
            del self.parts[obj_name]
            to_be_deleted = isinstance(obj, ModuleObject) or not obj.is_clone
            if to_be_deleted:
                self.file_paths.remove(fp)
            # remove all dependencies of this item
            if obj_name in self.dependencies:
                del self.dependencies[obj_name]
            # remove if it was a dependency
            keys = list(self.dependencies.keys())
            for key in keys:
                if obj_name in self.dependencies[key]:
                    self.remove_dependencies(key, [obj_name])
            if with_source and os.path.exists(fp):
                os.remove(fp)
                print("%s file was deleted!" % fp)
        else:
            if not silent:
                print("There was no object with 'name=%s' found in the pipeline" % obj_name)
            
    def add_dependencies(self, obj_name, dep_names=[], reset=False):
        r"""
        Add new dependencies between pipeline objects
        
        Args:
            obj_name: Select an object by name
            dep_names: Provide the list of object names that the selected item depends on.
            reset: Decide whether to reset former dependencies
        """
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
        r"""
        Delete existing dependencies between pipeline objects
        
        Args:
            obj_name: Select an object by name
            dep_names: Provide the list of object names that the selected item no longer depends on. Note that all dependencies are deleted if the list is empty.
        """
        if obj_name in self.dependencies:
            if len(dep_names) > 0:            
                for dep_name in dep_names:
                    if dep_name in self.dependencies[obj_name]:
                        self.dependencies[obj_name].remove(dep_name)
                        if len(self.dependencies[obj_name]) == 0:
                            del self.dependencies[obj_name]
                            break
            else:
                del self.dependencies[obj_name]
                            
    def add_clone(self, obj_name, custom_config={}):
        r"""
        Add new clone item to the pipeline.
        
        Args:
            obj_name: select object to be cloned by name
            custom_config: provide custom configuration for the new clone
        """
        if not isinstance(custom_config, dict):
            raise ValueError("Configuration must be specified in a dictionary!")
        if obj_name in self.parts:
            obj_config = custom_config
            cnt = self.num_clones.get(obj_name, 0)
            postfix = "_CLONE_%i" % (cnt+1)
            clone = self.parts[obj_name].copy()
            clone.is_clone = True
            clone.name = obj_name + postfix
            clone.config = obj_config
            old_path = str(clone.path)
            extension = old_path.split(".")[-1]
            new_path = old_path.replace("."+extension,postfix+"."+extension)
            clone.path = new_path
            self._duplicate_file(old_path, new_path)
            self.add(clone)
            self.num_clones[obj_name] = (cnt+1)
        else:
            raise ValueError("Invalid object name!")
    
    def clear(self):
        r"""
        Remove all clones from the pipeline.
        """
        # remove clones
        items = list(self.num_clones.items())
        for obj_name, cnt in items:
            for i in range(cnt):
                clone_name = "%s_CLONE_%i" % (obj_name, i+1)
                self.remove(clone_name, with_source=False)
            del self.num_clones[obj_name]
        # clear config
        self.default_config = {}
        for obj_name in self.parts:
            if isinstance(self.parts[obj_name], Configurable):
                self.parts[obj_name].config = {}
