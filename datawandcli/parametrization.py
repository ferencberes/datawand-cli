from datawandcli.components.objects import Pipeline, Configurable

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
            if self.pipeline.base_dir == "":
                fp = obj.path
            else:
                fp = self.pipeline.base_dir + "/" + obj.path
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
        self.pipeline.load(pipe_path)
        for name, item in self.pipeline.parts.items():
            if isinstance(item, Configurable):
                self._configurables.append(name)
                
    def save_params(self, default_config, custom_config={}):
        self.pipeline.default_config = default_config
        for obj_name, obj_clones in custom_config.items():
            if not isinstance(obj_clones, list):
                raise ValueError("For each object specify the list of clones with configuration!")
            else:
                for clone_conf in obj_clones:
                    self.pipeline.add_clone(obj_name, clone_conf)
        if self.experiment_name != None:
            self.pipeline.name = self.experiment_name
        if self.experiment_dir != None:
            self.pipeline.base_dir = self.experiment_dir
        self.pipeline.save()