import pandas as pd
import sys
from datawandcli.parametrization import ParamHelper

ph = ParamHelper('..', 'GraphDemo', sys.argv)
metrics = ph.get("metrics")
corr_type = ph.get("corr_type")

scores_df = pd.read_csv("%s.csv" % metrics[0])
for m in metrics[1:]:
    scores_df = scores_df.merge(pd.read_csv("%s.csv" % m), on="id")
scores_df = scores_df.drop("id", axis=1)
print(scores_df.corr(method=corr_type))