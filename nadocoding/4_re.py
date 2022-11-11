import re

p = re.compile("ca.e")

m = p.match("case")

print(m.group())