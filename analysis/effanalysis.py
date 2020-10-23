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

print("Read {} events from file".format(n_events))

# example event loop
count = [0, 0, 0, 0]  # counts per channel

for event in events:
    for pulse in event.pulses:
        # only count rising edges
        if pulse.edge == 0:
            count[pulse.chan] += 1

print("Counts by channel")
print("Channel 0 : {} ".format(count[0]))
print("Channel 1 : {} ".format(count[1]))
print("Channel 2 : {} ".format(count[2]))
print("Channel 3 : {} ".format(count[3]))

# now find concidences betwen two channels (0 and 1)
n0_coinc = 0
n1_coinc = 0
n2_coinc = 0
n3_coinc = 0
n1_true = 0
n2_true = 0
n3_true = 0
for event in events:
    found0 = False
    found1 = False
    found2 = False
    found3 = False
    for pulse in event.pulses:
        # only count rising edges
        if pulse.edge==0 and pulse.chan == 0:
            found0 = True
        if pulse.edge==0 and pulse.chan == 1:
            found1 = True
        if pulse.edge==0 and pulse.chan == 2:
            found2 = True
        if pulse.edge==0 and pulse.chan == 3:
            found3 = True
    if found1 and found0 and found2:
        n1_true += 1
    if found0 and found2:
        n1_coinc += 1
    if found1 and found2 and found3:
        n2_true += 1
    if found1 and found3:
        n2_coinc += 1
    if found0 and found1 and found3:
        n3_true += 1
    if found0 and found1:
        n3_coinc += 1
    if found1 and found2:
        n0_coinc += 1
        
chan0 = count[0]
chan1 = count[1]
chan2 = count[2]
chan3 = count[3]
        
print("Channel 0 efficiency: {}%".format(np.float16((np.float16(n1_true)/np.float16(chan0))*100)))
print("Channel 1 efficiency: {}%".format(np.float16((np.float16(n1_true)/np.float16(chan1))*100)))
print("Channel 2 efficiency: {}%".format(np.float16((np.float16(n2_true)/np.float16(chan2))*100)))
print("Channel 3 efficiency: {}%".format(np.float16((np.float16(n3_true)/np.float16(chan3))*100)))

