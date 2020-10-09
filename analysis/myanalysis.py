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
            
# open the file
ifile = open(args.in_file, 'rb')
events= pickle.load(ifile)
n_events= len(events)

afile = open("0Chan1000.dat")
aevents= pickle.load(afile)
n10_events= len(aevents)
bfile = open("0Chan900.dat")
bevents= pickle.load(bfile)
n9_events= len(bevents)
cfile = open("0Chan800.dat")
cevents= pickle.load(cfile)
n8_events= len(cevents)
dfile = open("0Chan700.dat")
devents= pickle.load(dfile)
n7_events= len(devents)
efile = open("0Chan600.dat")
eevents= pickle.load(efile)
n6_events= len(eevents)
ffile = open("0Chan500.dat")
fevents= pickle.load(ffile)
n5_events= len(fevents)


print("Read {} events from file".format(n_events))

# example event loop
count = [0,0,0,0]
count1000 = [0, 0, 0, 0] 
count900 = [0, 0, 0, 0]
count800 = [0, 0, 0, 0]
count700 = [0, 0, 0, 0]
count600 = [0, 0, 0, 0]
count500 = [0, 0, 0, 0]# counts per channel

def Count(events, countl):
    for event in events:
        for pulse in event.pulses:
            # only count rising edges
            if pulse.edge == 0:
                countl[pulse.chan] += 1
    return countl
    
Count(aevents, count1000)
Count(bevents, count900)
Count(cevents, count800)
Count(devents, count700)
Count(eevents, count600)
Count(fevents, count500)

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
