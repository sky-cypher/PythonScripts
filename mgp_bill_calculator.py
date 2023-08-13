#!/usr/bin/env python3

import re
import sys
import subprocess

if len(sys.argv) != 2:
        print("Check Arguments")
        exit(0)

def calculate_bill(bill, ignore = 0):
        bill = float(bill)
        temp = (bill - ignore) / 100
        temp = round(temp,2)
        temp *= 100
        temp *= 0.03
        bill += temp
        return int(bill)

subprocess.run(
        f"pdftotext {sys.argv[1]} grahak-bill.txt",
        shell=True)

content = ""
lines = []
with open("grahak-bill.txt") as file:
        lines = file.readlines()
subprocess.run("rm grahak-bill.txt", shell=True)

save = False
for line in lines:
        if save:
                if re.search('^-',line):
                        save = False
                        break
                content += ''.join(line)
        if not save and re.search('-?#', line):
                save = True

names = re.findall(r'[A-Z]+\s[A-Z]+\s[A-Z]+', content)
bags_bill = re.findall(r'[0-9]+\s\|\s[0-9]+\.[0-9]', content)
bills = [ x.split()[-1] for x in bags_bill ]
bags = [ x.split()[0] for x in bags_bill ]

print("Name\tAmount\tBags")
for name, bill, bag in zip(names, bills, bags):
        if 'AARTI' in name:
                continue
        print(''.join( [ x.capitalize() + ' ' for x in name.split()]),
              calculate_bill(bill),
              bag,
              sep='\t'
              )

