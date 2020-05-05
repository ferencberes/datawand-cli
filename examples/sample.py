import sys
from datawandcli.parametrization import ParamHelper

print(sys.argv)
ph = ParamHelper('', 'Trial', sys.argv)
print(ph.get("p1"))
print(ph.get("p2"))
print(ph.get("p3"))