#!/usr/bin/env python

from optparse import OptionParser
from ConfigParser import ConfigParser
import sys
import os

import daq

def main():
 
    # get command line options
    parser = OptionParser()
    parser.add_option('-o','--outfile',dest='outfile',
                       default=None,help='Path of output file')
    parser.add_option('-s','--setup',dest='cfgfile',
                       default=os.getenv('CR_BASE')+'/DAQ/daq.cfg',help='Path of config file')
    parser.add_option('-t','--time',dest='time',
                       default=0,help='Time to run in seconds')
    parser.add_option('-g','--gate',dest='gate',
                       default=None,help='Gate in units of 40ns')
    parser.add_option('-w','--window',dest='window',
                       default=None,help='Time window in units of 40 ns')
    parser.add_option('-c','--coincidence',dest='coinc',
                       default=None,help='Coincidence code (see manual)')
    parser.add_option('-e','--enable',dest='enable',
                       default=None,help='Channel enable code (see manual)')
    parser.add_option('-0','--threshold-ch0',dest='thresh_ch0',
                       default=None,help='Threshold channel 0')
    parser.add_option('-1','--threshold-ch1',dest='thresh_ch1',
                       default=None,help='Threshold channel 1')
    parser.add_option('-2','--threshold-ch2',dest='thresh_ch2',
                       default=None,help='Threshold channel 2')
    parser.add_option('-3','--threshold-ch3',dest='thresh_ch3',
                       default=None,help='Threshold channel 3')
    (options, args) = parser.parse_args(sys.argv[1:])

    # get default options from config file where not set at command line
    config = ConfigParser()
    config.readfp(open(options.cfgfile))

    serialPort = config.get('communication','port')

#    if (options.time == None) :
#        time = config.getint('daq','time')
#    else :
#        time = None

    if (options.enable == None) :
        enable = config.get('daq','enable')
    else :
        enable = options.time

    if (options.gate == None) :
        gate = config.getint('daq','gate')
    else :
        gate = int(options.gate)

    if (options.window == None) :
        window = config.getint('daq','window')
    else :
        window = int(options.window)

    if (options.coinc == None) :
        coinc = config.get('daq','coincidence')
    else :
        coinc = options.coinc

    thresh = [0,0,0,0]
    if (options.thresh_ch0 == None) :
        thresh[0] = config.getint('daq','thresh_ch0')
    else :
        thresh[0] = options.thresh_ch0

    if (options.thresh_ch1 == None) :
        thresh[1] = config.getint('daq','thresh_ch1')
    else :
        thresh[1] = options.thresh_ch1

    if (options.thresh_ch2 == None) :
        thresh[2] = config.getint('daq','thresh_ch2')
    else :
        thresh[2] = options.thresh_ch2

    if (options.thresh_ch3 == None) :
        thresh[3] = config.getint('daq','thresh_ch3')
    else :
        thresh[3] = options.thresh_ch3        

    # connect to the hardware
    port = daq.connect()

    # setup the board
    daq.setup(port, thresh, enable, coinc, gate, window)

    # record the data
    daq.run(port, options.outfile, int(options.time))



if __name__ == '__main__':
    main()
