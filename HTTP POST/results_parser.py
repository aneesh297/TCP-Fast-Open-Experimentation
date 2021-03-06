#!/usr/bin/python

import sys
import re
import csv

vanilla_times = []
tfo_times = []
site = None;
tcp_protocol = None;
tfo = None;
filename = "results.txt"

with open('results.csv', 'w') as csvfile:
    fieldnames = ['Website', 'tcp', 'Time for transfer', 'Delay', 'Bandwidth']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

with open(filename) as f:
    for line in f:
        if "===" in line:
            line = line.replace("=", "")
            line = line.replace(" ", "")
            site = line.strip()
        if "cubic" in line:
            tcp_protocol = "cubic"
        if "westwood" in line:
            tcp_protocol = "westwood"
        if "tfo enabled" in line:
            tfo = True
        if "vanilla tcp" in line:
            tfo = False
        if "Delay" in line:
            m = re.search("\d", line)
            first_digit = m.start()
            delay = line[first_digit:]
            delay = delay.strip()
        
        if "Bandwidth" in line:
            m = re.search("\d", line)
            first_digit = m.start()
            band = line[first_digit:]
            band = band.strip()
    
        if "Time for transfer" in line:
            m = re.search("\d", line)
            first_digit = m.start()
            time = float(line[first_digit:])
            if tfo:
                tfo_times.append(time)
            else:
                vanilla_times.append(time)
            
            
            if delay == "100" and tfo and band == "5":
                print len(vanilla_times), len(tfo_times)
                print "\nsite: " + site
                print "tcp protocol: " + tcp_protocol
                delays = [10, 20, 50, 100]
                bandwidths = [5]
                m = len(delays)
                n = len(bandwidths)
                for i in range(len(delays)):
                    for j in range(len(bandwidths)):
                        print "delay: " + str(delays[i])
                        print "bandwitdh: " + str(bandwidths[j])
                        print "% improvement: " + str(100 * (abs(tfo_times[i*n+j] - vanilla_times[i*n+j]) / (vanilla_times[i*n+j])))
                        with open('results.csv' ,'a') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow({'Website' : site, 'tcp': 'tcp fast_open' , 'Time for transfer':tfo_times[i*n+j], 'Delay' : delays[i], 'Bandwidth': bandwidths[j]})
                            writer.writerow({'Website' : site, 'tcp': 'vanilla' , 'Time for transfer': vanilla_times[i*n+j], 'Delay' : delays[i],'Bandwidth': bandwidths[j]})
                vanilla_times = []
                tfo_times = []

