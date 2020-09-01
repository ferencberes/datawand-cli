from datawandcli.parametrization import ConfigGenerator

metrics = ["degree","pagerank","closeness","betweenness"]
corr_types = ["pearson","spearman"]

cg = ConfigGenerator("GraphDemo.json", experiment_name="demo", experiment_dir="experiments/demo/")
DEFAULTS = {}
DEFAULTS["metrics"] = metrics

PARAMETERS = {}
for item in cg.pythonitem_names:
    PARAMETERS[item] = []

for m in metrics:
    PARAMETERS["centrality"].append({"metric":m})
for c in corr_types:
    PARAMETERS["correlation"].append({"corr_type":c})
    
cg.save_params(DEFAULTS, PARAMETERS)
cg.pipeline.save()