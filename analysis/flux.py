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
          
chan0eff = np.float16((np.float16(n1_true)/np.float16(n0_coinc))*100)
err0 = ((np.sqrt(n0_coinc)/n0_coinc)*100)+((np.sqrt(n1_true)/n1_true)*100)
chan1eff = np.float16((np.float16(n1_true)/np.float16(n1_coinc))*100)
err1 = ((np.sqrt(n1_coinc)/n1_coinc)*100)+((np.sqrt(n1_true)/n1_true)*100)
chan2eff = np.float16((np.float16(n2_true)/np.float16(n2_coinc))*100)
err2 = ((np.sqrt(n2_coinc)/n2_coinc)*100)+((np.sqrt(n2_true)/n2_true)*100)
chan3eff = np.float16((np.float16(n2_true)/np.float16(n0_coinc))*100)
err3 = ((np.sqrt(n0_coinc)/n0_coinc)*100)+((np.sqrt(n2_true)/n2_true)*100)
print(u"Channel 0 efficiency: {} \u00B1 {}%".format(int(chan0eff), int(err0)))
print(u"Channel 1 efficiency: {} \u00B1 {}%".format(int(chan1eff), int(err1)))
print(u"Channel 2 efficiency: {} \u00B1 {}%".format(int(chan2eff), int(err2)))
print(u"Channel 3 efficiency: {} \u00B1 {}%".format(int(chan3eff), int(err3)))

flux0 = (chan0/(chan0eff/100))/(720*1762)
flux0err = np.sqrt((((((1/(chan0eff/100))/(720*1762))*np.sqrt(chan0))**2))+ (((-(chan0/(chan0eff)**2)/(720*1762))*err0)**2))
flux1 = (chan1/(chan1eff/100))/(720*1762)
flux1err = np.sqrt((((((1/(chan1eff/100))/(720*1762))*np.sqrt(chan1))**2))+ (((-(chan1/(chan1eff)**2)/(720*1762))*err1)**2))
flux2 = (chan2/(chan2eff/100))/(720*1762)
flux2err = np.sqrt((((((1/(chan2eff/100))/(720*1762))*np.sqrt(chan2))**2))+ (((-(chan2/(chan2eff)**2)/(720*1762))*err2)**2))
flux3 = (chan3/(chan2eff/100))/(720*1762)
flux3err = np.sqrt((((((1/(chan3eff/100))/(720*1762))*np.sqrt(chan3))**2))+ (((-(chan3/(chan3eff)**2)/(720*1762))*err3)**2))
print(u"Flux across Channel 0: {} \u00B1 {} events per min per cm^2".format(flux0,flux0err))
print(u"Flux across Channel 1: {} \u00B1 {} events per min per cm^2".format(flux1,flux1err))
print(u"Flux across Channel 2: {} \u00B1 {} events per min per cm^2".format(flux2,flux2err))
print(u"Flux across Channel 3: {} \u00B1 {} events per min per cm^2".format(flux3,flux3err))
