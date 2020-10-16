# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:52:33 2020
@author: glads
"""

#!/usr/bin/env python

# data analysis program
#
# Usage :
# python analysis.py -i test.dat

import pickle
import numpy as np
import matplotlib.pyplot as plt

from event import Event, Pulse

print("Starting analysis")

# example event loop
count1000 = [0, 0, 0, 0] 
count900 = [0, 0, 0, 0]
count800 = [0, 0, 0, 0]
count700 = [0, 0, 0, 0]
count600 = [0, 0, 0, 0]
count500 = [0, 0, 0, 0]# counts per channel
count400 = [0, 0, 0, 0]
count300 = [0, 0, 0, 0]
count200 = [0, 0, 0, 0]
count100 = [0, 0, 0, 0]

def Count(countl,file):

    ifile = open(file)
    events= pickle.load(ifile)
    
    for event in events:
        for pulse in event.pulses:
            # only count rising edges
            if pulse.edge == 0:
                countl[pulse.chan] += 1

    return countl
    
Count(count1000, '1000.dat')
Count(count900,'900.dat')
Count(count800,'800.dat')
Count(count700,'700.dat')
Count(count600,'600.dat')
Count(count500,'500.dat')
Count(count400,'400.dat')
Count(count300,'300.dat')
Count(count200,'200.dat')
Count(count100, '100.dat')

counts0 = [count1000[0], count900[0],count800[0],count700[0],count600[0],count500[0],count400[0],count300[0],count200[0],count100[0]]
counts1 = [count1000[1], count900[1],count800[1],count700[1],count600[1],count500[1],count400[1],count300[1],count200[1],count100[1]]
counts2 = [count1000[2], count900[2],count800[2],count700[2],count600[2],count500[2],count400[2],count300[2],count200[2],count100[2]]
counts3 = [count1000[3], count900[3],count800[3],count700[3],count600[3],count500[3],count400[3],count300[3],count200[3],count100[3]]
thresh = [1000,900,800,700,600,500,400,300,200,100]
error0 = [np.sqrt(x) for x in counts0]
error1 = [np.sqrt(x) for x in counts1]
error2 = [np.sqrt(x) for x in counts2]
error3 = [np.sqrt(x) for x in counts3]
plt.errorbar(thresh, counts0, yerr = error0, fmt = 'k', label = 'CH0')
plt.errorbar(thresh, counts1, yerr = error1, fmt = 'r', label = 'CH1')
plt.errorbar(thresh, counts2, yerr = error2, fmt = 'g', label = 'CH2')
plt.errorbar(thresh, counts3, yerr = error3, fmt = 'b', label = 'CH3')
plt.ylabel("Events")
plt.xlabel('Threshold (mV)')
plt.legend()
plt.show()
