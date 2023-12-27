#program for detection area dependence on area of random multistataic field using source buoys and receiver buoys in large target area
import scipy.spatial.distance as distance
import numpy as np
from numpy.random import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#parameters
det_range = 3      #detection range
s_quant = int(4)    #sources quantity
r_quant = int(12)   #receivers quantity
buoy_side = np.array([5, 10, 15, 20, 25])   #side length of buoy field
tgt_side = 30   #side length of detection area
db = 0.1        #direct blast effect
trial_1 = int(1000)    #number of trial, reproducing the buoy field
trial_2 = int(500)  #number of trial, reproducing detection/nondetection point

count = 0
P = []
det_ave = []
det_max = 0
s_max = []
r_max = []
det_min = trial_2
s_min = []
r_min = []
buoy_loc_param = []
det = np.zeros([buoy_side.size,trial_1])
det_ave = np.zeros([buoy_side.size,trial_1])
dist_P_ss = np.zeros([buoy_side.size,trial_1])
dist_P_rr = np.zeros([buoy_side.size,trial_1])
dist_P_sr = np.zeros([buoy_side.size,trial_1])
dist_P = np.empty([4,buoy_side.size,trial_1])

#sonobuoy field production
for h in range(buoy_side.size):
    for i in range(trial_1):
        source = []
        source = np.random.rand(s_quant,2)
        source = buoy_side[h] * (source - 0.5)
        receiver = []
        receiver = np.random.rand(r_quant,2)
        receiver = buoy_side[h] * (receiver - 0.5)
        dist_P_ss[h][i] = np.average(distance.pdist(source))
        dist_P_rr[h][i] = np.average(distance.pdist(receiver))
        dist_P_sr[h][i] = np.average(distance.cdist(source,receiver))    

        for j in range(trial_2):
            target = []
            x = tgt_side * (random() - 0.5)
            y = tgt_side * (random() - 0.5)

            for k in range(s_quant):

                for l in range(r_quant):
                    R1 = np.sqrt((source[k][0] - x)**2 + (source[k][1] - y)**2)
                    R2 = np.sqrt((receiver[l][0] - x)**2 + (receiver[l][1] - y)**2)
                    R3 = np.sqrt((source[k][0] - receiver[l][0])**2 + (source[k][1] - receiver[l][1])**2)
                
                    if R1*R2 <= det_range**2:
                        if R1 + R2 - R3 >= db:
                            det[h][i] = det[h][i] + 1
                            target = 1
                
                    if target == 1:
                        break
            
                if target == 1:
                    break

        det_ave[h][i] = np.sum(det[h])/(i + 1)

    print('calc progress',int(100*(h+1)/buoy_side.size),'%')  #displaying the progress

print('detection average:')
for h in range(buoy_side.size):
    print(det_ave[h][trial_1 - 1])

#output

#calculations
plt.xlabel("calc No.", fontsize=10) # x軸ラベル
plt.ylabel("detection count", fontsize=10) # y軸ラベル
left = np.arange(0,trial_1)
for h in range(buoy_side.size):
    plt.bar(left, det[h], align='center', color=cm.tab10(h))
    plt.plot(det_ave[h], color=cm.tab10(h), label=buoy_side[h])
plt.legend()
plt.show()

#buoy-buoy distance vs detection count
plt.xlabel("average buoy-buoy distance", fontsize=10) # x軸ラベル
plt.ylabel("detection count", fontsize=10) # y軸ラベル

plt.title('detection count dependence on S-R distance',fontsize=10)
for h in range(buoy_side.size):
    plt.scatter(dist_P_sr[h], det[h], s=6, color=cm.tab10(h), label=buoy_side[h])
plt.legend()
plt.show()

'''
plt.title('detection count dependence on S-S distance',fontsize=10)
for h in range(buoy_side.size):
    plt.scatter(dist_P_ss[h],det[h],marker='.', s=6, color=cm.tab10(h), label=buoy_side[h])
plt.legend()
plt.show()

plt.title('detection count dependence on R-R distance',fontsize=10)
for h in range(buoy_side.size):
    plt.scatter(dist_P_rr[h],det[h],marker='.', s=6, color=cm.tab10(h), label=buoy_side[h])
plt.legend() 
plt.show()
'''
