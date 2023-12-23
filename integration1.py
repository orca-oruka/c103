# the area of a pair of buoys as monostatic or bistatic
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

# parameters
R1 = 1.5  #monostatic detection range
R2 = 2  #bistatic detection range
d_max = 5   #half of max distance between two buoys, equals to x-value of the buoy position
step = 0.05 

def f1(x):
    return np.sqrt(R1**2 - (x - d)**2)

def f2(x):
    return np.sqrt(np.sqrt(4 * (d**2) * (x**2) + R2**4) - x**2 - d**2)

data = np.zeros(int(d_max/step)+1)
data1 = np.zeros(int(d_max/step)+1)
data2 = np.zeros(int(d_max/step)+1)
d = 0
g1 = 0
h1 = d + R1
g2 = 0
h2 = np.sqrt(d**2 + R2**2)
data[0] = 0
data1[0] = 4 * integrate.quad(f1, g1, h1)[0]
data2[0] = 4 * integrate.quad(f2, g2, h2)[0]
for i in range(int(d_max/step)):
    d = d + step
    g1 = max(0, d - R1)
    h1 = d + R1
    if d <= R2:
        g2 = 0
    else:
        g2 = np.sqrt(d**2 - R2**2)
    h2 = np.sqrt(d**2 + R2**2)
    data[i+1] = d
    data1[i+1] = 4 * integrate.quad(f1, g1, h1)[0]
    data2[i+1] = 4 * integrate.quad(f2, g2, h2)[0]

plt.plot(data, data1, color='red', label='monostatic')
plt.plot(data, data2, color='blue', label='bistatic')
plt.legend()
plt.show()
