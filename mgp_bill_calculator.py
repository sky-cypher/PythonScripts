#!/usr/bin/env python3

import re
import sys
import subprocess
from rich.console import Console
from rich.table import Table

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
        global total_commission
        total_commission += int(temp)
        return('\u20b9' + str(int(bill)))


subprocess.run(
        f"pdftotext {sys.argv[1]} grahak-bill.txt",
        shell=True)

table = Table(title="grahak-bill",show_lines=True)

table.add_column("Name")
table.add_column("Amount", style="green")
table.add_column("Bags", style="yellow")

total_commission = 0
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
if(len(names) != len(bags_bill)):
        print("Error while parsing: count mismatch")
        exit(1)

bills = [ x.split()[-1] for x in bags_bill ]
bags = [ x.split()[0] for x in bags_bill ]

for name, bill, bag in zip(names, bills, bags):
        if 'AARTI' in name:
                continue
        table.add_row(
                ''.join(
                    [ x.capitalize() + ' ' for x in name.split()]
                ),
                calculate_bill(bill),
                bag
        )

console = Console()
console.print(table)
print("\nTotal commission :", total_commission)
