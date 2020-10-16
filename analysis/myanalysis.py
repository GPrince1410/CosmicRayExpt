# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:52:33 2020
@author: glads
"""

#!/usr/bin/env python

# data analysis example program
# Including some examples of how to use DataFrames from pandas
#
# Usage :
# python analysis.py -i test.dat

import pickle
import numpy as np
import matplotlib.pyplot as plt
import argparse

from event import Event, Pulse

print("Starting analysis")

# example event loop
count1000 = np.zeroes(4) 
count900 = np.zeroes(4) 
count800 = np.zeroes(4) 
count700 = np.zeroes(4) 
count600 = np.zeroes(4) 
count500 = np.zeroes(4) 
# counts per channel

def Count(countl,file):
    
    ifile = open(file)
    events= pickle.load(ifile)
    
    for event in events:
        for pulse in event.pulses:
            # only count rising edges
            if pulse.edge == 0:
                countl[pulse.chan] += 1
    return countl
    
Count(count1000, '0Chan1000.dat')
Count(count900,'0Chan900.dat')
Count(count800,'0Chan800.dat')
Count(count700,'0Chan700.dat')
Count(count600,'0Chan600.dat')
Count(count500,'0Chan500.dat')

bins = [count1000[0], count900[0],count800[0],count700[0],count600[0],count500[0]]
thresh = [1000,900,800,700,600,500]
plt.plot(thresh, bins)
plt.ylabel("Events/Second")
plt.xlabel('Threshold (mV)')
plt.show()
