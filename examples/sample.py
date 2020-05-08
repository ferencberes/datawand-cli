import sys
from my_module import print_params
from datawandcli.parametrization import ParamHelper

ph = ParamHelper('', 'Trial', sys.argv)
p1, p2, p3 = ph.get("p1"),ph.get("p2"),ph.get("p3")
print_params(p1, p2, p3)