import luigi, os, time, subprocess
from jinja2 import Template

### Task Abstraction ###

class PythonScriptTask(luigi.Task):
    
    @property
    def info_path(self):
        return ".".join(self.source_path.split(".")[:-1]) + ".info"
    
    @property
    def pid_path(self):
        return ".".join(self.source_path.split(".")[:-1]) + ".pid"
    
    @property
    def log_path(self):
        return ".".join(self.source_path.split(".")[:-1]) + ".log"
    
    @property
    def source_dir(self):
        return "/".join(self.source_path.split("/")[:-1])
    
    @property
    def task_name(self):
        return self.source_path.split("/")[-1]
    
    def output(self):
        return luigi.LocalTarget(self.info_path)

    def keep_pid_while_running(self, process):
        with open(self.pid_path, "w") as fp:
            fp.write(str(process.pid))
        while process.poll() is None:
            time.sleep(1)
        os.remove(self.pid_path)

    def run(self):
        fp = open(self.log_path, "w")
        process = subprocess.Popen(["python", "-u", self.source_path, self.task_namespace], stdout=fp, stderr=fp)
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
PYTHONPATH='.' luigi --module {{ name_space }} {{ name_space }}.{{task_name}} --workers $1
""")

run_local_template = Template("""
PYTHONPATH='.' luigi --module {{ name_space }} {{ name_space }}.{{task_name}} --local-scheduler --workers $1
""")

SUCCESS_MSG = "This progress looks :) because there were no failed tasks or missing dependencies"

FAILURE_MSG = "This progress looks :( because there were failed tasks"