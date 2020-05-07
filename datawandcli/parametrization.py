import os
from datawandcli.components.objects import Pipeline, Configurable
from datawandcli.components.luigi import pyscript_template, master_template, dependency_extractor

class ParamHelper():
    def __init__(self, base_dir, pipeline_name, args):
        self._base_dir = base_dir
        self._pipeline_name = pipeline_name
        self._execution_path = args[0]
        self._load_pipeline()
        self._load_custom_config()
    
    @property
    def base_dir(self):
        return self._base_dir
    
    @property
    def pipeline_name(self):
        return self._pipeline_name
    
    @property
    def path(self):
        if self.base_dir == "":
            return "%s.json" % self.pipeline_name
        else:
            return "%s/%s.json" % (self.base_dir, self.pipeline_name)
        
    @property
    def default_config(self):
        return self.pipeline.default_config
        
    @property
    def custom_config(self):
        return self._custom_config
        
    def _load_pipeline(self):
        pipe = Pipeline()
        pipe.load(self.path)
        self.pipeline = pipe
        print(self.pipeline.config)
        
    def _load_custom_config(self):
        conf = {}
        for name, obj in self.pipeline.parts.items():
            #if self.pipeline.base_dir == "":
            fp = obj.path
            #else:
            #    fp = self.pipeline.base_dir + "/" + obj.path
            if fp == self._execution_path:
                conf = obj.config
                break
        self._custom_config = conf
    
    def get(self, param_id):
        if param_id in self.custom_config:
            return self.custom_config[param_id]
        elif param_id in self.default_config:
            val = self.default_config[param_id]
            print("Using the default value '%s=%s'!" % (param_id, str(val)))
            return val
        else:
            raise KeyError("Parameter '%s' was not provided for this pipeline!" % param_id)
        
        
class ConfigGenerator():
    def __init__(self, pipeline_path, clear=True, experiment_dir=None, experiment_name=None):
        self.experiment_dir = experiment_dir
        self.experiment_name = experiment_name
        self._load(pipeline_path)
        if clear:
            self.pipeline.clear()
        
    @property
    def pythonitem_names(self):
        return self._configurables
    
    @property
    def pipeline_cfg(self):
        return self.pipeline.config
        
    def _load(self, pipe_path):
        self._configurables = []
        self.pipeline = Pipeline()
        self.pipeline.load(pipe_path, self.experiment_name, self.experiment_dir)
        print(self.pipeline.name, self.pipeline.experiment_name)
        for name, item in self.pipeline.parts.items():
            if isinstance(item, Configurable):
                self._configurables.append(name)
                
    def save_params(self, default_config, custom_config={}, with_luigi=True):
        self.pipeline.default_config = default_config
        for obj_name, obj_clones in custom_config.items():
            if not isinstance(obj_clones, list):
                raise ValueError("For each object specify the list of clones with configuration!")
            else:
                for clone_conf in obj_clones:
                    self.pipeline.add_clone(obj_name, clone_conf)
        if with_luigi:
            self.generate_luigi_plan()
        self.pipeline.save()
        
    def generate_luigi_plan(self):
        clones = []
        for task_name, obj in self.pipeline.parts.items():
            if obj.is_clone:
                clones.append(obj)
        plan = """
from datawandcli.components.luigi import PythonScriptTask
import luigi
        """
        experiment_name = self.pipeline.experiment_name
        for obj in clones:
            path_prefix = ".".join(obj.path.split(".")[:-1])
            for tmp_file in [path_prefix+".info", path_prefix+".log"]:
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)
            if obj.name in self.pipeline.dependencies:
                deps = dependency_extractor(self.pipeline.dependencies[obj.name])
            else:
                deps = ""
            plan += pyscript_template.render(name=obj.name, path=obj.path, config=obj.config, name_space=experiment_name, deps=deps)
            plan += "\n"
        plan += master_template.render(config=self.pipeline.default_config, name_space=experiment_name, deps=dependency_extractor([obj.name for obj in clones]))
        with open("%s/%s.py" % (self.pipeline.base_dir, experiment_name), 'w') as f:
            f.write(plan)
        print("Luigi plan was generated")
        