import numpy as np

data = np.loadtxt("input/day1.txt")
print(np.sum(np.diff(data) > 0))

windowed = data[:-2] + data[1:-1] + data[2:]
print(np.sum(np.diff(windowed) > 0))
