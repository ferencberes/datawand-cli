import networkx as nx
import pandas as pd
import sys
from datawandcli.parametrization import ParamHelper

ph = ParamHelper('..', 'GraphDemo', sys.argv, comet_fp="../comet_key.txt")
metric = ph.get("metric")

G = nx.karate_club_graph()
if metric == "pagerank":
    scores = dict(nx.pagerank(G))
elif metric == "degree":
    scores = dict(nx.degree_centrality(G))
elif metric == "closeness":
    scores = dict(nx.closeness_centrality(G))
elif metric == "betweenness":
    scores = dict(nx.betweenness_centrality(G))
else:
    raise ValueError("Unsupported centrality score!")

scores_df = pd.DataFrame(scores.items(), columns=["id",metric])
ph.experiment.log_metric("size",len(scores_df))
scores_df.to_csv("%s.csv" % metric, index=False)
print("done")
ph.close()