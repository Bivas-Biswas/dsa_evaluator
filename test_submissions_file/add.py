import sys
with open(sys.argv[1], 'r') as f:
    a, b = map(int, f.read().split())
with open(sys.argv[2], 'w') as f:
    f.write(str(a + b) + "\n")