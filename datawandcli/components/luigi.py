import luigi, os, time, subprocess
from jinja2 import Template

### Task Abstraction ###

class BaseTask(luigi.Task):
    @property
    def source_dir(self):
        return os.path.split(self.source_path)[0]
    
    @property
    def info_path(self):
        return os.path.join(self.source_dir, self.task_name + ".info")
    
    @property
    def pid_path(self):
        return os.path.join(self.source_dir, self.task_name + ".pid")
    
    @property
    def log_path(self):
        return os.path.join(self.source_dir, self.task_name + ".log")
    
    def output(self):
        return luigi.LocalTarget(self.info_path)

    def keep_pid_while_running(self, process):
        with open(self.pid_path, "w") as fp:
            fp.write(str(process.pid))
        while process.poll() is None:
            time.sleep(1)
        os.remove(self.pid_path)

    def run(self):
        resource_dir, resource_name = os.path.split(self.source_path)
        fp = open(self.log_path, "w")
        # NOTE: namespace must be given in order to be able to kill the processes successfully!
        process = subprocess.Popen(self.execution_command(resource_name, self.task_namespace), cwd=resource_dir, stdout=fp, stderr=fp)
        self.keep_pid_while_running(process)
        fp.close()
        if process.returncode != 0:
            with open(self.log_path):
                print(fp.readlines())
            raise RuntimeError("Error during execution!")
        with open(self.output().fn, "w") as fout:
            fout.write('OK')
        print("%s task was executed!" % self.task_name)
        
class PythonScriptTask(BaseTask):
    def execution_command(self, resource_name, namespace):
        return ["python", "-u", resource_name, namespace]
    
class NotebookTask(BaseTask):
    def execution_command(self, resource_name, namespace):
        return ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=None", "--execute", "--to", "notebook", resource_name, "--output", resource_name, namespace]
    
### Task templates ###

def dependency_extractor(deps):
    out = ""
    for i, name in enumerate(deps):
        out += str(name)+"()"
        if i != len(deps)-1:
            out += ", "
    return out

def base_task_template_factory(task_type):
    return Template("""
class {{ name }}(""" + task_type + """):
    params = luigi.parameter.DictParameter(default={{ config }})
    source_path = "{{ path }}"
    task_name = "{{ name }}"
    task_namespace = "{{ name_space }}"
    {% if deps|length > 0 %}
    def requires(self):
        return [{{ deps }}]
    {% endif %}
""")

PYSCRIPT_TEMPLATE = base_task_template_factory("PythonScriptTask")
NOTEBOOK_TEMPLATE = base_task_template_factory("NotebookTask")
MASTER_TEMPLATE = Template("""
class Master(luigi.Task):
    params = luigi.parameter.DictParameter(default={{ config }})
    task_namespace = "{{ name_space }}"
    
    def requires(self):
        return [{{ deps }}]
    
    def run(self):
        print("All dependencies are done")
""")

RUN_TEMPLATE = Template("""
export LUIGI_CONFIG_PATH={{ cfg_path }};
PYTHONPATH='.' luigi --module {{ name_space }} {{ name_space }}.{{task_name}} --workers $1
""")

RUN_LOCAL_TEMPLATE = Template("""
PYTHONPATH='.' luigi --module {{ name_space }} {{ name_space }}.{{task_name}} --local-scheduler --workers $1
""")

SUCCESS_MSG = "This progress looks :)"
FAILURE_MSG = "This progress looks :("