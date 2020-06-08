import luigi, os, time, subprocess
from jinja2 import Template

### Task Abstraction ###

class PythonScriptTask(luigi.Task):
    
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
        script_dir, script_name = os.path.split(self.source_path)
        fp = open(self.log_path, "w")
        process = subprocess.Popen(["python", "-u", script_name, self.task_namespace], cwd=script_dir, stdout=fp, stderr=fp)
        self.keep_pid_while_running(process)
        fp.close()
        if process.returncode != 0:
            raise RuntimeError("Error when executing a python script!")
        with open(self.output().fn, "w") as fout:
            fout.write('OK')
        print("%s task was executed!" % self.task_name)

def dependency_extractor(deps):
    out = ""
    for i, name in enumerate(deps):
        out += str(name)+"()"
        if i != len(deps)-1:
            out += ", "
    return out
        
pyscript_template = Template("""
class {{ name }}(PythonScriptTask):
    params = luigi.parameter.DictParameter(default={{ config }})
    source_path = "{{ path }}"
    task_name = "{{ name }}"
    task_namespace = "{{ name_space }}"
    {% if deps|length > 0 %}
    def requires(self):
        return [{{ deps }}]
    {% endif %}
""")

master_template = Template("""
class Master(luigi.Task):
    params = luigi.parameter.DictParameter(default={{ config }})
    task_namespace = "{{ name_space }}"
    
    def requires(self):
        return [{{ deps }}]
    
    def run(self):
        print("All dependencies are done")
""")

run_template = Template("""
export LUIGI_CONFIG_PATH={{ cfg_path }};
PYTHONPATH='.' luigi --module {{ name_space }} {{ name_space }}.{{task_name}} --workers $1
""")

run_local_template = Template("""
PYTHONPATH='.' luigi --module {{ name_space }} {{ name_space }}.{{task_name}} --local-scheduler --workers $1
""")

SUCCESS_MSG = "This progress looks :)"

FAILURE_MSG = "This progress looks :("
