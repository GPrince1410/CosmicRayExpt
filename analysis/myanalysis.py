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

parser = argparse.ArgumentParser(description='Analyse CSV file')
parser.add_argument("-i", "--in_file", help="input file")
parser.add_argument("-o", "--out_file", help='output file')
parser.add_argument("-n", "--n_max", help='max number of lines to process')

args = parser.parse_args()

print("Starting analysis")



print("Read {} events from file".format(n_events))

# example event loop
count1000 = [0, 0, 0, 0] 
count900 = [0, 0, 0, 0]
count800 = [0, 0, 0, 0]
count700 = [0, 0, 0, 0]
count600 = [0, 0, 0, 0]
count500 = [0, 0, 0, 0]# counts per channel

def Count(events, countl,file):
    
    ifile = open(file, 'rb')
    events= pickle.load(ifile)
    
    for event in events:
        for pulse in event.pulses:
            # only count rising edges
            if pulse.edge == 0:
                countl[pulse.chan] += 1
    return countl
    
Count(aevents, count1000, '0Chan1000.txt')
Count(bevents, count900,'0Chan900.txt')
Count(cevents, count800,'0Chan800.txt')
Count(devents, count700,'0Chan700.txt')
Count(eevents, count600,'0Chan600.txt')
Count(fevents, count500,'0Chan500.txt')

print("Counts by channel")
print("Channel 0 : {} ".format(count[0]))
print("Channel 1 : {} ".format(count[1]))
print("Channel 2 : {} ".format(count[2]))
print("Channel 3 : {} ".format(count[3]))

# now find concidences betwen two channels (0 and 1)
n_coinc = 0
for event in events:
    found0 = False
    found1 = False
    for pulse in event.pulses:
        # only count rising edges
        if pulse.edge==0 and pulse.chan == 0:
            found0 = True
        if pulse.edge==0 and pulse.chan == 1:
            found1 = True
    if found0 and found1:
        n_coinc += 1
            
print("N (0,1) coincidences : {}".format(n_coinc))

# get some pulse time information
dts = []
for event in events:
    found0 = False
    found1 = False
    time0 = 0.
    time1 = 0.
    for pulse in event.pulses:
        # only count rising edges
        if pulse.edge==0 and pulse.chan == 0:
            found0 = True
            time0 = pulse.time
        if pulse.edge==0 and pulse.chan == 1:
            found1 = True
            time1 = pulse.time
    if found0 and found1:
        dts.append(abs(time1-time0))

# print some summary info
print("Mean delta-t : {}".format(np.mean(dts)))
print("Std dev delta-t : {}".format(np.std(dts)))

bins = [count1000[0], count900[0],count800[0],count700[0],count600[0],count500[0]]
thresh = [1000,900,800,700,600,500]
plt.plot(thresh, bins)
plt.ylabel("Events/Second")
plt.xlabel('Threshold (mV)')
plt.show()
