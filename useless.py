import sys

kk = sys.argv[1]

with open(kk,'r') as f:
    data = f.read()
print repr(data)
