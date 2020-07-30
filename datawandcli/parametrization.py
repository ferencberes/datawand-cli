import os
from datawandcli.cli.utils import get_luigi_conf
from datawandcli.components.objects import Pipeline, Configurable, Module, PyScript, Notebook
from datawandcli.components.luigi import *

class ParamHelper():
    r"""
    With ParamHelper you can access the parameters assigned to a given pipeline component.
    
    Args:
        base_dir: Provide relative path to the project root folder
        pipeline_name: Provide the name of your pipeline
        args: sys.argv
    """
    def __init__(self, base_dir, pipeline_name, args):
        self._base_dir = base_dir
        self._pipeline_name = pipeline_name
        self._execution_path = args[0]
        self._load_pipeline()
        self._load_custom_config()
        item_config = self.default_config.copy()
        item_config.update(self.custom_config)
        print(item_config)
    
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
            return os.path.join(self.base_dir, self.pipeline_name + ".json")
        
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
        
    def _load_custom_config(self):
        conf = {}
        executed_file = os.path.split(self._execution_path)[1]
        for name, obj in self.pipeline.parts.items():
            fp = obj.path
            fname = os.path.split(fp)[1]
            if fname == executed_file:
                conf = obj.config
                break
        self._custom_config = conf
    
    def get(self, param_id):
        r"""
        Use this function to query object parameters
        
        Args:
            param_id: Provide string identifier (dictionary key value) for the parameter to query 
        """
        if param_id in self.custom_config:
            return self.custom_config[param_id]
        elif param_id in self.default_config:
            val = self.default_config[param_id]
            print("Using the default value '%s=%s'!" % (param_id, str(val)))
            return val
        else:
            raise KeyError("Parameter '%s' was not provided for this pipeline!" % param_id)
        
        
class ConfigGenerator():
    r"""
    With ConfigGenerator you can assign parameters to pipeline components.
    
    Args:
        pipeline_path: Provide relative path to pipeline JSON configuration file
        clear: Clear pipeline before setting parameters
        experiment_dir: Provide path relative to the project root folder
        experiment_name: Provide experiment name
    """
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
        for name, item in self.pipeline.parts.items():
            if isinstance(item, Configurable):
                self._configurables.append(name)
    
    def _resolve_clone_dependencies(self):
        tuples = list(self.pipeline.dependencies.items())
        for item, dependencies in tuples:
            item_nc = self.pipeline.num_clones.get(item, 0)
            if item_nc > 0:
                for dep in dependencies:
                    dep_nc = self.pipeline.num_clones.get(dep, 0)
                    if dep_nc > 0:
                        clone_deps = ["%s_CLONE_%i" % (dep,j) for j in range(1,dep_nc+1)]
                        for i in range(1, item_nc+1):
                            self.pipeline.add_dependencies("%s_CLONE_%i" % (item,i), clone_deps)
    
    def save_params(self, default_config, custom_config={}, with_luigi=True, local_scheduler=False):
        r"""
        Save parameter configuration for you pipeline.
        
        Args:
            default_config (dict): Provide parameters shared among all pipeline components
            custom_config (dict of lists): Provide custom parameters for selected components
            with_luigi: Generate executable files for the Luigi Scheduler framework
            local_scheduler: Use local scheduling for Luigi
        """
        self.pipeline.default_config = default_config
        # add clones with dependencies
        for obj_name, obj_clones in custom_config.items():
            if not isinstance(obj_clones, list):
                raise ValueError("For each object specify the list of clones with configuration!")
            else:
                for clone_conf in obj_clones:
                    self.pipeline.add_clone(obj_name, clone_conf)
        self._resolve_clone_dependencies()
        # delete original resources
        to_be_removed = []
        for name, obj in self.pipeline.parts.items():
            if not obj.is_clone and not isinstance(obj, Module):
                to_be_removed.append(name)
        for name in to_be_removed:
            self.pipeline.remove(name)
        # save pipeline
        output_path = self.pipeline.save()
        # generate luigi plan
        if with_luigi:
            self._generate_luigi_plan(local_scheduler)
        print("### New experiment was created ###")
        print("Name:", self.pipeline.experiment_name)
        print("Path:", output_path)
        
    def _generate_luigi_plan(self, local_scheduler=False):
        clones = []
        for task_name, obj in self.pipeline.parts.items():
            if obj.is_clone:
                clones.append(obj)
        plan = """
from datawandcli.components.luigi import PythonScriptTask, NotebookTask
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
            if isinstance(obj, PyScript):
                plan += PYSCRIPT_TEMPLATE.render(name=obj.name, path=obj.path, config=obj.config, name_space=experiment_name, deps=deps)
            elif isinstance(obj, Notebook):
                plan += NOTEBOOK_TEMPLATE.render(name=obj.name, path=obj.path, config=obj.config, name_space=experiment_name, deps=deps)
            else:
                raise RuntimeError("Unsupported task object was detected %s!" % obj.name)
            plan += "\n"
        plan += MASTER_TEMPLATE.render(config=self.pipeline.default_config, name_space=experiment_name, deps=dependency_extractor([obj.name for obj in clones]))
        with open(os.path.join(self.pipeline.base_dir, experiment_name + ".py"), 'w') as f:
            f.write(plan)
        with open(os.path.join(self.pipeline.base_dir, experiment_name + ".sh"), 'w') as f:
            if local_scheduler:
                f.write(RUN_LOCAL_TEMPLATE.render(name_space=self.pipeline.experiment_name, task_name="Master"))
            else:
                luigi_cfg_path = f.write(RUN_TEMPLATE.render(cfg_path=get_luigi_conf(), name_space=self.pipeline.experiment_name, task_name="Master"))
        print("Luigi plan was generated")
        
